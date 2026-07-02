from src.knowledge_base.repository import KBRepository

class RuleEngine:
    """
    Deterministic rule engine that checks parsed logs for known signatures 
    before passing them to the ML pipeline.
    """
    def __init__(self, kb_repo: KBRepository = None):
        self.kb_repo = kb_repo if kb_repo else KBRepository()

    def evaluate(self, parsed_logs: list, boot_analysis: dict = None) -> list:
        """
        Evaluates the logs against deterministic rules and the Knowledge Base.
        Returns a list of anomalies (if any).
        """
        anomalies = []
        
        # We will parse backwards to find the latest critical error first, 
        # or we can just scan all. Let's scan all.
        for log in parsed_logs:
            text = str(log.get('payload', log.get('message', ''))).lower()
            raw = str(log.get('raw', text))
            line_no = log.get('line_no', 0)
            
            # 1. Check against the Knowledge Base
            kb_match = self.kb_repo.find_match(raw)
            if kb_match:
                anomalies.append({
                    "line": line_no,
                    "reason": kb_match['type'],
                    "severity": "CRITICAL" if kb_match['confidence'] == 'HIGH' else "WARNING",
                    "model": "KNOWLEDGE_BASE",
                    "raw": raw,
                    "kb_resolution": kb_match['resolution'],
                    "kb_confidence": kb_match['confidence']
                })
                continue # Don't need to check hardcoded rules if KB matched

            # 2. Hardcoded specific rules (Fallback if KB doesn't have it)
            if 'unknown kernel command line parameters' in text:
                anomalies.append({"line": line_no, "reason": "Broken bootargs", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            elif 'unable to register' in text and 'port' in text:
                anomalies.append({"line": line_no, "reason": "UART Registration Failure", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            elif 'kernel panic' in text or 'end kernel panic' in text or 'kernel bug' in text:
                anomalies.append({"line": line_no, "reason": "Kernel Panic / Crash", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            elif 'oops' in text and ('bug' in text or 'error' in text):
                anomalies.append({"line": line_no, "reason": "Kernel Oops", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            elif 'out of memory' in text and 'kill process' in text:
                anomalies.append({"line": line_no, "reason": "OOM Killer activated", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            elif 'null pointer dereference' in text:
                anomalies.append({"line": line_no, "reason": "NULL Pointer Dereference", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            elif 'segfault' in text:
                anomalies.append({"line": line_no, "reason": "Segmentation Fault", "severity": "CRITICAL", "model": "RULE_KERNEL", "raw": raw})
            elif 'i/o error' in text or 'io error' in text:
                anomalies.append({"line": line_no, "reason": f"I/O Error: {text[:60]}", "severity": "WARNING", "model": "RULE_KERNEL", "raw": raw})
            elif 'timeout waiting for hardware' in text:
                anomalies.append({"line": line_no, "reason": "Hardware timeout (possible SD card issue)", "severity": "WARNING", "model": "RULE_KERNEL", "raw": raw})
                
        return anomalies
