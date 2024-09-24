from cellpose import models
import argparse
import os
import numpy as np
import tifffile as tif

def main(input, output):
    
    # Create output folder
    os.makedirs(output, exist_ok=True)

    model = models.CellposeModel(gpu=True, pretrained_model='utils/models/nuclei/nuclei_cellpose_model.pth')
    
    # Load tiff files
    tiff_files = tif.imread(input)[:, 1, :, :]

    print('Shape of tiff files:', tiff_files.shape)

    # images = np.concatenate(tiff_files, axis=2)

    # Normalize images to 0-1 range
    # tiff_files = tiff_files.astype(np.float32) / 255.0

    # Evaluate the model on the input images
    results = model.eval(tiff_files, channels=[0, 0])
    
    # Unpack results based on their length
    if len(results) == 3:
        masks_pred, flows, styles = results
    else:
        masks_pred, flows, styles, diams = results

    # Save masks and flows to TIFF files
    masks_output_path = os.path.join(output, 'masks_pred.tif')
    flows_output_path = os.path.join(output, 'flows.tif')

    tif.imwrite(masks_output_path, masks_pred.astype(np.uint16))  # Convert masks to uint16 for saving
    tif.imwrite(flows_output_path, flows[0].astype(np.float32))   # Assuming flows[0] is the relevant data

if __name__ == "__main__": 
    # Create argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, required=True, help='Input to the folder that contains tiff files.')
    parser.add_argument('--output', type=str, required=True, help='Output folder to save the results.')

    args = parser.parse_args()

    main(args.input, args.output)
