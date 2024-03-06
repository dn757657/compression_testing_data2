import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, UniqueConstraint, Boolean, Integer, String, Float, ForeignKey, CheckConstraint, DateTime
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

    #is_calibration = Column(Boolean, nullable=False, default=False)

    sample_id = Column(Integer, ForeignKey('Samples.id', ondelete="CASCADE"))
    sample = relationship('Sample', back_populates='trials')

    phantom_id = Column(Integer, ForeignKey('Phantoms.id', ondelete="CASCADE"))
    phantom = relationship('Phantom', back_populates='trials')

    steps = relationship(
        'CompressionStep',
        back_populates='compression_trial',
        cascade="all, delete",
        passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint(
            '(sample_id IS NOT NULL AND phantom_id IS NULL) OR '
            '(sample_id IS NULL AND phantom_id IS NOT NULL)',
            name='check_only_one_sample'
        ),
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

    metashape_projects = relationship(
        'MetashapeProject',
        back_populates='compression_step',
        cascade="all, delete",
        passive_deletes=True
    )

    full_point_clouds = relationship(
        'FullPointCloud',
        back_populates='compression_step',
        cascade="all, delete",
        passive_deletes=True
    )

    processed_point_clouds = relationship(
        'ProcessedPointCloud',
        back_populates='compression_step',
        cascade="all, delete",
        passive_deletes=True
    )

    stls = relationship(
        'ProcessedSTL',
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
    # filepath = Column(String)

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


class MetashapeProject(Base):
    __tablename__ = 'Metashape_Projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    file_extension = Column(String)
    file_name = Column(String)
    # filepath = Column(String)

    # step also links to frames
    compression_step_id = Column(Integer, ForeignKey('Compression_Steps.id', ondelete="CASCADE"))
    compression_step = relationship('CompressionStep', back_populates='metashape_projects')

    __table_args__ = (
        CheckConstraint(file_extension.in_(['psx'])),
    )


class FullPointCloud(Base):
    __tablename__ = 'Full_Point_Clouds'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    file_extension = Column(String)
    file_name = Column(String)
    # filepath = Column(String)

    # step also links to frames
    compression_step_id = Column(Integer, ForeignKey('Compression_Steps.id', ondelete="CASCADE"))
    compression_step = relationship('CompressionStep', back_populates='full_point_clouds')

    metashape_ply_export_setting_id = Column(Integer, ForeignKey('Metashape_PLY_Export_Settings.id', ondelete="CASCADE"))
    metashape_ply_export_setting = relationship('MetashapePlyExportSetting', back_populates='full_point_clouds')

    metashape_ply_generation_setting_id = Column(Integer, ForeignKey('Metashape_PLY_Generation_Settings.id', ondelete="CASCADE"))
    metashape_ply_generation_setting = relationship('MetashapePlyGenerationSetting', back_populates='full_point_clouds')

    __table_args__ = (
        CheckConstraint(file_extension.in_(['ply'])),
        UniqueConstraint(
            'compression_step_id',
            'metashape_ply_export_setting_id',
            'metashape_ply_generation_setting_id',
            name=f'uix_{__tablename__}'
        ),
    )


class ProcessedPointCloud(Base):
    __tablename__ = 'Processed_Point_Clouds'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    file_extension = Column(String)
    file_name = Column(String)
    # filepath = Column(String)

    scaling_factor = Column(Float, default=0)

    # step also links to frames
    compression_step_id = Column(Integer, ForeignKey('Compression_Steps.id', ondelete="CASCADE"))
    compression_step = relationship('CompressionStep', back_populates='processed_point_clouds')

    stls = relationship(
        'ProcessedSTL',
        back_populates='processed_point_cloud',
        cascade="all, delete",
        passive_deletes=True
    )

    # open3d options!
    open3d_segmentation_setting_id = Column(Integer, ForeignKey('Open3D_Segmentation_Settings.id', ondelete="CASCADE"))
    open3d_segmentation_setting = relationship('Open3DSegmentationSetting', back_populates='processed_point_clouds')

    open3d_dbscan_clustering_setting_id = Column(Integer, ForeignKey('Open3D_DBSCAN_Clustering_Settings.id', ondelete="CASCADE"))
    open3d_dbscan_clustering_setting = relationship('Open3DDBSCANClusteringSetting', back_populates='processed_point_clouds')

    platon_dimension_id = Column(Integer, ForeignKey('Platon_Dimensions.id', ondelete="CASCADE"))
    platon_dimension = relationship('PlatonDimension', back_populates='processed_point_clouds')

    __table_args__ = (
        CheckConstraint(file_extension.in_(['ply'])),
        UniqueConstraint(
            'compression_step_id',
            'open3d_segmentation_setting_id',
            'open3d_dbscan_clustering_setting_id',
            'platon_dimension_id',
            name=f'uix_{__tablename__}'
        ),
    )


class ProcessedSTL(Base):
    __tablename__ = 'Processed_STLs'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    file_extension = Column(String)
    file_name = Column(String)
    # filepath = Column(String)

    volume = Column(Float, default=0)
    volume_unit = Column(String, default='mm3')

    compression_step_id = Column(Integer, ForeignKey('Compression_Steps.id', ondelete="CASCADE"))
    compression_step = relationship('CompressionStep', back_populates='stls')

    scaling_factor_id = Column(Integer, ForeignKey('Scaling_Factors.id', ondelete="CASCADE"))
    scaling_factor = relationship('ScalingFactor', back_populates='stls')

    # step also links to frames
    metahsape_build_model_setting_id = Column(Integer, ForeignKey('Metashape_Build_Model_Settings.id', ondelete="CASCADE"))
    metahsape_build_model_setting = relationship('MetashapeBuildModelSetting', back_populates='stls')

    processed_point_cloud_id = Column(Integer, ForeignKey('Processed_Point_Clouds.id', ondelete="CASCADE"))
    processed_point_cloud = relationship('ProcessedPointCloud', back_populates='stls')


# TODO add other artifacts
#   stls - plys - psx meta project - etc


TestComponentModels = [cls for cls in Base.__subclasses__()]
