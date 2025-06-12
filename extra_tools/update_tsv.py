"""
Be careful, script destroy previous generated file, use it only if you are sure that you want to overwrite the destination file.

This script must be be launch after addType2CVS.py

This script update the features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab update.tmp.csv


file with some new columns 
    + name: determine ecotaxa column name from JSON path
    + transform: add column to transform data, some are pre filled (like boolean and date)
    + bioodv.*: 3 columns to map feature name with the BioODV reference

"""

import pandas as pd
from dateutil.parser import parse

# Load CSV
input_path = "features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab update.tmp.csv"
df = pd.read_csv(input_path, dtype=str).astype(str)

# Fix type column based on value in "example_value"
def correct_type(val, current_type):
    """
    Determine the correct type based on the example value.
    Returns [d] for dates, [t] for text/NaN values, or keeps current type.
    """
    if pd.isna(val) or val.strip().lower() == "nan":
        return "[t]"
    
    try:
        # Try to parse as date
        parse(val, fuzzy=False)
        return "[d]"
    except (ValueError, TypeError):
        # If it's not a date, keep the current type
        return current_type

# Apply type correction
# df["type"] = df.apply(lambda row: correct_type(row["example_value"], row["type"]), axis=1)

# Create "name" from suffix of "path"
df["__name_tmp__"] = df["path"].apply(lambda x: x.rsplit(".", 1)[-1] if "." in x else x)

# Apply specific overrides
df.loc[df["path"] == "filename", "__name_tmp__"] = "filename"
df.loc[df["path"] == "instrument.name", "__name_tmp__"] = "instrument"

# Insert "name" column just after "path"
if "path" in df.columns:
    path_index = df.columns.get_loc("path")
    # Ensure we have an integer index
    if isinstance(path_index, int):
        insert_position = path_index + 1
    else:
        # Handle case where get_loc returns a slice or array (shouldn't happen with unique column names)
        insert_position = list(df.columns).index("path") + 1
    
    df.insert(insert_position, "name", df.pop("__name_tmp__"))
else:
    raise ValueError("Column 'path' not found in the DataFrame.")

# Insert "transform" after "type" 
if "type" in df.columns:
    type_index = df.columns.get_loc("type")
    # Ensure we have an integer index
    if isinstance(type_index, int):
        insert_position = type_index + 1
    else:
        # Handle case where get_loc returns a slice or array
        insert_position = list(df.columns).index("type") + 1
    
        # Create transform values based on type
    def get_transform_value(t):
        if t == "[b]":
            return 'lambda v: "true" if v else "false"'
        elif t == "[d]":
            return '[extract_date_utc,extract_time_utc]'
        else:
            return "None"
        
    df.insert(
        insert_position,
        "transform",
        df["type"].map(get_transform_value)
    )
else:
    raise ValueError("Column 'type' not found in the DataFrame.")

# Add bioODV columns
df["bioODV.subject"] = ""
df["bioODV.object"] = ""
df["bioODV.units"] = ""


# some fix for the transform column
df.loc[df["path"] == "filename", "transform"] = "remove_extension"

# Save output
output_path = "features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab update.csv"
df.to_csv(output_path, index=False)


print(f"Processing complete. Output saved to {output_path}")
print(f"Processed {len(df)} rows")