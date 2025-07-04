# Cytosense to EcoTaxa Pipeline

<img src="https://github.com/ecotaxa/cytosense_to_ecotaxa_pipeline/actions/workflows/build.yml/badge.svg" alt="Build cytosense_to_ecotaxa_pipeline"/>


A pipeline tool to convert Cytosense data files to EcoTaxa compatible format.
## Features

- Automated conversion from Cytosense (.cyz) to EcoTaxa format
- Built-in cyz2json binary for data extraction
- Cross-platform support (Linux, Windows, MacOS)

# pre installation
## Linux
sudo apt  install jq 

## Installation

### Installation from Github
Recommended way to install the pipeline is to use the install.sh script.

You just need to download the install.sh file from the repository. Run it with the following commands:

```bash
curl -L -O "https://raw.githubusercontent.com/ecotaxa/cytosense_to_ecotaxa_pipeline/main/install.sh"
chmod +x install.sh
sudo ./install.sh --github
```

### Installation from local files
The manual mode
```diff
- Warning: not fully tested
```

```bash
python3 -m venv venv    
source venv/bin/activate
pip install --upgrade pip
pip intall -e .
pip install six matplotlib Pillow numpy

# necessary to install the cyz2json binary but need to copy the main.py and/or pipeline.py files in the venv
# LATEST_TAG=$(curl -s "https://api.github.com/repos/ecotaxa/cytosense_to_ecotaxa_pipeline/releases/latest" | jq -r '.tag_name')
# TAG_WITHOUT_V="${LATEST_TAG#v}"
# PLATFORM_TAG="macosx_10_9_x86_64"
# PLATFORM_TAG="macosx_11_0_arm64"
# WHEEL_FILE_NAME="cytosense_to_ecotaxa_pipeline-${TAG_WITHOUT_V}-py3-none-${PLATFORM_TAG}.whl"
# WHEEL_URL="https://github.com/ecotaxa/cytosense_to_ecotaxa_pipeline/releases/download/${LATEST_TAG}/${WHEEL_FILE_NAME}"
# WHEEL_FILE="/tmp/${WHEEL_FILE_NAME}"
# curl -s -L "$WHEEL_URL" -o "$WHEEL_FILE"
# pip install "$WHEEL_FILE"
# SITE_PACKAGES_PATH=$(python -c "import site; print(site.getsitepackages()[0])")
# sudo ln -s "$SITE_PACKAGES_PATH/cytosense_to_ecotaxa_pipeline/bin/Cyz2Json" $PWD/test_venv/bin/Cyz2Json
# sudo ln -s "$SITE_PACKAGES_PATH/cytosense_to_ecotaxa_pipeline/pipeline.py" $PWD/test_venv/bin/pipeline.py
# sudo ln -s "$SITE_PACKAGES_PATH/cytosense_to_ecotaxa_pipeline/main.py" $PWD/test_venv/bin/main.py
# export LD_LIBRARY_PATH=$PWD/test_venv/lib/python${PYTHON_VERSION}/site-packages/cytosense_to_ecotaxa_pipeline/lib:${LD_LIBRARY_PATH}
# sudo chmod ago+x $PWD/test_venv/lib/python${PYTHON_VERSION}/site-packages/cytosense_to_ecotaxa_pipeline/bin/*

# without cyz2json binary
# make data folder
# paste in the data folder the json file
# add an extra line in the json file to add the cytosense data

# run the pipeline
python3 main.py --extra ../../data/extra_data.json ../../data/Deployment\ 1\ 2024-07-18\ 21h12.json

```

need to install cyz2json in the repo before, there are some bugs
```bash
sudo ./install.sh
```

on Windows use install.ps1 instead of install.sh not tested



### On MacOSX
When you use manual build: you need to bypass security 
You have 2 possibilities :
using xattr command.
```
xattr -d com.apple.quarantine  /opt/cytosense_to_ecotaxa_pipeline/bin/*
```
or if you do not want use xattr you need to go in Systems Settings > Security & Privacy > General and allow the app to be opened for the 10+ libraries. You need to relauch sevaral time the cyz2json binary to acheive all neccessary permissions.


# Run the pipeline

## using the command installed by the install.sh script
```bash
/usr/local/bin/cytosense_to_ecotaxa_pipeline the_cyz_files_to_import.tsv
```
the result will be in the the folder where you run the command
you will find
+ the json file (generated by cyz2json)
+ the images folder (with ecotaxa tsv file in it)
+ and the zip file, you could upload it to EcoTaxa

a folder named extra_data will be create with the extra data json files

## run pipeline.py
```
cd src/cytosense_to_ecotaxa_pipeline
ln -s /opt/cytosense_to_ecotaxa_pipeline_venv/bin/Cyz2Json cyz2json
(venv) python pipeline.py the_cyz_files_to_import.tsv
```

## run convert.py
```
(venv) python convert.py the_cyz_file_to_import.cyz --extra extra_data.json
```

# run only main.py
```
(venv) python main.py Deployment\ 1\ 2024-07-18\ 21h12.json --extra extra_data.json
```

# Uninstall

```bash
sudo ./uninstall.sh
```

on Windows use uninstall.ps1 instead of uninstall.sh


# Run with Docker

## build the container
```
docker build -t cyto2eco .
```

## run the container
```
docker run -v /Users/sebastiengalvagno/Work/cytosense_to_ecotaxa_pipeline/data:/data -v /Users/sebastiengalvagno/Work/cytosense_to_ecotaxa_pipeline/src/cytosense_to_ecotaxa_pipeline/extra_data:/extra cyto2eco /data/Deployment\ 1\ 2024-07-18\ 21h12.json --extra /extra/Deployment\ 1\ 2024-07-18\ 21h12.json --bioODV=False
```

# Build


## with GitHub Actions
Commit your code and push it to GitHub.
then add a tag to the commit and push it to GitHub. like the sample below
```bash
git tag v0.0.65 && git push origin v0.0.65
```
the action will build the binary and push it to the release

You will find result in : https://github.com/ecotaxa/cytosense_to_ecotaxa_pipeline/actions
and release in : https://github.com/ecotaxa/cytosense_to_ecotaxa_pipeline/releases

<!--
# Bug

+ to discover 
-->


# Make your mapping


## the tsv (for pipeline.py)

the tsv file is composed by two parts: the first part is the header describing the bioODV features and the second part is the data.

The header is composed by 4 columns.
+ the 1st column is //
+ the 2nd column contains the name of the column in the tsv (ie. a column name from the 1st line of the data part))
+ the 3rd and the 4th columns are the bioODV ampping.
+ the 3rd column contains the bioODV object name
+ the 4th column contains the bioODV units used by the value

```TSV
//  column_name  bioODV_name  bioODV_unit
```

sample
```TSV
//  object_lat   SDN:P01::STRTXLAT  SDN:P06::UUUU
//  object_lon   SDN:P01::STRTXLON  SDN:P06::UUUU
//  object_date  SDN:P01::STRT8601  SDN:P06::UUUU
file    object_lat  object_lon  object_date object_time object_depth_min    object_depth_max
Deployment 1 2024-07-18 21h12.cyz   42  7.2 2019-04-17  10:00   10  100
```


The data part is compoposed by
+ a 1st line that contains the columun name, where the 1st column is the path to the cyz file, the other columns are the extra data to add to the ecotaxa tsv file
+ the others lines are the data

## the JSON mapping (for main.py)
To update your mapping edit main.py, and search column_mapping variable. This is a dictionary where the key is the path to a JSON Cytosense feature 
and the value is an object to define how to store and transform the data for ecotaxa. The object have 3 features:
    + name: is the name of the column in ecotaxa
    + type: is the type of the column in ecotaxa [t] or [f] (for text or float)
    + transform: is a function to transform the value before storing it, you can use a lambda function or a function to transform the value

the cytosense key is a path in the json file, you can use the dot notation to access nested objects.

for example instrument.name is the path to read feature
```JSON
{
    "instrument":{
        "name": "instrument name"
    }
}
```

## Read data in particle array

to read feature, that are defined in the particle array, you need to use square bracket notation
"particles[].pulseShapes", in this case dot path are limited to the first feature and you need to use a function to find the data on it

To get particles[].pulseShapes.FWS, in fact you need to use a function to find the data on it

```JSON
{
    "particles[].pulseShapes*FWS": {
        "name": "object_pulseShape_FWS",
        "type": "[t]",
        "transform":search_pulse_shapes("FWS")
    }
}
```

search_pulse_shapes("FWS") is a function that search for the feature FWS in the pulseShapes array and return the value. You could add some processing in the sub function, for example, to convert the values in this case into a polynomial function or to convert the values to a string (take care to the data size: string length are limited to 250 characters in Ecotaxa)

The sub function permit to pass extra parameters to the function
```python
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
```


### Several use of the same cytosense feature
If you need to use the same cytosense feature several time in the mapping you can use the same name but with a different suffix: the suffix must be an id prefixed by a star.

Ecotaxa have a column for date and a column for time, but in the Cytosense data there is only one feature containing both date and time. Then you need to split the feature in two store in two columns.

For example:
the path to my feature is "instrument.measurementResults.start" then I define two mapping:
I use suffix "*date" and "*hour" to define different entries in the mapping, but you are free to choose the name you want (just need to have differnet suffix for each column, I could work with *1 et #2 
or
 the couple : no suffix and *mysuffix)
 (there are no use of the suffix in the code, that just for Python Dictionnary Key that must be unique)
```JSON
    "instrument.measurementResults.start*date": {"name": "sample_measurementResults_Start", "type": "[t]", "transform": extract_date_utc},
    "instrument.measurementResults.start*hour": {"name": "sample_measurementResults_StartH", "type": "[t]", "transform": extract_time_utc},
 ```


# The json extra data for ecotaxa tsv file used by main.py

The json file is a list of object, each object describes the data to add to the ecotaxa tsv file.
and could also contain the bioODV mapping.

a simple extra_data.json file could be:
```JSON
{
    "object_lat": {
        "value": "42",
    },
    "object_lon": {
        "value": "7.2",
    },
    "object_date": {
        "value": "2019-04-17",
    },
    "object_time": {
        "value": "10:00",
    },
    "object_depth_min": {
        "value": "10",
    },
    "object_depth_max": {
        "value": "100",
    }
}
```

a more complex example with the bioODV mapping
```JSON
{
    "object_lat": {
        "value": "42",
        "object": "SDN:P01::STRTXLAT",
        "units": "SDN:P06::UUUU"
    },
    "object_lon": {
        "value": "7.2",
        "object": "SDN:P01::STRTXLON",
        "units": "SDN:P06::UUUU"
    },
    "object_date": {
        "value": "2019-04-17",
        "object": "SDN:P01::STRT8601",
        "units": "SDN:P06::UUUU"
    },
    "object_time": {
        "value": "10:00",
    },
    "object_depth_min": {
        "value": "10",
    },
    "object_depth_max": {
        "value": "100",
    }
}

"object" and "units" features are optional.

