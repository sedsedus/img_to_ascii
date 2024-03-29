#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from convert import ImgConverter
from capture import ImageGrabber
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def live_convert(converter, fileBase, cameraId, saveIntermediate):
        capturedName = f'{fileBase}.png'
        outName = f"{fileBase}.txt"
        with ImageGrabber(cameraId) as grabber:
            try:
                print("Press 'Ctrl + c' to quit")
                for img in grabber.get_images():
                    if(saveIntermediate):
                        img.save(capturedName)
                    converter.convert_image(img, outName)
            except KeyboardInterrupt:
                print()
                print("Exiting...")

if __name__ == "__main__":
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--live", action="store_true", default=False, help="Capture and convert straight from camera")
    parser.add_argument("--fileName", default="img.jpg", help="Filename to use with the converter")
    parser.add_argument("--cameraId", default=0, type=int, help="Select camera id for live mode")
    parser.add_argument("--numChunks", default=100, type=int, help="Num chunks to divide the input image (per axis). Total amount of chunks ~ numChunks^2")
    parser.add_argument("--fontAspectRatio", default=2.3, type=float, help="Font character aspect ratio (~2)")
    parser.add_argument("--liveSaveIntermediate", action="store_true", default=False, help="Save intermediate camera grabbed image")
    args = parser.parse_args()
    
    if(len(sys.argv) == 1):
        parser.print_help()
        sys.exit(0)

    converter = ImgConverter(args.numChunks, args.fontAspectRatio)
    fileName = args.fileName
    fileBase = os.path.basename(fileName).split(".")[0]
    fileOutput = os.path.join(os.path.dirname(fileName), f"{fileBase}.txt")

    print(f"Using filename: {fileName}")

    if(args.live):
        print(f"Live mode (output: {fileOutput})")
        live_convert(converter, fileBase, args.cameraId, args.liveSaveIntermediate)
    else:
        print(f"Converting {fileName} to {fileOutput}...")
        converter.convert(fileName, fileOutput)