
import pandas as pd

def generate_mapping(csv_path: str, output_path: str):
    df = pd.read_csv(csv_path, dtype=str).fillna("")

    eco_taxa_cols = [
        "MIO=keep in EcoTaxa",
        "Lotty=keep in EcoTaxa",
        "CEFAS=keep in EcoTaxa",
        "SYKE=keep in EcoTaxa",
        "LOG =keep in EcoTaxa"
    ]

    def is_selected(row):
        return any(row.get(col, "").strip().lower() == "true" for col in eco_taxa_cols)

    selected_rows = df[df.apply(is_selected, axis=1)]

    with open(output_path, "w") as f:
        f.write("from .transform_function import *\n\n")
        f.write("column_mapping = {\n")

        for _, row in selected_rows.iterrows():
            path = row['path']
            type_ = row['type']
            transform_raw = row['transform'].strip()
            bioODV_name = row.get('bioODV.name', '').strip()
            name = bioODV_name if bioODV_name else row['name']
            obj = row.get('bioODV.object', '').strip()
            units = row.get('bioODV.units', '').strip()

            def write_entry(dict_path, dict_name, dict_type, dict_transform, dict_obj, dict_units):
                f.write(f'    "{dict_path}": {{ "name": "{dict_name}", "type": "{dict_type}"')
                if dict_transform == "":
                    pass  # omit transform
                elif dict_transform == "None":
                    f.write(f', "transform": None')
                else:
                    f.write(f', "transform": {dict_transform}')
                if dict_obj:
                    f.write(f', "object": "{dict_obj}"')
                if dict_units:
                    f.write(f', "units": "{dict_units}"')
                f.write(" },\n")

            if transform_raw.startswith("[") and transform_raw.endswith("]"):
                transforms = transform_raw.strip("[]").split(",")
                transforms = [t.strip().replace("'", "").replace('"', "") for t in transforms]
                for idx, func in enumerate(transforms):
                    suffix = f"*{name}" if idx > 0 else ""
                    write_entry(path + suffix, name, type_, func, obj, units)
            else:
                transform_func = transform_raw  # may be "", "None", or function name
                write_entry(path, name, type_, transform_func, obj, units)

        f.write("}\n")

if __name__ == "__main__":
    generate_mapping(
        csv_path="features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab update.csv",
        output_path="mapping.py"
    )
