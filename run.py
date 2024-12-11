import logging
from cellpose import models
import argparse
import os
import numpy as np
import tifffile as tif
import sys
import traceback

def main(input, output):
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Create output folder
        os.makedirs(output, exist_ok=True)
        logging.info(f'Created output directory: {output}')

        model = models.CellposeModel(gpu=True, pretrained_model='utils/models/cyto2/cyto2_cellpose_model.pth')
        logging.info('Cellpose model loaded.')

        # Load tiff files
        image = tif.imread(input)
        if image.ndim == 4:
            logging.info('Multichannel tiff imported, using Channel 1...')
            tiff_files = image[:, 1, :, :]
        else:
            logging.info('Single Channel tiff...')
            tiff_files = image[:, :, :]

        logging.info(f'Shape of tiff files: {tiff_files.shape}')

        # Normalize images to 0-1 range
        tiff_files = tiff_files.astype(np.float32) / 255.0
        logging.info('Normalized tiff files to 0-1 range.')

        # Evaluate the model on the input images
        results = model.eval(tiff_files, channels=[0, 0], cellprob_threshold=-1.0, flow_threshold=0.5)
        logging.info('Model evaluation completed.')

        # Unpack results based on their length
        if len(results) == 3:
            masks_pred, flows, styles = results
            logging.info('Results unpacked: masks_pred, flows, styles.')
        else:
            masks_pred, flows, styles, diams = results
            logging.info('Results unpacked: masks_pred, flows, styles, diams.')

        # Save masks and flows to TIFF files
        masks_output_path = os.path.join(output, 'masks_pred.tif')
        flows_output_path = os.path.join(output, 'flows.tif')

        tif.imwrite(masks_output_path, masks_pred.astype(np.uint16))
        logging.info(f'Masks saved to {masks_output_path}')

        tif.imwrite(flows_output_path, flows[0].astype(np.float32))
        logging.info(f'Flows saved to {flows_output_path}')

    except Exception as e:
        logging.error("An error occurred:", exc_info=True)
        sys.exit(1)

if __name__ == "__main__": 
    # Create argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, required=True, help='Input folder that contains tiff files.')
    parser.add_argument('--output', type=str, required=True, help='Output folder to save the results.')

    args = parser.parse_args()

    main(args.input, args.output)