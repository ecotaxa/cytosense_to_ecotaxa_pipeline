#!/bin/bash

# Determine OS and Architecture
OS=$(uname -s)
ARCH=$(uname -m)

# Determine correct wheel file based on OS
case "$OS" in
  Darwin)
    OS_NAME="macos"
    ;;
  Linux)
    OS_NAME="ubuntu"  # Or determine the specific distro if needed
    ;;
  *)
    echo "Unsupported operating system: $OS"
    exit 1
    ;;
esac

# Get latest tag using GitHub API
LATEST_TAG=$(curl -s "https://api.github.com/repos/ecotaxa/cytosense_to_ecotaxa_pipeline/releases/latest" | jq -r '.tag_name')

if [[ -z "$LATEST_TAG" ]]; then
  echo "Error getting latest tag. Exiting."
  exit 1
fi

# Remove the "v" prefix if it exists
TAG_WITHOUT_V="${LATEST_TAG#v}" # This is parameter expansion to remove the leading "v"


# Check for --github flag
if [[ "$1" == "--github" ]]; then


  WHEEL_FILE_NAME="cytosense_to_ecotaxa_pipeline_${OS_NAME}-${TAG_WITHOUT_V}-py3-none-any.whl"
  WHEEL_URL="https://github.com/ecotaxa/cytosense_to_ecotaxa_pipeline/releases/download/${LATEST_TAG}/${WHEEL_FILE_NAME}"

echo "Latest tag: $LATEST_TAG"
echo "Tag without 'v': $TAG_WITHOUT_V"
echo "Wheel file name: $WHEEL_FILE_NAME"
echo "Wheel URL: $WHEEL_URL"
echo "debug    : https://github.com/ecotaxa/cytosense_to_ecotaxa_pipeline/releases/download/v0.0.24/cytosense_to_ecotaxa_pipeline_macos-0.0.24-py3-none-any.whl"

echo curl -s -L "$WHEEL_URL" -o "/tmp/$(basename "$WHEEL_URL")"

#   WHEEL_FILE=$(curl -s -L "$WHEEL_URL" -o "/tmp/$(basename "$WHEEL_URL")")
  # Download the file and store the *path* in WHEEL_FILE
  WHEEL_FILE="/tmp/$(basename "$WHEEL_URL")"  # Construct the full path
  curl -s -L "$WHEEL_URL" -o "$WHEEL_FILE"    # Download to the specified path
  echo "Downloaded wheel file: $WHEEL_FILE"

  if [[ -f "$WHEEL_FILE" ]]; then
    echo "Downloaded wheel file from GitHub: $WHEEL_FILE"

    # Check if running on macOS
    if [[ $(uname) == "Darwin" ]]; then
        if [[ -d "/Users/sebastiengalvagno/Downloads" && -f "/Users/sebastiengalvagno/Downloads/cytosense_to_ecotaxa_pipeline_${OS_NAME}-${TAG_WITHOUT_V}-py3-none-any.whl" ]] ; then
            xattr -d com.apple.quarantine /Users/sebastiengalvagno/Downloads/cytosense_to_ecotaxa_pipeline_${OS_NAME}-${TAG_WITHOUT_V}-py3-none-any.whl
            echo "Removed quarantine attribute on macOS."
        elif [[ -f "cytosense_to_ecotaxa_pipeline_${OS_NAME}-${TAG_WITHOUT_V}-py3-none-any.whl" ]]; then  #Local build
                xattr -d com.apple.quarantine cytosense_to_ecotaxa_pipeline_${OS_NAME}-${TAG_WITHOUT_V}-py3-none-any.whl
                echo "Removed quarantine attribute on macOS from local directory."
        fi
    fi

  else
    echo "Error downloading wheel file from GitHub. Exiting."
    exit 1
  fi

elif [[ "$1" == "--local" || -z "$1" ]]; then
  # Install from local dist directory
  WHEEL_FILE=$(ls dist/*.whl)

    # Check if running on macOS (place this *after* getting the wheel file)
    if [[ $(uname) == "Darwin" ]]; then
        if [[ -f "$WHEEL_FILE" ]]; then  #Local build
                xattr -d com.apple.quarantine "$WHEEL_FILE"
                echo "Removed quarantine attribute on macOS from local directory."
        fi
    fi


  # Check if WHEEL_FILE is empty
  if [[ -z "$WHEEL_FILE" ]]; then
    echo "No wheel file found in dist/. Exiting."
    exit 1
  fi
else
  echo "Invalid argument. Use --github or --local."
  exit 1
fi


# Create system-wide virtual environment
sudo python3 -m venv /opt/cytosense_to_ecotaxa_pipeline_venv

# Install the wheel
sudo /opt/cytosense_to_ecotaxa_pipeline_venv/bin/pip install "$WHEEL_FILE"



# Install execution script
sudo tee /usr/local/bin/cytosense_to_ecotaxa_pipeline << 'EOF'
#!/bin/bash
source /opt/cytosense_to_ecotaxa_pipeline_venv/bin/activate
python /opt/cytosense_to_ecotaxa_pipeline_venv/bin/main.py "$@"
deactivate
EOF

sudo chmod +x /usr/local/bin/cytosense_to_ecotaxa_pipeline

