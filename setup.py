

from setuptools import setup, find_packages

setup(
    name="cytosense_to_ecotaxa_pipeline",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        'cytosense_to_ecotaxa_pipeline': ['bin/cyz2json*'],  # Include all cyz2json binaries
    },
    include_package_data=True,  # Ensure package_data is included
    entry_points={
        'console_scripts': [
            'cytosense_to_ecotaxa_pipeline=cytosense_to_ecotaxa_pipeline.main:main',
        ],
    },
    install_requires=[
        'six',
        'matplotlib',
    ],
    python_requires='>=3.6'
)
