#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fileinput import filename
from convert import ImgConverter
from capture import live_convert
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys
import os

if __name__ == "__main__":
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--live", action="store_true", default=False, help="Capture and convert straight from camera")
    parser.add_argument("--fileName", default="img.jpg", help="Filename to use with the converter")
    parser.add_argument("--cameraId", default=0, help="Select camera id for live mode")
    parser.add_argument("--numChunks", default=100, type=int, help="Num chunks to divide the input image (per axis). Total amount of chunks ~ numChunks^2")
    args = parser.parse_args()
    
    if(len(sys.argv) == 1):
        parser.print_help()
        exit(0)

    converter = ImgConverter(args.numChunks)
    fileName = args.fileName
    fileBase = os.path.basename(fileName).split(".")[0]
    fileOutput = os.path.join(os.path.dirname(fileName), f"{fileBase}.txt")

    print(f"Using filename: {fileName}")

    if(args.live):
        print(f"Live mode (output: {fileOutput})")
        live_convert(converter, fileBase, args.cameraId)
    else:
        print(f"Converting {fileName} to {fileOutput}...")
        intensities = converter.get_intensities(fileName)
        converter.generate_output(intensities, fileOutput)