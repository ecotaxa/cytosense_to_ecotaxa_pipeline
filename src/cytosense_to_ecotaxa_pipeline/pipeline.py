import os
import subprocess
import sys
from pathlib import Path
import json
import shutil

def get_cyz2json_path():
    """Get the platform-specific path to cyz2json binary"""
    package_dir = Path(__file__).parent
    bin_dir = package_dir / "bin"
    
    binary_name = "cyz2Json.exe" if sys.platform == "win32" else "cyz2Json"
    binary_path = bin_dir / binary_name
    
    if not binary_path.exists():
        raise FileNotFoundError(f"Could not find cyz2json binary at {binary_path}")
    
    if sys.platform != "win32":
        binary_path.chmod(0o755)
    
    return str(binary_path)

def run_cyz2json(input_file):
    """
    Run the cyz2json binary on the input file
    
    Args:
        input_file (Path): Path to the input .cyz file
    Returns:
        Path: Path to the output JSON file
    """
    output_file = input_file.with_suffix('.json')
    cyz2json_path = get_cyz2json_path()
    
    try:
        subprocess.run([cyz2json_path, str(input_file), '--output', str(output_file)], 
                      check=True,
                      stderr=subprocess.PIPE,
                      universal_newlines=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error running cyz2json: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def create_default_extra_data(input_file):
    """
    Create a default extra_data.json file if none exists
    
    Args:
        input_file (Path): Path to the input .cyz file
    Returns:
        Path: Path to the extra data JSON file
    """
    extra_data = {
        "cruise": "",
        "ship": "",
        "station": "",
        "bottle": "",
        "latitude": "",
        "longitude": "",
        "depth": ""
    }
    
    extra_data_file = input_file.with_name('extra_data.json')
    if not extra_data_file.exists():
        with open(extra_data_file, 'w') as f:
            json.dump(extra_data, f, indent=2)
        print(f"Created default extra_data.json at {extra_data_file}")
        print("Please edit this file with your metadata before processing.")
        sys.exit(0)
    
    return extra_data_file

def process_file(input_file):
    """
    Process a cytosense file through cyz2json and main.py
    
    Args:
        input_file (str): Path to the input .cyz file
    """
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.cyz':
        print("Error: Input file must have .cyz extension", file=sys.stderr)
        sys.exit(1)
    
    # Convert cyz to json
    json_file = run_cyz2json(input_path)
    
    # Get or create extra_data.json
    extra_data_file = create_default_extra_data(input_path)
    
    # Run main.py from the virtual environment
    venv_python = Path(sys.executable).parent
    main_script = venv_python / 'main.py'
    
    if not main_script.exists():
        print(f"Error: main.py not found in {venv_python}", file=sys.stderr)
        sys.exit(1)
    
    try:
        subprocess.run([sys.executable, str(main_script), str(json_file), '--extra', str(extra_data_file)],
                      check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running main.py: {e}", file=sys.stderr)
        sys.exit(1)

def main_cli():
    """Command line interface entry point"""
    if len(sys.argv) != 2:
        print("Usage: cytosense_to_ecotaxa_pipeline <input_cyz_file>")
        sys.exit(1)
    
    process_file(sys.argv[1])

if __name__ == "__main__":
    main_cli()