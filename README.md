# Cytosense to EcoTaxa Pipeline

<img src="https://github.com/ecotaxa/cytosense_to_ecotaxa_pipeline/actions/workflows/build.yml/badge.svg" alt="Build cytosense_to_ecotaxa_pipeline"/>


A pipeline tool to convert Cytosense data files to EcoTaxa compatible format.
## Features

- Automated conversion from Cytosense (.cyz) to EcoTaxa format
- Built-in cyz2json binary for data extraction
- Cross-platform support (Linux, Windows, MacOS)
- System-wide installation

## Installation

### Installation from Github

```bash
sudo ./install.sh --github
```

### Installation from local files

```bash
sudo ./install.sh
```

on Windows use install.ps1 instead of install.sh


to remove or put in cyz2json
### On MacOSX
manual build
to bypass security with xattr command, then need to go in Systems Settings > Security & Privacy > General and allow the app to be opened for the 10+ libraries. (need to relauch sevaral time the cyz2json binary)

xattr -d com.apple.quarantine  /Users/sebastiengalvagno/Downloads/cytosense_to_ecotaxa_pipeline_macos-0.0.24/cytosense_to_ecotaxa_pipeline/bin/*


# Run the pipeline

```bash
/usr/local/bin/cytosense_to_ecotaxa_pipeline Deployment\ 1\ 2024-07-18\ 21h12.cyz --output Deployment\ 1\ 2024-07-18\ 21h12.json
```

# Uninstall

```bash
sudo ./uninstall.sh
```

on Windows use uninstall.ps1 instead of uninstall.sh

