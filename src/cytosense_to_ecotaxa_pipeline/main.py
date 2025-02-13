import json
import os
import base64
import csv
import argparse
from datetime import datetime
import shutil
import sys
from zipfile import ZipFile
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


bioODVHeader=False

def remove_extension(value):
    """
    Function to remove the extension name from a file name.
    """
    if value and isinstance(value, str):
        return os.path.splitext(value)[0]
    return value

# Transformation pour les dates
# def transform_date(value):
#     if value and isinstance(value, str):
#         try:
#             return datetime.fromisoformat(value).strftime("%Y-%m-%d")
#         except ValueError:
#             return value  # Retourne la valeur brute si elle n'est pas au bon format
#     return value

# def transform_time(value):
#     if value and isinstance(value, str):
#         try:
#             return datetime.fromisoformat(value).strftime("%H:%M:%S")
#         except ValueError:
#             return value  # Retourne la valeur brute si elle n'est pas au bon format
#     return value

def extract_date_utc(iso_datetime):
    """
    Extrait la date au format YYYYMMDD UTC à partir d'une chaîne ISO 8601.
    Convert an ISO 8601 datetime string to YYYYMMDD UTC format.
    """
    try:
        dt = datetime.fromisoformat(iso_datetime.rstrip("Z")).astimezone()  # Conversion vers UTC
        return dt.strftime("%Y%m%d UTC")
    except ValueError:
        return "INVALID_DATE"

def extract_time_utc(iso_datetime):
    """
    Extrait l'heure au format HHMMSS UTC à partir d'une chaîne ISO 8601.
    Convert an ISO 8601 datetime string to HHMMSS UTC format.
    """
    try:
        dt = datetime.fromisoformat(iso_datetime.rstrip("Z")).astimezone()  # Conversion vers UTC
        return dt.strftime("%H%M%S UTC")
    except ValueError:
        return "INVALID_TIME"


# def search_Pulse_Shapes(value, description):
#     return next((item for item in value if item['description'] == description), None)

# def search_FWS(value):
#     result = search_Pulse_Shapes(value, "FWS")
#     return result["values"]

def search_pulse_shapes(description):
    """
    Then in your mapping you can use it like:
    {"name": "pulseShape_FWS", "type": "[t]", "transform": search_pulse_shapes("FWS")}
    """
    def search(value):
        result = next((item for item in value if item['description'] == description), None)
        if result:
            return result["values"]
        return None
    return search

def search_pulse_shapes2(description, value):
    """
    Search in pulse value the section associated to description 
    and return its values
    """
    result = next((item for item in value if item['description'] == description), None)
    if result:
        return result["values"]
    return None



def image_particle(particle_data):
    max_y = len(particle_data)
    max_x = 50

    a = np.zeros((max_y, max_x), dtype=np.uint8)

    y = 0
    for pulse_shape in particle_data:
        x = 0
        print(len(particle_data))

        for value in particle_data:
            if x >= max_x:
                break

            a[y, x] = value
            x = x + 1

        y = y + 1
    return a

def draw_pulse_shape_old(pulse_data,description,image_path):

    data = search_pulse_shapes2(description, pulse_data)

    a = image_particle(data)
    # Normalize to 0-1
    a = (a - np.min(a)) / (np.max(a) - np.min(a))

    a = a * (256 * 256 * 256 - 1)

    red = a // (256**2)
    green = (a // 256) % 256
    blue = a % 256

    rgb_image_array = np.stack((red, green, blue), axis=-1)

    # Convert the 3D array into an image using Pillow
    image = Image.fromarray(np.uint8(rgb_image_array))
    image.save(image_path)



def normalize_data(values):
    """Normalizes data to the range [0, 1] using min-max scaling."""
    return (values - np.min(values)) / (np.max(values) - np.min(values))

def draw_pulse_shape(pulse_data, description, image_path, normalize= True):
    """
    Draws a pulse shape image from pulse data and saves it.

    Args:
        pulse_data (list): List of pulse shape dictionaries.
        description (str): Description of the pulse shape to draw (e.g., "FWS").
        image_path (str): Path to save the image.
    """
    values = next((pulse["values"] for pulse in pulse_data if pulse["description"] == description), None)

    if values is None:
        print(f"Warning: No pulse shape found with description '{description}'. Skipping image creation.")
        return 
    
    if normalize:
        values = normalize_data(values) # Normalize if requested

    x = range(len(values))

    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size as needed
    ax.plot(x, values, marker="o", linestyle="-", ms=0.1)  # Keep marker size small
    ax.set_title(f"{description}")
    ax.set_xlabel("Time")  # Add axis labels
    ax.set_ylabel("Value")

    plt.tight_layout()
    # plt.show()
    plt.tight_layout()
    plt.savefig(image_path)  # Save the figure to the specified path
    plt.close(fig)  # Close the figure to free up resources




# def draw_pulse_shape__(pulse_data, description, image_path):
#     """
#     Draws a pulse shape image from pulse data and saves it.

#     Args:
#         pulse_data (list): List of pulse shape dictionaries.
#         description (str): Description of the pulse shape to draw (e.g., "FWS").
#         image_path (str): Path to save the image.
#     """
#     values = next((pulse["values"] for pulse in pulse_data if pulse["description"] == description), None)

#     if values is None:
#         print(f"Warning: No pulse shape found with description '{description}'. Skipping image creation.")
#         return  # Or raise an exception if this is an error condition.

#     max_x = len(values)  # Dynamic width based on pulse data
#     max_y = 1 # Constant height now

#     a = np.zeros((max_y, max_x), dtype=np.float32)
#     a[0, :] = values  # Populate the array with pulse data


#     # Normalize to 0-255 for 8-bit image
#     a = ((a - np.min(a)) / (np.max(a) - np.min(a)) * 255).astype(np.uint8)


#     # Create the grayscale image using Pillow
#     image = Image.fromarray(a, mode="L") # 'L' mode for grayscale.
#     image.save(image_path)



# def add_pulse_shapes(description):
#     """
#     Then in your mapping you can use it like:
#     {"name": "pulseShape_FWS", "type": "[t]", "transform": add_pulse_shapes("FWS")}
#     """
#     def add(value):
#         result = next((item for item in value if item['description'] == description), None)
#         if result:
#             result["values"].append(0)

#         draw_pulse_shape(value, path)
#         return value
#     return add



def format_value(value):
    """
    Formate une valeur avec un seul jeu de guillemets pour les chaînes de texte
    Clean the value, only one pair of quotes for text strings
    """
    # print("format_value:",value)
    if isinstance(value, str):
        cleaned_value = value.strip('"')  # Remove the double quote around the data
        return f'"{cleaned_value}"'
    return str(value)  # Retourne les autres types sous forme de chaîne

def summarize_pulse_numpy(pulse_data_list, n_poly=10):
    """
    Summarizes a pulse shape using polynomial fitting with NumPy.

    Args:
        #pulse_data (np.ndarray): 1D NumPy array containing the pulse data.
        pulse_data (List): array containing the pulse data.
        n_poly (int): Degree of the polynomial fit.

    Returns:
        # np.ndarray: 1D NumPy array containing the polynomial coefficients.
        List: array containing the polynomial coefficients.
    """
    pulse_data = np.array(pulse_data_list)
    n = len(pulse_data)
    x = np.linspace(1, n, n)  # Create x-values for the fit
    poly = np.polynomial.polynomial.Polynomial.fit(x, pulse_data, deg=n_poly - 1)
    coefficients = poly.convert().coef
    return coefficients.tolist()


def transform_column_name(name):
    """
    Function pour transform dynamicately the column name
"""
    return name.replace(".", "_").replace(" ", "_")

def gen_bioODV_header_from_extra(mapping, headers):
    print("BioODV header generating from extra data")
    for key, value in mapping.items():
        # print(f"bioODV {key} {value}")
        if 'object' in value and 'units' in value:
            row=f"<subject>{key}</subject>"
            row+=f"<object>{value['object']}</object>"
            row+=f"<units>{value['units']}</units>"
            headers.append(row)
    return headers
    pass

def gen_bioODV_header_from_mapping(mapping,headers):
    print("BioODV header generating from mapping")
    for key, value in mapping.items():
        # print(f"bioODV {key} {value}")
        if 'bioodv' in value:
            row=f"<subject>{value['name']}</subject>"
            row+=f"<object>{value['bioodv']['object']}</object>"
            row+=f"<units>{value['bioodv']['units']}</units>"
            headers.append(row)
    return headers


def make_row(particle, data, image_file, img_rank, column_mapping, extra_data, polynomial_fits=[]):
    row = [image_file, img_rank]  # img_file_name
    for value in extra_data.values():
        row.append(format_value(value['value']))

    for key, mapping in column_mapping.items():
        # print("Key:", key)
        # print("Mapping:", mapping)

        if "name" not in mapping or mapping["name"] is None:
            continue  # Ignore column with undefined name

        try:
            if "." in key:
                # print(f"Key: {key}, Value: {data.get(key, None)}")
                key_parts = key.split(".")
                # print(f"Key parts: {key_parts}")
            #     value = data.get(key_parts[0], {}).get(key_parts[1], None)
            #     print(f"Key parts: {key_parts}, Value: {value}")
            # else:
            #     value = data.get(key, None)
        
                # current_obj = particle  # Start from the particle object
                current_obj = data  # Start from the particle object
                for part in key_parts:
                    # print(f"Current part: {part}")
                    star = part.split("*")
                    bracket = part.split("[")
                    if len(star)>1: part = star[0]
                    if len(bracket)>1: 
                        part = bracket[0]
                        # print(f"Bracket: part: {part}")
                        if part == "particles":
                            current_obj = particle
                            # print("Particles -> " , current_obj)
                        # current_obj = part
                    else:
                        current_obj = current_obj.get(part, {})
                        # if part == "pulseShapes":
                            # print("PulseShapes -> " , current_obj)
                    # print(f"Current object: {current_obj}")



                value = current_obj if current_obj != {} else None
            else:
                value = particle.get(key, None)


            if mapping["transform"]:
                value = mapping["transform"](value)
                # print(f"Transformed value: {value}")

            row.append(format_value(value))
        except Exception as e:
            row.append("ERROR")

    return row



def main(input_json, extra_data_file):
    # Loading the JSON files

    print("open:", input_json)
    print("extra:", extra_data_file)

    try:
        with open(input_json, "r") as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(f"Invalid JSON format in {input_json}")
        print("Error details:", str(e))
        print(f"Please check your cyz.json file.")
        sys.exit(1)

    try:
        with open(extra_data_file, "r") as f:
            extra_data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(f"Invalid JSON format in {extra_data_file}")
        print("Error details:", str(e))
        print("Please check for trailing commas or other JSON syntax errors")
        sys.exit(1)

    working_dir = os.getcwd()
    # output_images_dir = "images"
    output_images_dir = os.path.join(working_dir, "images")
    print("output_images_dir:", output_images_dir)
    if os.path.exists(output_images_dir):
        shutil.rmtree(output_images_dir)    
    os.makedirs(output_images_dir, exist_ok=True)
    output_tsv = os.path.join(output_images_dir, "ecotaxa_output.tsv")
    # output_tsv = os.path.abspath(output_tsv)# make absolute path
    log_file = os.path.join(output_images_dir, "log.json")
    log_file = os.path.abspath(log_file) # make absolute path

    """
    Mapping dictionnary
    key is the json key
    value is an object to define how to store and transform the data for ecotaxa
        name: is the name of the column in ecotaxa
        type: is the type of the column in ecotaxa
        transform: is a function to transform the value before storing it, you can use a lambda function or a function to transform the value
        bioodv: the bioODV object
          bioodv.subject: is tsv column name [NOT NEEDED] = value.name
          bioodv.object: is the SDN name
          bioodv.units: is the SDN units
    """
    # column_mapping = {
    #     "filename": {"name": "sample_id", "type": "[t]", "transform": remove_extension},
    #     "nb_images": {"name": "img_rank", "type": "[f]", "transform": lambda _: 1},
    #     "instrument.name": {"name": "instrument", "type": "[t]", "transform": None},
    #     "instrument.serialNumber": {"name": "serialnumber", "type": "[t]", "transform": None},
    # }

    column_mapping = {
    "filename": {"name": "sample_id", "type": "[t]", "transform": remove_extension},
    "particleId": {"name": "object_id", "type": "[f]", "transform": None},
    # "hasImage": {"name": "has_image", "type": "[t]", "transform": lambda v: "true" if v else "false"},
    "hasImage": {},

    # "instrument.name": {"name": "instrument", "type": "[t]", "transform": None},
    # "instrument.serialNumber": {"name": "serialnumber", "type": "[t]", "transform": None},

    "instrument.name": {"name": "acq_name", "type": "[t]", "transform": None},
    "instrument.serialNumber": {"name": "acq_id", "type": "[t]", "transform": None},


    "instrument.measurementSettings.name": {"name": "acq_measurementSettings_name", "type": "[t]", "transform": None},
    "instrument.measurementSettings.duration": {"name": "acq_measurementSettings_duration", "type": "[f]", "transform": None, "bioodv": {
        "object":"SDN:P01::AZDRZZ01",
        "units":"SDN:P06:UMIN"
    }},
    "instrument.measurementSettings.CytoSettings.SamplePompSpeed": {"name": "acq_measurementSettings_pumpSpeed", "type": "[f]", "transform": None},
    "instrument.measurementSettings.triggerChannel": {"name": "acq_measurementSettings_triggerChannel", "type": "[t]", "transform": None},
    "instrument.measurementSettings.triggerLevel": {"name": "acq_measurementSettings_triggerLevel", "type": "[f]", "transform": None},
    "instrument.measurementSettings.smartTrigger": {"name": "acq_measurementSettings_smartTrigger", "type": "[t]", "transform": lambda v: "true" if v else "false"},
    # "instrument.measurementSettings.takeImages": {"name": "measurementSettings_takeImages", "type": "[t]", "transform": None},
    # "instrument.measurementSettings.takeImages": {"name": None},

    "instrument.measurementResults.start": {"name": "sample_measurementResults_Start", "type": "[t]", "transform": extract_date_utc},
    "instrument.measurementResults.start*1": {"name": "sample_measurementResults_StartH", "type": "[t]", "transform": extract_time_utc},
    "instrument.measurementResults.duration": {"name": "sample_measurementResults_duration", "type": "[f]", "transform": None},
    "instrument.measurementResults.particleCount": {"name": "sample_measurementResults_particleCount", "type": "[f]", "transform": None},
    "instrument.measurementResults.particlesInFileCount": {"name": "sample_measurementResults_particlesInFileCount", "type": "[f]", "transform": None},
    "instrument.measurementResults.pictureCount": {"name": "sample_measurementResults_pictureCount", "type": "[f]", "transform": None},
    "instrument.measurementResults.pumpedVolume": {"name": "sample_measurementResults_pumpedVolume", "type": "[f]", "transform": None},
    "instrument.measurementResults.analysedVolume": {"name": "sample_measurementResults_analysedVolume", "type": "[f]", "transform": None},
    "instrument.measurementResults.particleConcentration": {"name": "sample_measurementResults_particleConcentration", "type": "[f]", "transform": None},
    "instrument.measurementResults.systemTemperature": {"name": "sample_measurementResults_systemTemperature", "type": "[f]", "transform": None},
    "instrument.measurementResults.sheathTemperature": {"name": "sample_measurementResults_sheathTemperature", "type": "[f]", "transform": None},
    "instrument.measurementResults.absolutePressure": {"name": "sample_measurementResults_absolutePressure", "type": "[f]", "transform": None},
    "instrument.measurementResults.differentialPressure": {"name": "sample_measurementResults_differential_pressure","type": "[f]","transform": None},

    # commented because same data are too long to be stored in the colunms (more than 250 characters (limited in Ecotaxa by varstring))
    # "particles[].pulseShapes*FWS": {"name": "object_pulseShape_FWS","type": "[t]","transform":search_pulse_shapes("FWS")},
    # "particles[].pulseShapes*FWS": {"name": "object_pulseShape_FWS","type": "[t]","transform":add_pulse_shapes("FWS")},
    # "particles[].pulseShapes*Sidewards_Scatter": {"name": "object_pulseShape_Sidewards_Scatter","type": "[t]","transform":search_pulse_shapes("Sidewards Scatter")},
    # "particles[].pulseShapes*Fl_Yellow": {"name": "object_pulseShape_Fl_Yellow","type": "[t]","transform":search_pulse_shapes("Fl Yellow")},
    # "particles[].pulseShapes*Fl_Orange": {"name": "object_pulseShape_Fl_Orange","type": "[t]","transform":search_pulse_shapes("Fl Orange")},
    # "particles[].pulseShapes*Fl_Red": {"name": "object_pulseShape_Fl_Red","type": "[t]","transform":search_pulse_shapes("Fl Red")},
    # "particles[].pulseShapes*Curvature": {"name": "object_pulseShape_Curvature","type": "[t]","transform":search_pulse_shapes("Curvature")},
    # "particles[].pulseShapes*Forward_Scatter_Left": {"name": "object_pulseShape_Forward_Scatter_Left","type": "[t]","transform":search_pulse_shapes("Forward Scatter Left")},
    # "particles[].pulseShapes*Forward_Scatter_Right": {"name": "object_pulseShape_Forward_Scatter_Right","type": "[t]","transform":search_pulse_shapes("Forward Scatter Right")},
}
    


    # # Add les dynamics column FOR measurementSettings AND measurementResults features
    # dynamic_keys = ["measurementSettings", "measurementResults"]
    # for key in dynamic_keys:
    #     if key in data["instrument"]:
    #         for subkey, value in data["instrument"][key].items():
    #             column_name = transform_column_name(f"{key}.{subkey}")
    #             column_mapping[f"{key}.{subkey}"] = {
    #                 "name": column_name,
    #                 "type": "[t]" if isinstance(value, str) else "[f]",
    #                 "transform": None,
    #             }

    # # add the pulseShapes columns
    # pulse_shapes = data["instrument"]["channels"]
    # for channel in pulse_shapes:
    #     print(f"Processing channel: {channel['description']}")
    #     column_name = transform_column_name(f"pulseShape.{channel['description']}")
    #     print(f"Column name: {column_name}")
    #     column_mapping[f"pulseShape.{channel['description']}"] = {
    #         "name": column_name,
    #         "type": "[t]",
    #         "transform": None,
    #     }

    # Build the columns and types list

    files_in_zip = []

    bioODV_header = [
        "SDN_PARAMETER_MAPPING"
    ]
    bioODV_header = gen_bioODV_header_from_mapping(column_mapping, bioODV_header)
    bioODV_header = gen_bioODV_header_from_extra(extra_data, bioODV_header)
    # print(bioODV_header)
    columns = ["img_file_name","img_rank"] + list(extra_data.keys())  # Add extra data at the begin of the tsv line
    types = ["[t]","[f]"] + ["[t]" if isinstance(value['value'], str) else "[f]" for value in extra_data.values()]
    seen_columns = set(columns)  # Éviter les doublons avec extra_data

    for key, mapping in column_mapping.items():
        # if mapping["name"] == None:
        if "name" not in mapping or mapping["name"] is None:
            continue  # Ignore column where name is undefined
        if mapping["name"] not in seen_columns:
            columns.append(mapping["name"])
            types.append(mapping["type"])
            seen_columns.add(mapping["name"])

    # Array to log particles without image
    missing_images = []

    # Building tsv lines
    rows = []
    for particle in data["particles"]:
        if not particle["hasImage"]:
            continue  # Ignore particles without image

        particle_id = particle["particleId"]
        print(f"\rProcessing particle: {particle_id}", end='', flush=True)
        pulseShapes = particle["pulseShapes"]
        # print("pulseShapes:", pulseShapes)
        image_data = next((img["base64"] for img in data["images"] if img["particleId"] == particle_id), None)
        if image_data:
            image_file = f"particle_{particle_id}.jpg"
            with open(os.path.join(output_images_dir, image_file), "wb") as img_file:
                img_file.write(base64.b64decode(image_data))
                files_in_zip.append(os.path.join(output_images_dir, image_file))
        else:
            missing_images.append(particle_id)
            continue  # go to next particle

        pulse_shape_file =  f"pulse_shape_{particle_id}.jpg"
        pulse_shape_path = os.path.join(output_images_dir, pulse_shape_file)
        with open(pulse_shape_path, "wb") as img_file:
            image_data = draw_pulse_shape(pulseShapes, "FWS", pulse_shape_path)
            # img_file.write(image_data)
            files_in_zip.append(pulse_shape_path)

            #TODO: add columns defining polynom coefficents of the pulse shape
            # row.append(polynomial_fits)

        #TODO: add columns defining polynom coefficents of the pulse shape
        polynomial_fits = []

        row = make_row(particle, data, image_file, 0, column_mapping, extra_data, polynomial_fits)
        rows.append(row)
        row = make_row(particle, data, pulse_shape_file, 1, column_mapping, extra_data, polynomial_fits)
        rows.append(row)

    print() # to invalid the progress bar

    # Écrire le fichier TSV
    with open(output_tsv, "w", newline="") as tsv_file:

        # Write the bioODV header
        if bioODVHeader == True:
            for row in bioODV_header:
                # tsv_file.write("\t".join(row) + "\n")
                tsv_file.write("//"+ row + "\n")

        # Write the TSV header
        tsv_file.write("\t".join(columns) + "\n")
        tsv_file.write("\t".join(types) + "\n")

        # Write the TSV data
        for row in rows:
            # print("Row:", row)
            # tsv_file.write("\t".join(row) + "\n")
            tsv_file.write("\t".join(str(item) for item in row) + "\n")

    files_in_zip.append(output_tsv)

    archive_filename = os.path.splitext(input_json)[0] + '.zip'
    with ZipFile(archive_filename, 'w') as zip_file:
        for file in files_in_zip:
            zip_file.write(file)
            # zip_file.write(file, arcname=os.path.basename(file))



    # with ZipFile('archive.zip', 'w') as zip_file:
    #     for root, dirs, files in os.walk(output_images_dir):
    #         for file in files:
    #             file_path = os.path.join(root, file)
    #             zip_file.write(file_path, arcname=os.path.basename(file_path))

    # Write the log file
    # with open(log_file, "w") as log:
    #     json.dump(missing_images, log, indent=4)

    print(f"Images save in: {output_images_dir}")
    print(f"TSV file save in: {output_tsv}")
    # print(f"Log des particules sans images : {log_file}")
    print("Fichier zip créé :", archive_filename)



def is_absolute_windows(path):
    """Determines if a path is absolute on Windows."""
    return os.path.splitdrive(path)[0] != ""

def is_absolute_unix(path):
    """Determines if a path is absolute on Unix/Linux/macOS."""
    return path.startswith('/')

def is_absolute(path):
    """Determines if a path is absolute, depending on the operating system."""
    if os.name == 'nt':
        return is_absolute_windows(path)
    else:
        return is_absolute_unix(path)

# CLI
if __name__ == "__main__":

    print("-- main.py --")

    parser = argparse.ArgumentParser(description="Analyze JSON file to generate a folder containing the TSV file and the images.")
    parser.add_argument("input_json", help="The path to the JSON file to analyze.")
    parser.add_argument("--extra", required=True, help="The path to the JSON file containing the extra data. (at the moment name must be extra_data.json and aside the json file)")
    parser.add_argument("--bioODV", default=False, help="Add the bioODV headers to the TSV file.")
    args = parser.parse_args()

    input_json = args.input_json
    if not is_absolute(input_json):
        input_json = os.path.abspath(input_json)
    #print("input_file:", input_json)

    extra_file = args.extra
    if not is_absolute(extra_file):
        extra_file = os.path.abspath(extra_file)
    #print("extra_file:",extra_file)

    bioODVHeader = args.bioODV

    # main(args.input_json, args.extra)
    main(input_json, extra_file)
