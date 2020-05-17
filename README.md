# DSHIPconverter

Scripts to convert DSHIP data

| :warning: ** This script is not yet generalized and might not work for your project. Pull requests are welcome**|
| --- |

## Installation

Install package with anaconda

```
conda create -n DSHIP
conda activate DSHIP
conda install -c observingClouds DSHIPconverter
```

## Converting
Example of converting DSHIP data:
```bash
python convert_DSHIP.py -i '/path/to/DSHIP/folder/*.dat' -o DSHIP_converted.nc
```

## EUREC4A METEOR DSHIP
This script works with the DSHIP data gathered onboard the RV METEOR. The data can be downloaded e.g. with
```bash
wget -r --cut-dirs=100 -A dat https://observations.ipsl.fr/aeris/eurec4a-data/SHIPS/RV-METEOR/DSHIP/
```

