#!/bin/bash

# Create system-wide virtual environment
sudo python -m venv /opt/cytosense_to_ecotaxa_pipeline_venv

# Install from requirements
sudo /opt/cytosense_to_ecotaxa_pipeline_venv/bin/pip install -r requirements.txt

# Install execution script
sudo tee /usr/local/bin/cytosense_to_ecotaxa_pipeline << 'EOF'
#!/bin/bash
source /opt/cytosense_to_ecotaxa_pipeline_venv/bin/activate
python /opt/cytosense_to_ecotaxa_pipeline_venv/bin/main.py "$@"
deactivate
EOF

sudo chmod +x /usr/local/bin/cytosense_to_ecotaxa_pipeline

