# Install script for Windows (install.ps1)

# Check if running as administrator
if (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
  Write-Error "This script requires administrator privileges. Please run it as administrator."
  exit 1
}

# Install pre-requisites (jq - consider using a package manager like Chocolatey or scoop if available)
#  Handle jq installation appropriately for Windows. This example assumes jq is already available in the PATH
Write-Host "Make sure jq is installed and available in the PATH"

# Create virtual environment
python -m venv $env:LOCALAPPDATA\cytosense_to_ecotaxa_pipeline_venv

# Activate virtual environment
& "$env:LOCALAPPDATA\cytosense_to_ecotaxa_pipeline_venv\Scripts\Activate.ps1"

# Install Python packages within the virtual environment
pip install -r requirements.txt
pip install . # Install the package

# Create installation directory
$installDir = "$env:ProgramFiles\cytosense_to_ecotaxa_pipeline"
New-Item -ItemType Directory -Path $installDir -Force

# Get Python executable path within the virtual environment
$pythonExec = (Get-Command python).Source

# Get site-packages path dynamically
$sitePackagesPath = & python -c "import site; print(site.getsitepackages()[0])"

# Copy files to the installation directory
Copy-Item -Path "$sitePackagesPath\cytosense_to_ecotaxa_pipeline\bin\Cyz2Json.exe" -Destination "$installDir\Cyz2Json.exe"
Copy-Item -Path "$sitePackagesPath\cytosense_to_ecotaxa_pipeline\pipeline.py" -Destination "$installDir\pipeline.py"
Copy-Item -Path "$sitePackagesPath\cytosense_to_ecotaxa_pipeline\main.py" -Destination "$installDir\main.py"



# Create executable wrappers (using batch files for simplicity)
# Cyz2Json.bat
@"
@echo off
"$env:LOCALAPPDATA\cytosense_to_ecotaxa_pipeline_venv\Scripts\python.exe" "$installDir\pipeline.py" %*
"@ | Out-File -Encoding ascii "$installDir\cytosense_to_ecotaxa_pipeline.bat"


# Add installation directory to PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
if (-not ($currentPath -like "*$installDir*")) {
  [Environment]::SetEnvironmentVariable("PATH", "$installDir;$currentPath", "Machine")
  Write-Host "Added '$installDir' to the system PATH.  You may need to restart your PowerShell session or log out and back in for this change to take effect."
}


# Deactivate virtual environment
deactivate

Write-Host "Installation complete."

