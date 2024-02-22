import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, \
    ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Sample(Base):
    """
    non-nullable are required by user when entering
    """
    __tablename__ = "Samples"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # geometric - derived from first step in trial
    # technically dont need these here but its convenient
    height_enc = Column(Float)
    #height_stl = Column(Float)  # not in use
    geometry_units = Column(String, nullable=False, default='mm')

    # infill
    cell_size = Column(Float, nullable=False, default=1)
    relative_density = Column(Float, nullable=False, default=0.5)

    # other
    n_perimeters = Column(Integer, nullable=False, default=1)

    print_id = Column(Integer, ForeignKey('Prints.id', ondelete="CASCADE"))
    print = relationship('Print', back_populates='samples')

    # infill_pattern_id = Column(Integer, ForeignKey('Infill_Patterns.id'))
    # infill_pattern = relationship('InfillPattern', back_populates='samples')

    trials = relationship(
        'CompressionTrial',
        back_populates='sample',
        cascade="all, delete",
        passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint('relative_density BETWEEN 0 AND 1', name='relative_density_range_value_check'),
    )

class Phantom(Base):
    """
    non-nullable are required by user when entering
    """
    __tablename__ = "Phantoms"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String, unique=True, default='cylinder')
    
    volume = Column(Float)
    geometry_units = Column(String, nullable=False, default='mm')

    trials = relationship(
        'CompressionTrial',
        back_populates='phantom',
        cascade="all, delete",
        passive_deletes=True
    )



# class InfillPattern(Base):
#     __tablename__ = "Infill_Patterns"
#
#     id = Column(Integer, primary_key=True)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#
#     equation = Column(String, default='x + y + z = 0')
#     cell_size = Column(Float, nullable=False, default=1)
#     relative_density = Column(Float, nullable=False, default=0.5)
#
#     samples = relationship('Sample', back_populates='infill_pattern')
#
#     __table_args__ = (
#         CheckConstraint('relative_density BETWEEN 0 AND 1', name='relative_density_range_value_check'),
#         UniqueConstraint(
#             'equation',
#             'cell_size',
#             'relative_density',
#             name=f'uix_{__tablename__}'
#         ),
#     )


class Print(Base):
    __tablename__ = "Prints"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String, unique=True, nullable=False, default="default")

    filament_name = Column(String, nullable=False)
    printer_model = Column(String, nullable=False)
    printer_settings_file = Column(String, nullable=False)
    stl_file = Column(String, nullable=False, unique=True)

    samples = relationship(
        'Sample',
        back_populates='print',
        cascade="all, delete",
        passive_deletes=True
    )


SampleModels = [cls for cls in Base.__subclasses__()]