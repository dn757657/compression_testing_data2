import datetime
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, Float, DateTime, UniqueConstraint, \
    Boolean, CheckConstraint, String
from .base import Base


class MetashapePlyGenerationSetting(Base):
    __tablename__ = 'Metashape_PLY_Generation_Settings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    image_alignment_accuracy = Column(Integer, default=1)
    depth_map_quality = Column(Integer, default=2)
    filter_mode = Column(Integer, default=0)

    full_point_clouds = relationship(
        'FullPointCloud',
        back_populates='metashape_ply_generation_setting',
        cascade="all, delete",
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint(
            'image_alignment_accuracy',
            'depth_map_quality',
            'filter_mode',
            name=f'uix_{__tablename__}'
        ),
    )


class MetashapePlyExportSetting(Base):
    __tablename__ = 'Metashape_PLY_Export_Settings'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    save_point_color = Column(Boolean, default=True)
    save_point_normal = Column(Boolean, default=True)
    save_point_intensity = Column(Boolean, default=True)
    save_point_classification = Column(Boolean, default=True)
    save_point_confidence = Column(Boolean, default=True)
    save_point_return_number = Column(Boolean, default=True)
    save_point_scan_angle = Column(Boolean, default=True)
    save_point_source_id = Column(Boolean, default=True)
    save_point_timestamp = Column(Boolean, default=True)
    save_point_index = Column(Boolean, default=True)

    full_point_clouds = relationship(
        'FullPointCloud',
        back_populates='metashape_ply_export_setting',
        cascade="all, delete",
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint(
            'save_point_color',
            'save_point_normal',
            'save_point_intensity',
            'save_point_classification',
            'save_point_confidence',
            'save_point_return_number',
            'save_point_scan_angle',
            'save_point_source_id',
            'save_point_timestamp',
            'save_point_index',
            name=f'uix_{__tablename__}'
        ),
    )


class Open3DSegmentationSetting(Base):
    __tablename__ = 'Open3D_Segmentation_Settings'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    plane_limit = Column(Integer, default=10)
    distance_threshold = Column(Float, default=0.01)
    ransac_n = Column(Integer, default=3)
    num_iterations = Column(Integer, default=1000)

    processed_point_clouds = relationship(
        'ProcessedPointCloud',
        back_populates='open3d_segmentation_setting',
        cascade="all, delete",
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint(
            'plane_limit',
            'distance_threshold',
            'ransac_n',
            'plane_limit',
            name=f'uix_{__tablename__}'
        ),
    )


class MetashapeBuildModelSetting(Base):
    __tablename__ = 'Metashape_Build_Model_Settings'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    surface_type = Column(Integer, default=0)
    interpolation = Column(Float, default=1)
    face_count = Column(Integer, default=2)
    source_data = Column(Integer, default=0)

    stls = relationship(
        'ProcessedSTL',
        back_populates='metahsape_build_model_setting',
        cascade="all, delete",
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint(
            'surface_type',
            'interpolation',
            'face_count',
            'source_data',
            name=f'uix_{__tablename__}'
        ),
    )


class ColorDefinition(Base):
    __tablename__ = 'Color_Definitions'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    red_mean_val = Column(Float)
    green_mean_val = Column(Float)
    blue_mean_val = Column(Float)

    red_mean_stdv = Column(Float)
    green_mean_stdv = Column(Float)
    blue_mean_stdv = Column(Float)

    standard_dev_range = Column(Integer)
    color = Column(String(20))

    __table_args__ = (
        CheckConstraint('red_mean_val BETWEEN 0 AND 255', name='red_range_value_check'),
        CheckConstraint('green_mean_val BETWEEN 0 AND 255', name='green_range_value_check'),
        CheckConstraint('blue_mean_val BETWEEN 0 AND 255', name='blue_range_value_check'),
        CheckConstraint('standard_dev_range BETWEEN 0 AND 5', name='stdev_range_value_check'),
        UniqueConstraint(
            'red_mean_val',
            'green_mean_val',
            'blue_mean_val',
            'color',
            name=f'uix_{__tablename__}'
        ),
    )


class Open3DDBSCANClusteringSetting(Base):
    __tablename__ = 'Open3D_DBSCAN_Clustering_Settings'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    eps = Column(Float, default=0.05)
    min_points = Column(Integer, default=1000)

    processed_point_clouds = relationship(
        'ProcessedPointCloud',
        back_populates='open3d_dbscan_clustering_setting',
        cascade="all, delete",
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint(
            'eps',
            'min_points',
            name=f'uix_{__tablename__}'
        ),
    )


ProcessingModels = [
    MetashapePlyGenerationSetting,
    MetashapePlyExportSetting,
    Open3DDBSCANClusteringSetting,
    Open3DSegmentationSetting,
    ColorDefinition,    
]

