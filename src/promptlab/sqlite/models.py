from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Asset(Base):
    __tablename__ = "assets"
    asset_name = Column(String, primary_key=True)
    asset_version = Column(Integer, primary_key=True)
    asset_description = Column(Text)
    asset_type = Column(String)
    asset_binary = Column(Text)  # Store as JSON/text
    is_deployed = Column(Boolean, default=False)
    deployment_time = Column(DateTime)
    status = Column(Integer, default=1)  # 1 - 'active', 0 - 'inactive'
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="assets")


class Experiment(Base):
    __tablename__ = "experiments"
    experiment_id = Column(String, primary_key=True)
    model = Column(Text)  # Store as JSON/text
    asset = Column(Text)  # Store as JSON/text
    status = Column(Integer, default=1)  # 1 - 'active', 0 - 'inactive'
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="experiments")
    results = relationship("ExperimentResult", back_populates="experiment")


class ExperimentResult(Base):
    __tablename__ = "experiment_result"
    id = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id = Column(String, ForeignKey("experiments.experiment_id"))
    dataset_record_id = Column(String)
    completion = Column(Text)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    latency_ms = Column(Float)
    evaluation = Column(Text)  # Store as JSON/text
    created_at = Column(DateTime, default=datetime.now())
    experiment = relationship("Experiment", back_populates="results")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'admin' or 'engineer'
    status = Column(Integer, default=1)  # 1 - 'active', 0 - 'inactive'
    created_at = Column(DateTime, default=datetime.now())
    assets = relationship("Asset", back_populates="user")
    experiments = relationship("Experiment", back_populates="user")
