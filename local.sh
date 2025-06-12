#!/bin/bash


WHEEL_URL="https://github.com/ecotaxa/cytosense_to_ecotaxa_pipeline/releases/download/v1.0.0/cytosense_to_ecotaxa_pipeline-1.0.0-py3-none-linux_x86_64.whl"
WHEEL_FILE="cytosense_to_ecotaxa_pipeline-1.0.0-py3-none-linux_x86_64.whl"
curl -L -O $WHEEL_URL -o $WHEEL_FILE



sudo python3 -m venv /opt/cytosense_to_ecotaxa_pipeline_venv
sudo chmod +x /opt/cytosense_to_ecotaxa_pipeline_venv/bin/*
source /opt/cytosense_to_ecotaxa_pipeline_venv/bin/activate
PYTHON_EXECUTABLE=$(which python)
PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
SITE_PACKAGES_PATH=$(python -c "import site; print(site.getsitepackages()[0])")

sudo /opt/cytosense_to_ecotaxa_pipeline_venv/bin/pip install "$WHEEL_FILE" 


sudo ln -s "$SITE_PACKAGES_PATH/cytosense_to_ecotaxa_pipeline/bin/Cyz2Json" /opt/cytosense_to_ecotaxa_pipeline_venv/bin/Cyz2Json
sudo ln -s "$SITE_PACKAGES_PATH/cytosense_to_ecotaxa_pipeline/pipeline.py" /opt/cytosense_to_ecotaxa_pipeline_venv/bin/pipeline.py
sudo ln -s "$SITE_PACKAGES_PATH/cytosense_to_ecotaxa_pipeline/convert.py" /opt/cytosense_to_ecotaxa_pipeline_venv/bin/convert.py
sudo ln -s "$SITE_PACKAGES_PATH/cytosense_to_ecotaxa_pipeline/main.py" /opt/cytosense_to_ecotaxa_pipeline_venv/bin/main.py

export LD_LIBRARY_PATH=/opt/cytosense_to_ecotaxa_pipeline_venv/lib/python${PYTHON_VERSION}/site-packages/cytosense_to_ecotaxa_pipeline/lib:${LD_LIBRARY_PATH}

sudo chmod ago+x /opt/cytosense_to_ecotaxa_pipeline_venv/lib/python${PYTHON_VERSION}/site-packages/cytosense_to_ecotaxa_pipeline/bin/*

desactivate


sudo tee /usr/local/bin/cytosense_to_ecotaxa_pipeline << 'EOF'
#!/bin/bash
source /opt/cytosense_to_ecotaxa_pipeline_venv/bin/activate
python /opt/cytosense_to_ecotaxa_pipeline_venv/bin/pipeline.py "$@"
deactivate
EOF

sudo chmod +x /usr/local/bin/cytosense_to_ecotaxa_pipeline

rm $WHEEL_FILE



echo "Installation completed successfully!"
exit 0

