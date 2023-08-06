"""
Organizes exported Lightroom photos into directories, according to a key-value pair in
a side-car text file for each image. The value of this key-value pair is the name of the
directory that the photo should be put into.
"""
import os
import sys
import structlog
from os import path
from glob import glob
from argparse import ArgumentParser

from lightroom_export_organizer.make_folders import do, undo

log = structlog.getLogger()


def get_clargs():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-directory", help="Path to directory")
    return parser.parse_args()


def main():
    args = get_clargs()
    return do(args.input_directory)


if __name__ == '__main__':
    sys.exit(main())
