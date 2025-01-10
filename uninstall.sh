#!/bin/bash

# Remove the executable
sudo rm /usr/local/bin/cytosense_to_ecotaxa_pipeline

# Remove the virtual environment
sudo rm -rf /opt/cytosense_to_ecotaxa_pipeline_venv

echo "Cytosense to EcoTaxa Pipeline uninstalled."
