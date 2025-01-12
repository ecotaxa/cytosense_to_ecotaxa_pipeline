import os
import subprocess
import sys
from pathlib import Path
import json

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

def create_default_extra_data(input_path):
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
    
    extra_file = input_path.parent / 'extra_data.json'
    if not extra_file.exists():
        with open(extra_file, 'w') as f:
            json.dump(extra_data, f, indent=2)
        print(f"Created default extra_data.json at {extra_file}")
        print("Please edit this file with your metadata before processing.")
        sys.exit(0)
    
    return extra_file

def process_file(input_file):
    """
    Process a cytosense file through cyz2json and main.py
    
    Args:
        input_file (str): Path to the input .cyz file
    """
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.cyz':
        print("Error: Input file must have .cyz extension")
        sys.exit(1)
    
    # Get paths
    json_output = input_path.with_suffix('.json')
    extra_data = create_default_extra_data(input_path)
    cyz2json = get_cyz2json_path()
    
    # Convert .cyz to .json
    print(f"Converting {input_path.name} to JSON...")
    try:
        subprocess.run([cyz2json, str(input_path), '--output', str(json_output)], 
                      check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running cyz2json: {e}")
        sys.exit(1)
    
    # Run main.py with the generated JSON
    print("Processing with main.py...")
    try:
        main_script = Path('/opt/cytosense_to_ecotaxa_pipeline_venv/bin/main.py')
        python_exe = Path(sys.executable)
        
        subprocess.run([
            str(python_exe),
            str(main_script),
            str(json_output),
            '--extra',
            str(extra_data)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running main.py: {e}")
        sys.exit(1)

def main_cli():
    """Command line interface entry point"""
    if len(sys.argv) != 2:
        print("Usage: cytosense_to_ecotaxa_pipeline <input_cyz_file>")
        sys.exit(1)
    
    process_file(sys.argv[1])

if __name__ == "__main__":
    main_cli()