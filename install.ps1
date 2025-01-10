# Determine OS and Architecture (for wheel selection)
$OS = Get-WmiObject Win32_OperatingSystem | Select-Object -ExpandProperty Caption
$ARCH = (Get-WmiObject Win32_Processor).Architecture

# Determine correct wheel file based on architecture (adjust as needed)
switch ($ARCH) {
  "64-bit" { $ARCH_NAME = "windows"; break } # Example for most common architecture
  # Add other architectures if needed
  Default { Write-Host "Unsupported architecture: $ARCH"; exit 1 }
}

# Get latest tag using GitHub API
$LatestTag = (Invoke-RestMethod "https://api.github.com/repos/ecotaxa/cytosense_to_ecotaxa_pipeline/releases/latest").tag_name

if (-not $LatestTag) {
    Write-Host "Error getting latest tag. Exiting."
    exit 1
}


# Construct wheel file name
$WheelFileName = "cytosense_to_ecotaxa_pipeline_${ARCH_NAME}-${LatestTag}-py3-none-any.whl"

# Construct download URL
$WheelUrl = "https://github.com/ecotaxa/cytosense_to_ecotaxa_pipeline/releases/download/${LatestTag}/${WheelFileName}"

# Download wheel file 
$WheelFile = "$PSScriptRoot\$WheelFileName" # Save to same directory as the script
Invoke-WebRequest -Uri $WheelUrl -OutFile $WheelFile


if (-not (Test-Path $WheelFile)) {
    Write-Host "Error downloading wheel file. Exiting."
    exit 1
}

# Install wheel using pip
# Check if venv exists - create if does not exist
$Venv = "C:\Users\sebastiengalvagno\AppData\Local\Programs\Python\Python310\python.exe"
if (-not (Test-Path "$Venv")) {
   # Path does not exist - assuming we have not created a venv
   Write-Host "Creating virtual environment"
   & $Venv -m venv .venv
}

# Now activate venv and install package
.venv\Scripts\activate
& $Venv -m pip install $WheelFile

# ... any further Windows-specific installation steps (e.g., creating shortcuts)

# Example of creating a simple batch script to run your Python entry point (optional)
$BatchScriptContent = @"
@echo off
.venv\Scripts\activate
python your_main_script.py %* 
deactivate
"@
$BatchScriptContent | Out-File -FilePath "run_cytosense_to_ecotaxa_pipeline.bat" -Encoding ascii

Write-Host "Installation complete."


