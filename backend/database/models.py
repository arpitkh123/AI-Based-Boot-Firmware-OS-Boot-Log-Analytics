from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
import datetime

# from database.base import Base
from backend.database.base import Base

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, unique=True, index=True, nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    analysis_time = Column(Float, nullable=True)
    processing_time = Column(Float, nullable=True)
    status = Column(String, default="success")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # 1-to-1 relationships
    prediction = relationship("Prediction", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    boot = relationship("Boot", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    boot_progress = relationship("BootProgress", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    failure_flags = relationship("FailureFlags", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    environment = relationship("Environment", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    statistics = relationship("Statistics", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    recommendation = relationship("Recommendation", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    
    # 1-to-many relationships
    error_logs = relationship("ErrorLog", back_populates="analysis", cascade="all, delete-orphan")
    warning_logs = relationship("WarningLog", back_populates="analysis", cascade="all, delete-orphan")
    templates = relationship("Template", back_populates="analysis", cascade="all, delete-orphan")


class Prediction(Base):
    __tablename__ = "prediction"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False, unique=True)
    prediction_class = Column(String)
    confidence = Column(Float)
    severity = Column(String)
    anomaly_score = Column(Float)
    
    analysis = relationship("Analysis", back_populates="prediction")


class Boot(Base):
    __tablename__ = "boot"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False, unique=True)
    boot_success = Column(Boolean)
    boot_duration = Column(Float)
    failure_stage = Column(String, nullable=True)
    failure_type = Column(String, nullable=True)
    failure_reason = Column(Text, nullable=True)
    failure_log = Column(Text, nullable=True)
    
    analysis = relationship("Analysis", back_populates="boot")


class BootProgress(Base):
    __tablename__ = "boot_progress"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False, unique=True)
    kernel_started = Column(Boolean, default=False)
    rootfs_mounted = Column(Boolean, default=False)
    init_started = Column(Boolean, default=False)
    login_prompt = Column(Boolean, default=False)
    boot_completed = Column(Boolean, default=False)
    
    analysis = relationship("Analysis", back_populates="boot_progress")


class FailureFlags(Base):
    __tablename__ = "failure_flags"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False, unique=True)
    kernel_panic = Column(Boolean, default=False)
    dma_failure = Column(Boolean, default=False)
    irq_failure = Column(Boolean, default=False)
    filesystem_failure = Column(Boolean, default=False)
    rootfs_failure = Column(Boolean, default=False)
    cpu_failure = Column(Boolean, default=False)
    oom = Column(Boolean, default=False)
    dtb_failure = Column(Boolean, default=False)
    init_failure = Column(Boolean, default=False)
    
    analysis = relationship("Analysis", back_populates="failure_flags")


class Environment(Base):
    __tablename__ = "environment"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False, unique=True)
    machine_model = Column(String, nullable=True)
    kernel_version = Column(String, nullable=True)
    architecture = Column(String, nullable=True)
    boot_type = Column(String, nullable=True)
    start_timestamp = Column(Float, nullable=True)
    end_timestamp = Column(Float, nullable=True)
    
    analysis = relationship("Analysis", back_populates="environment")


class Statistics(Base):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False, unique=True)
    logs_parsed = Column(Integer, default=0)
    total_lines = Column(Integer, default=0)
    ignored_lines = Column(Integer, default=0)
    errors = Column(Integer, default=0)
    warnings = Column(Integer, default=0)
    templates = Column(Integer, default=0)
    features = Column(Integer, default=0)
    
    analysis = relationship("Analysis", back_populates="statistics")


class Recommendation(Base):
    __tablename__ = "recommendation"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False, unique=True)
    technical_report = Column(Text, nullable=True)
    
    analysis = relationship("Analysis", back_populates="recommendation")


class ErrorLog(Base):
    __tablename__ = "error_logs"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False)
    line_number = Column(Integer)
    timestamp = Column(Float, nullable=True)
    subsystem = Column(String)
    severity = Column(String)
    message = Column(Text)
    
    analysis = relationship("Analysis", back_populates="error_logs")


class WarningLog(Base):
    __tablename__ = "warning_logs"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False)
    line_number = Column(Integer)
    timestamp = Column(Float, nullable=True)
    subsystem = Column(String)
    severity = Column(String)
    message = Column(Text)
    
    analysis = relationship("Analysis", back_populates="warning_logs")


class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analysis.analysis_id", ondelete="CASCADE"), nullable=False)
    template_text = Column(Text)
    occurrences = Column(Integer, default=1)
    
    analysis = relationship("Analysis", back_populates="templates")
