# SLAP2-Cellpose
## Cellpose Nuclei model retrained with SLAP2 data 

This repository contains a version of the Cellpose nuclei model that has been retrained using SLAP2 data. The Cellpose model is a generalist algorithm for cell segmentation.

# 1. Create an conda env
`conda create -n cellpose python=3.12`

`conda activate cellpose`

# 2. Install cellpose
`pip install -U --no-cache-dir git+https://www.github.com/mouseland/cellpose.git`

# 3. Running cellpose 
`python run.py --input <input_file_path> --output <output_directory_path>`
## Example
`python run.py --input /Users/caleb.shibu/Downloads/725018_20240326_163614_DMD1_merged.tif --output /Users/caleb.shibu/Desktop/test-cellpose` 

The output folder would have 2 files `flows.tif` and `masks_pred.tif`.
