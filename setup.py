

from setuptools import setup, find_packages
import os

version = os.environ.get('GITHUB_REF_NAME', 'v1.0.0').replace('v', '')

setup(
    name="cytosense_to_ecotaxa_pipeline",
    version=version,
    packages=find_packages(),
    package_data={
        # 'cytosense_to_ecotaxa_pipeline': ['bin/cyz2json*'],  # Include all cyz2json binaries
        'cytosense_to_ecotaxa_pipeline': ['bin/*'],

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
