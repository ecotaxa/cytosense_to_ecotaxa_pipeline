

from setuptools import setup, find_packages

setup(
    name="cytosense_to_ecotaxa_pipeline",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cytosense_to_ecotaxa_pipeline=cytosense_to_ecotaxa_pipeline.main:main',
        ],
    },
    install_requires=[
        'six',
        'matplotlib',
    ],
    python_requires='>=3.5'
)
