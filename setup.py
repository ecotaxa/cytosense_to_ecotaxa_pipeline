

from setuptools import setup, find_packages
import os

platform = os.getenv('PLATFORM', 'unknown')
version = os.environ.get('GITHUB_REF_NAME', 'v1.1.0').replace('v', '')

setup(
    name=f'cytosense_to_ecotaxa_pipeline-{platform}',
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"}, 
    package_data={
        # 'cytosense_to_ecotaxa_pipeline': ['bin/cyz2json*'],  # Include all cyz2json binaries
        'cytosense_to_ecotaxa_pipeline': ['bin/*'],

    },
    include_package_data=True,  # Ensure package_data is included
    entry_points={
        'console_scripts': [
            'cytosense-to-ecotaxa=cytosense_to_ecotaxa_pipeline.main:cli_main',

        ],
    },
    install_requires=[
        'six',
        'matplotlib',
        'numpy',
        'pillow',
    ],
    python_requires='>=3.6',
    author="Sébastien Galvagno",
    author_email="dev@galvagno.info",
    description="A pipeline tool to convert Cytosense data files to EcoTaxa compatible format."
)
