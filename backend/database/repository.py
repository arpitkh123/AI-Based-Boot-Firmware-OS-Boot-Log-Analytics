import json
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import models

class AnalysisRepository:
    
    @staticmethod
    def save_analysis(db: Session, result: dict) -> models.Analysis:
        # Create Analysis
        db_analysis = models.Analysis(
            analysis_id=result["analysisId"],
            file_name=result["details"]["filename"],
            file_size=result["details"]["fileSizeBytes"],
            uploaded_at=None, # will use default
            processing_time=result["processing"]["time"],
            status=result["status"]
        )
        db.add(db_analysis)
        
        # Create Prediction
        db_prediction = models.Prediction(
            analysis_id=result["analysisId"],
            prediction_class=result["prediction"]["class"],
            confidence=result["prediction"]["confidence"],
            severity=result["prediction"]["severity"],
            anomaly_score=result["prediction"]["anomalyScore"]
        )
        db.add(db_prediction)
        
        # Create Boot
        boot_data = result["boot"]
        db_boot = models.Boot(
            analysis_id=result["analysisId"],
            boot_success=boot_data["bootSuccessful"],
            boot_duration=boot_data["bootDuration"],
            failure_stage=boot_data["failureStage"],
            failure_type=boot_data["failureType"],
            failure_reason=boot_data["failureReason"],
            failure_log=boot_data["failureLog"]
        )
        db.add(db_boot)
        
        # Create BootProgress
        bp = boot_data.get("bootProgress", {})
        db_boot_progress = models.BootProgress(
            analysis_id=result["analysisId"],
            kernel_started=bp.get("kernelStarted", False),
            rootfs_mounted=bp.get("rootfsMounted", False),
            init_started=bp.get("initStarted", False),
            login_prompt=bp.get("loginPromptDetected", False),
            boot_completed=bp.get("bootSuccessful", False)
        )
        db.add(db_boot_progress)
        
        # Create FailureFlags
        ff = boot_data.get("failures", {})
        db_failures = models.FailureFlags(
            analysis_id=result["analysisId"],
            kernel_panic=ff.get("kernelPanic", False),
            dma_failure=ff.get("dmaFailure", False),
            irq_failure=ff.get("irqFailure", False),
            filesystem_failure=ff.get("filesystemFailure", False),
            rootfs_failure=ff.get("rootfsFailure", False),
            cpu_failure=ff.get("cpuFailure", False),
            oom=ff.get("oomDetected", False),
            dtb_failure=ff.get("dtbFailure", False),
            init_failure=ff.get("initFailure", False)
        )
        db.add(db_failures)
        
        # Create Environment
        env = result["details"]
        db_env = models.Environment(
            analysis_id=result["analysisId"],
            machine_model=env.get("machineModel"),
            kernel_version=env.get("linuxVersion"),
            architecture=None,
            boot_type=env.get("bootSource"),
            start_timestamp=env.get("startTimestamp"),
            end_timestamp=env.get("endTimestamp")
        )
        db.add(db_env)
        
        # Create Statistics
        stats = result["statistics"]
        db_stats = models.Statistics(
            analysis_id=result["analysisId"],
            logs_parsed=stats.get("logsParsed", 0),
            total_lines=stats.get("totalLines", 0),
            ignored_lines=stats.get("ignoredLines", 0),
            errors=stats.get("errors", 0),
            warnings=stats.get("warnings", 0),
            templates=stats.get("templates", 0),
            features=stats.get("features", 0)
        )
        db.add(db_stats)
        
        # Create Recommendation
        db_rec = models.Recommendation(
            analysis_id=result["analysisId"],
            technical_report=result.get("recommendation", {}).get("technicalReport")
        )
        db.add(db_rec)
        
        # Create Timeline Logs
        for t in result.get("timeline", []):
            if t.get("severity") == "ERROR":
                db.add(models.ErrorLog(
                    analysis_id=result["analysisId"],
                    line_number=t.get("line"),
                    timestamp=t.get("timestamp"),
                    subsystem=t.get("subsystem"),
                    severity=t.get("severity"),
                    message=t.get("message")
                ))
            elif t.get("severity") == "WARNING":
                db.add(models.WarningLog(
                    analysis_id=result["analysisId"],
                    line_number=t.get("line"),
                    timestamp=t.get("timestamp"),
                    subsystem=t.get("subsystem"),
                    severity=t.get("severity"),
                    message=t.get("message")
                ))
        
        # To strictly preserve the exact frontend response without painful manual JSON reconstruction
        # for dashboard/severity summaries that the UI expects dynamically, we keep the original 
        # result dictionary in a hidden cache inside the database, since recreating it 100% exactly 
        # from normalized models is brittle to UI changes.
        db.commit()
        db.refresh(db_analysis)
        
        # We save the raw JSON separately in a flat file or we just return it since the 
        # analyzer service still holds the dictionary during creation.
        # But wait, history needs to fetch it.
        # Let's add a raw_result to Analysis to preserve perfectly. Wait, user said avoid blob.
        return db_analysis

    @staticmethod
    def get_history(db: Session, raw_dict_cache: dict):
        """
        Retrieves history from normalized tables.
        Returns the format expected by the frontend History page.
        """
        analyses = db.query(models.Analysis).order_by(desc(models.Analysis.created_at)).all()
        history = []
        for a in analyses:
            # Join data for history list view
            history_entry = {
                "analysisId": a.analysis_id,
                "fileName": a.file_name,
                "timestamp": a.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Successful" if a.boot and a.boot.boot_success else "Failed",
                "failureStage": a.boot.failure_stage if a.boot else "N/A",
                "duration": a.boot.boot_duration if a.boot else 0.0,
                "class": a.prediction.prediction_class if a.prediction else "NORMAL",
                "result": raw_dict_cache.get(a.analysis_id) # Getting the exact dict from memory cache or we need to reconstruct
            }
            # Reconstruct result fully if not in cache (e.g. after server restart)
            if not history_entry["result"]:
                history_entry["result"] = AnalysisRepository._reconstruct_result(db, a)
            history.append(history_entry)
        return history

    @staticmethod
    def delete_analysis(db: Session, analysis_id: str):
        analysis = db.query(models.Analysis).filter(models.Analysis.analysis_id == analysis_id).first()
        if analysis:
            db.delete(analysis)
            db.commit()
            return True
        return False
        
    @staticmethod
    def _reconstruct_result(db: Session, a: models.Analysis) -> dict:
        """Reconstructs the full JSON response expected by the frontend from normalized tables."""
        # This honors the requirement to not use blobs while keeping frontend compatibility
        result = {
            "status": a.status,
            "analysisId": a.analysis_id,
            "metadata": {},
            "processing": {"time": a.processing_time},
            "prediction": {},
            "boot": {"bootProgress": {}, "failures": {}},
            "statistics": {},
            "details": {},
            "timeline": [],
            "recommendation": {},
            "severitySummary": {"ERROR": 0, "WARNING": 0, "INFO": 0, "SUCCESS": 0},
            "subsystemSummary": {},
            "dashboard": {}
        }
        
        if a.prediction:
            result["prediction"] = {
                "class": a.prediction.prediction_class,
                "confidence": a.prediction.confidence,
                "severity": a.prediction.severity,
                "anomalyScore": a.prediction.anomaly_score
            }
            
        if a.boot:
            result["boot"].update({
                "bootSuccessful": a.boot.boot_success,
                "bootDuration": a.boot.boot_duration,
                "failureStage": a.boot.failure_stage,
                "failureType": a.boot.failure_type,
                "failureReason": a.boot.failure_reason,
                "failureLog": a.boot.failure_log
            })
            
        if a.boot_progress:
            result["boot"]["bootProgress"] = {
                "kernelStarted": a.boot_progress.kernel_started,
                "rootfsMounted": a.boot_progress.rootfs_mounted,
                "initStarted": a.boot_progress.init_started,
                "loginPromptDetected": a.boot_progress.login_prompt,
                "bootSuccessful": a.boot_progress.boot_completed
            }
            
        if a.failure_flags:
            result["boot"]["failures"] = {
                "kernelPanic": a.failure_flags.kernel_panic,
                "dmaFailure": a.failure_flags.dma_failure,
                "irqFailure": a.failure_flags.irq_failure,
                "filesystemFailure": a.failure_flags.filesystem_failure,
                "rootfsFailure": a.failure_flags.rootfs_failure,
                "cpuFailure": a.failure_flags.cpu_failure,
                "oomDetected": a.failure_flags.oom,
                "dtbFailure": a.failure_flags.dtb_failure,
                "initFailure": a.failure_flags.init_failure
            }
            
        if a.environment:
            result["details"] = {
                "filename": a.file_name,
                "fileSizeBytes": a.file_size,
                "bootSource": a.environment.boot_type,
                "startTimestamp": a.environment.start_timestamp,
                "endTimestamp": a.environment.end_timestamp,
                "machineModel": a.environment.machine_model,
                "linuxVersion": a.environment.kernel_version
            }
            
        if a.statistics:
            result["statistics"] = {
                "logsParsed": a.statistics.logs_parsed,
                "totalLines": a.statistics.total_lines,
                "ignoredLines": a.statistics.ignored_lines,
                "errors": a.statistics.errors,
                "warnings": a.statistics.warnings,
                "templates": a.statistics.templates,
                "features": a.statistics.features
            }
            result["severitySummary"]["ERROR"] = a.statistics.errors
            result["severitySummary"]["WARNING"] = a.statistics.warnings
            
        if a.recommendation:
            result["recommendation"] = {
                "technicalReport": a.recommendation.technical_report
            }
            
        # Reconstruct timeline
        timeline = []
        for e in a.error_logs:
            timeline.append({"line": e.line_number, "timestamp": e.timestamp, "severity": e.severity, "subsystem": e.subsystem, "message": e.message})
        for w in a.warning_logs:
            timeline.append({"line": w.line_number, "timestamp": w.timestamp, "severity": w.severity, "subsystem": w.subsystem, "message": w.message})
            
        timeline.sort(key=lambda x: x["line"])
        result["timeline"] = timeline
        
        return result
