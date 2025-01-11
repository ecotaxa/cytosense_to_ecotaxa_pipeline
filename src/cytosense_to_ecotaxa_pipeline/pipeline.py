import os
import subprocess
import sys
from pathlib import Path
import importlib.util

def get_cyz2json_path():
    """Get the platform-specific path to cyz2json binary"""
    # Get the directory where the package is installed
    package_dir = Path(__file__).parent
    bin_dir = package_dir / "bin"
    
    # Check for platform-specific binary name
    if sys.platform == "win32":
        binary_name = "cyz2Json.exe"
    else:
        binary_name = "cyz2Json"
    
    binary_path = bin_dir / binary_name
    if not binary_path.exists():
        raise FileNotFoundError(f"Could not find cyz2json binary at {binary_path}")
    
    # Ensure the binary is executable on Unix-like systems
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
    
    # Import and run main
    try:
        from . import main
        main.process_file(str(json_file))
    except ImportError:
        print("Error: Could not import main module", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
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