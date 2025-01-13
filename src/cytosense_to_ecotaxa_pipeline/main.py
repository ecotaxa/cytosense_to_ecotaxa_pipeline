import json
import os
import base64
import csv
import argparse
from datetime import datetime
from zipfile import ZipFile

# Transformation pour supprimer l'extension d'un nom de fichier
def remove_extension(value):
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
    """
    try:
        dt = datetime.fromisoformat(iso_datetime.rstrip("Z")).astimezone()  # Conversion vers UTC
        return dt.strftime("%Y%m%d UTC")
    except ValueError:
        return "INVALID_DATE"

def extract_time_utc(iso_datetime):
    """
    Extrait l'heure au format HHMMSS UTC à partir d'une chaîne ISO 8601.
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
    def search(value):
        result = next((item for item in value if item['description'] == description), None)
        if result:
            return result["values"]
        return None
    return search
# Then in your mapping you can use it like:
# {"name": "pulseShape_FWS", "type": "[t]", "transform": search_pulse_shapes("FWS")}



# Formate une valeur avec un seul jeu de guillemets pour les chaînes de texte
def format_value(value):
    if isinstance(value, str):
        cleaned_value = value.strip('"')  # Supprime tous les guillemets autour
        return f'"{cleaned_value}"'
    return str(value)  # Retourne les autres types sous forme de chaîne

# Fonction pour transformer les noms de colonnes dynamiquement
def transform_column_name(name):
    return name.replace(".", "_").replace(" ", "_")

def main(input_json, extra_data_file):
    # Charger les fichiers JSON

    print("open:", input_json)
    print("extra:", extra_data_file)

    with open(input_json, "r") as f:
        data = json.load(f)

    with open(extra_data_file, "r") as f:
        extra_data = json.load(f)

    output_images_dir = "images"
    os.makedirs(output_images_dir, exist_ok=True)
    output_tsv = os.path.join(output_images_dir, "ecotaxa_output.tsv")
    output_tsv = os.path.abspath(output_tsv)# make absolute path
    log_file = os.path.join(output_images_dir, "log.json")
    log_file = os.path.abspath(log_file) # make absolute path

    # Dictionnaire de mapping des colonnes principales
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
    "instrument.measurementSettings.duration": {"name": "acq_measurementSettings_duration", "type": "[f]", "transform": None},
    "instrument.measurementSettings.pumpSpeed": {"name": "acq_measurementSettings_pumpSpeed", "type": "[f]", "transform": None},
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
#     "particles.pulseShape.FWS": {"name": "pulseShape_FWS","type": "[t]","transform": None},
#     "particles.pulseShape.Sidewards Scatter": {"name": "pulseShape_Sidewards_Scatter","type": "[t]","transform": None},
#     "particles.pulseShape.Fl Yellow": {"name": "pulseShape_Fl_Yellow","type": "[t]","transform": None},
#     "particles.pulseShape.Fl Orange": {"name": "pulseShape_Fl_Orange","type": "[t]","transform": None},
#     "particles.pulseShape.Fl Red": {"name": "pulseShape_Fl_Red","type": "[t]","transform": None},
#     "particles.pulseShape.Curvatures": {"name": "pulseShape_Curvatures","type": "[t]","transform": None},
#     "particles.pulseShape.Forwards Scatter Right": {"name": "pulseShape_Forwards_Scatter_Right","type": "[t]","transform": None},
#     "particles.pulseShape.Forwards Scatter Right": {"name": "pulseShape_Forwards_Scatter_Right","type": "[t]","transform": None},
    # "particles.pulseShape": {"name": "pulseShape_FWS","type": "[t]","transform":None },
    # "particles.pulseShape": {"name": "pulseShape_FWS2","type": "[t]","transform":None },

    # "particles[].pulseShapes": {"name": "pulseShape_FWS","type": "[t]","transform":search_FWS }
    "particles[].pulseShapes*FWS": {"name": "object_pulseShape_FWS","type": "[t]","transform":search_pulse_shapes("FWS")},
    "particles[].pulseShapes*Sidewards_Scatter": {"name": "object_pulseShape_Sidewards_Scatter","type": "[t]","transform":search_pulse_shapes("Sidewards Scatter")},
    "particles[].pulseShapes*Fl_Yellow": {"name": "object_pulseShape_Fl_Yellow","type": "[t]","transform":search_pulse_shapes("Fl Yellow")},
    "particles[].pulseShapes*Fl_Orange": {"name": "object_pulseShape_Fl_Orange","type": "[t]","transform":search_pulse_shapes("Fl Orange")},
    "particles[].pulseShapes*Fl_Red": {"name": "object_pulseShape_Fl_Red","type": "[t]","transform":search_pulse_shapes("Fl Red")},
    "particles[].pulseShapes*Curvature": {"name": "object_pulseShape_Curvature","type": "[t]","transform":search_pulse_shapes("Curvature")},
    "particles[].pulseShapes*Forward_Scatter_Left": {"name": "object_pulseShape_Forward_Scatter_Left","type": "[t]","transform":search_pulse_shapes("Forward Scatter Left")},
    "particles[].pulseShapes*Forward_Scatter_Right": {"name": "object_pulseShape_Forward_Scatter_Right","type": "[t]","transform":search_pulse_shapes("Forward Scatter Right")},

}
    


    # # Ajouter les colonnes dynamiques pour measurementSettings et measurementResults
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

    # # Ajouter les colonnes de pulseShapes
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

    # Construction des colonnes finales

    files_in_zip = []

    columns = ["img_file_name"] + list(extra_data.keys())  # Extra data en début
    types = ["[t]"] + ["[t]" if isinstance(value, str) else "[f]" for value in extra_data.values()]
    seen_columns = set(columns)  # Éviter les doublons avec extra_data

    for key, mapping in column_mapping.items():
        # if mapping["name"] == None:
        if "name" not in mapping or mapping["name"] is None:
            continue  # Ignorer les colonnes sans nom
        if mapping["name"] not in seen_columns:
            columns.append(mapping["name"])
            types.append(mapping["type"])
            seen_columns.add(mapping["name"])

    # Log des particules sans images
    missing_images = []

    # Construction des lignes
    rows = []
    for particle in data["particles"]:
        if not particle["hasImage"]:
            continue  # Ignorer les particules sans image

        particle_id = particle["particleId"]
        pulseShapes = particle["pulseShapes"]
        print("pulseShapes:",pulseShapes)
        image_data = next((img["base64"] for img in data["images"] if img["particleId"] == particle_id), None)
        if image_data:
            image_file = f"particle_{particle_id}.png"
            with open(os.path.join(output_images_dir, image_file), "wb") as img_file:
                img_file.write(base64.b64decode(image_data))
                files_in_zip.append(os.path.join(output_images_dir, image_file))
        else:
            missing_images.append(particle_id)
            continue  # Passer à la particule suivante

        row = [image_file]  # img_file_name
        for value in extra_data.values():
            row.append(format_value(value))

        for key, mapping in column_mapping.items():
            print("Key:", key)
            print("Mapping:", mapping)

            if "name" not in mapping or mapping["name"] is None:
                continue  # Ignorer les colonnes sans name défini

            try:
                if "." in key:
                    print(f"Key: {key}, Value: {data.get(key, None)}")
                    key_parts = key.split(".")
                    print(f"Key parts: {key_parts}")
                #     value = data.get(key_parts[0], {}).get(key_parts[1], None)
                #     print(f"Key parts: {key_parts}, Value: {value}")
                # else:
                #     value = data.get(key, None)
               
                    # current_obj = particle  # Start from the particle object
                    current_obj = data  # Start from the particle object
                    for part in key_parts:
                        print(f"Current part: {part}")
                        star = part.split("*")
                        bracket = part.split("[")
                        if len(star)>1: part = star[0]
                        if len(bracket)>1: 
                            part = bracket[0]
                            print(f"Bracket: part: {part}")
                            if part == "particles":
                                current_obj = particle
                                print("Particles -> " , current_obj)
                            # current_obj = part
                        else:
                            current_obj = current_obj.get(part, {})
                            if part == "pulseShapes":
                                print("PulseShapes -> " , current_obj)
                        print(f"Current object: {current_obj}")



                    value = current_obj if current_obj != {} else None
                else:
                    value = particle.get(key, None)


                if mapping["transform"]:
                    value = mapping["transform"](value)
                    print(f"Transformed value: {value}")

                row.append(format_value(value))
            except Exception as e:
                row.append("ERREUR")

        rows.append(row)

    # Écrire le fichier TSV
    with open(output_tsv, "w", newline="") as tsv_file:
        tsv_file.write("\t".join(columns) + "\n")
        tsv_file.write("\t".join(types) + "\n")
        for row in rows:
            tsv_file.write("\t".join(row) + "\n")
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

    # Écrire le fichier de log
    with open(log_file, "w") as log:
        json.dump(missing_images, log, indent=4)

    print(f"Fichier TSV sauvegardé : {output_tsv}")
    print(f"Images sauvegardées dans : {output_images_dir}")
    print(f"Log des particules sans images : {log_file}")
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

    parser = argparse.ArgumentParser(description="Analyse un fichier JSON pour générer un TSV et des images.")
    parser.add_argument("input_json", help="Le chemin vers le fichier JSON à analyser.")
    parser.add_argument("--extra", required=True, help="Le chemin vers le fichier JSON contenant les extra data.")
    args = parser.parse_args()

    input_json = args.input_json
    if not is_absolute(input_json):
        input_json = os.path.abspath(input_json)
    print("input_file:", input_json)

    extra_file = args.extra
    if not is_absolute(extra_file):
        extra_file = os.path.abspath(extra_file)
    print("extra_file:",extra_file)

    # main(args.input_json, args.extra)
    main(input_json, extra_file)
