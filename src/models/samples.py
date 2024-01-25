import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, \
    ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Sample(Base):
    __tablename__ = "Samples"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # geometric
    height = Column(Float)
    units = Column(String, nullable=False, default='mm')

    # infill
    cell_size = Column(Float, nullable=False, default=1)
    relative_density = Column(Float, nullable=False, default=0.5)

    # other
    n_perimeters = Column(Integer, nullable=False, default=1)

    print_id = Column(Integer, ForeignKey('Prints.id'))
    print = relationship('Print', back_populates='samples')

    # infill_pattern_id = Column(Integer, ForeignKey('Infill_Patterns.id'))
    # infill_pattern = relationship('InfillPattern', back_populates='samples')

    trials = relationship('CompressionTrial', back_populates='sample')

    __table_args__ = (
        CheckConstraint('relative_density BETWEEN 0 AND 1', name='relative_density_range_value_check'),
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

    samples = relationship('Sample', back_populates='print')


SampleModels = [cls for cls in Base.__subclasses__()]