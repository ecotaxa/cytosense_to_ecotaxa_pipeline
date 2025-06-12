"""
Be careful, script destroy previous generated file, use it only if you are sure that you want to overwrite the destination file.

This script update the features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab.csv

file with a new column with the type of each value in the second

"""


import pandas as pd
from dateutil.parser import parse

# Load CSV
csv_path = "features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab.csv"
df = pd.read_csv(csv_path)

# Determine type for each value in the second column
def detect_type(value):
    try:
        val = value.strip()
        
        type = '[t]'
        # Check for boolean values first
        if val.lower() in ['true', 'false']:
            # return '[b]'
            type = '[b]'
        
        # Try to parse as date
        try:
            parse(val, fuzzy=False)
            # return '[d]'
            type = '[d]'
        
        except (ValueError, TypeError):
            pass
        
        # Try to parse as float/number
        try:
            float(val)
            # return '[f]'
            type = '[f]'
        except:
            pass
        
        return type
    except:
        pass
    
    # Default to text if nothing else matches
    return '[t]'

second_column = df.columns[1]
type_column = df[second_column].astype(str).map(detect_type)

# Insert the type column
df.insert(2, 'type', type_column)

# Save to new CSV
output_path = "features_metadata_cytometry - SSLAMM_micro_setdef_CS101 - collab update.tmp.csv"
df.to_csv(output_path, index=False)

print("save file:", output_path)
