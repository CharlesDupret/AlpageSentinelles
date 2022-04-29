import os  # Portable way of using operating system dependent functionality
from setuptools import setup  # to set up of the package

setup(
    name="poi_grabber",
    version="0.0.1",
    description="A data grabber for Sentinel-2 images",
    long_description=open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "DatasetBuilder/src/README.md"
        )
    ).read(),
    long_description_content_type="text/markdown",
    py_modules=["poi_grabber"],
    package_dir={"": "DatasetBuilder"},
    classifiers=[
        "Programming Language :: Python ::3",
        "Programming Language :: Python ::3.6",
        "Programming Language :: Python ::3.7",
        "Programming Language :: Python ::3.8",
    ],
    install_requires=[
        "numpy>=1.21.5",
        "GDAL>=3.0.4",
        "matplotlib>=3.2.2",
        "geopandas>=0.10.2",
        "pandas>=1.3.5",
        "xarray>=0.18.2",
        "scipy>=1.8.0",
        "tqdm",
    ],
    extras_require={
        "dev": ["pytest>=3.7", "black>=7.1.2"],
    },
    author="Charles Dupret",
    author_email="charles.dupret@grenoble-inp.org",
)
