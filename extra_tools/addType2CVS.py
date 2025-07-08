"""
Be careful, script destroy previous generated file, use it only if you are sure that you want to overwrite the destination file.

This script update the features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab.csv

file with a new column with the type of each value in the second

"""


import pandas as pd
from dateutil.parser import parse

# Load CSV
csv_path = "features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab.csv"
output_path = "features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab update.tmp.csv"

with open(csv_path, encoding="utf-8") as f:
    lines = f.readlines()

output_lines = []
in_particle_section = False
in_pulse_shape = False
in_parameters = False
current_suffix = None

for idx, line in enumerate(lines):
    # Arrêt du traitement normal à la ligne "example of one particle from the acquisition file"
    if "example of one particle from the acquisition file" in line:
        output_lines.append(line)
        in_particle_section = True
        continue

    if not in_particle_section:
        # On recopie les lignes avant la section "example of one particle..."
        output_lines.append(line)
        continue

    # On est dans la section "example of one particle..."
    # Arrêt si on tombe sur une ligne vide, .xml file, ou ,,,,,,,
    if line.strip() == "" or line.startswith(".xml file:") or line.strip(",\n") == "":
        break

    cols = [c.strip() for c in line.split(",")]

    # Traitement des pulseShapes
    if cols[0].startswith("particles.pulseShapes.description"):
        func = cols[1]
        if func:
            # Génère la ligne spéciale pour chaque FUNC
            output_lines.append(f'# "particles[].pulseShapes*{func}": {{"name": "object_pulseShape_{func}","type": "[t]","transform":search_pulse_shapes("{func}")}},\n')
        in_pulse_shape = True
        continue

    # Ignore les values1
    if cols[0].startswith("particles.pulseShapes.values1"):
        continue

    # Traitement des parameters
    if cols[0].startswith("particles.parameters.description"):
        current_suffix = cols[1]
        in_parameters = True
        continue

    if in_parameters and cols[0].startswith("particles.parameters."):
        tag = cols[0].replace("particles.parameters.", "")
        # Cherche si au moins une colonne "TRUE" (dans les colonnes 2 à 6)
        if any(x.strip().upper() == "TRUE" for x in cols[2:7]):
            output_lines.append(f'particles[].parameters.{tag}*{current_suffix}\n')
        continue

    # Si on tombe sur une nouvelle section ou une ligne qui n'est pas un paramètre, on arrête le bloc parameters
    if in_parameters and not cols[0].startswith("particles.parameters."):
        in_parameters = False
        current_suffix = None

# Sauvegarde le résultat
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print("save file:", output_path)
