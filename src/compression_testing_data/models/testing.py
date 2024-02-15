import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, CheckConstraint, DateTime
from .base import Base


class CompressionTrial(Base):
    __tablename__ = 'Compression_Trials'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    frames_per_step_target = Column(Integer, nullable=False, default=100)
    strain_delta_target = Column(Float, nullable=False, default=0.1)  # engineering strain
    strain_limit = Column(Float, nullable=False, default=0.8)  # 4mm

    force_limit = Column(Float, nullable=False, default=1000)
    force_zero = Column(Float, nullable=False, default=0)
    force_unit = Column(String(5), nullable=False, default='N')

    sample_id = Column(Integer, ForeignKey('Samples.id', ondelete="CASCADE"))
    sample = relationship('Sample', back_populates='trials')

    steps = relationship(
        'CompressionStep',
        back_populates='compression_trial',
        cascade="all, delete",
        passive_deletes=True
    )


class CompressionStep(Base):
    __tablename__ = 'Compression_Steps'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # height can be derived from any choice of strain encoder or strain cam
    strain_target = Column(Float, nullable=False)
    strain_encoder = Column(Float)
    # strain_stl = Column(Float)

    force = Column(Float)

    compression_trial_id = Column(Integer, ForeignKey('Compression_Trials.id', ondelete="CASCADE"))
    compression_trial = relationship('CompressionTrial', back_populates='steps')

    frames = relationship(
        'Frame',
        back_populates='compression_step',
        cascade="all, delete",
        passive_deletes=True
    )


class Frame(Base):
    __tablename__ = 'Frames'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    file_extension = Column(String)
    file_name = Column(String)
    filepath = Column(String)

    camera_setting_id = Column(Integer, ForeignKey('Camera_Settings.id', ondelete="CASCADE"))
    camera_setting = relationship('CameraSetting', back_populates='frames')

    compression_step_id = Column(Integer, ForeignKey('Compression_Steps.id', ondelete="CASCADE"))
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
