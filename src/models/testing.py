import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint, DateTime
from .base import Base


class CompressionTrial(Base):
    __tablename__ = 'Compression_Trials'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    frames_per_step_target = Column(Integer, nullable=False, default=100)
    strain_delta_target = Column(Float, nullable=False, default=0.1)  # engineering strain
    force_limit = Column(Float, nullable=False, default=1000)  # newtons
    strain_limit = Column(Float, nullable=False, default=0.2)  # 4mm

    sample_id = Column(Integer, ForeignKey('Samples.id'))
    sample = relationship('Sample', back_populates='trials')

    steps = relationship('CompressionStep', back_populates='compression_trial')


class CompressionStep(Base):
    __tablename__ = 'Compression_Steps'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    strain_target = Column(Float, nullable=False)
    # strain_encoder - motor rotations
    # strain_cam - dist between platons
    # min_strain
    force = Column(Float, nullable=False)
    # max_force (do not want to exceed a given amount)

    compression_trial_id = Column(Integer, ForeignKey('Compression_Trials.id'))
    compression_trial = relationship('CompressionTrial', back_populates='steps')

    frames = relationship('Frame', back_populates='compression_step')


class Frame(Base):
    __tablename__ = 'Frames'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    file_extension = Column(String)
    filepath = Column(String)

    camera_setting_id = Column(Integer, ForeignKey('Camera_Settings.id'))
    camera_setting = relationship('CameraSetting', back_populates='frames')

    compression_step_id = Column(Integer, ForeignKey('Compression_Steps.id'))
    compression_step = relationship('CompressionStep', back_populates='frames')

    __table_args__ = (
        CheckConstraint(file_extension.in_([
            'jpg', 'jpeg', 'jp2', 'j2k', 'jxl', 'tif', 'tiff', 'png', 'bmp',
            'exr', 'tga', 'bpm', 'ppm', 'dng', 'mpo', 'seq', 'ara'
        ])),
    )

# TODO add other artifacts
#   stls - plys - psx meta project - etc


TestComponentModels = [cls for cls in Base.__subclasses__()]
