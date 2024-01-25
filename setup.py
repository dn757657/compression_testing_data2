from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="compression_testing_data2",  # Required
    version="1.0.0",  # Required
    description="SQL backend for compression testing",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/dn757657/compression_testing_data2",  # Optional
    packages=find_packages(where="models"),  # Required
    py_modules=['main'],
    python_requires=">=3.8, <4",
)