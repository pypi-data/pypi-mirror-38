import os
import shutil
import structlog
from os import path
from glob import glob
from argparse import ArgumentParser

log = structlog.getLogger()


def validate_file_pairs(base_directory):
    """
    - Make directories
    - Delete resulting empty directories
    - Make a backup of the photos
    - Send the backup to a local directory
    - Send the report to a new sub-domain of anthonyagnone.com

    Report Structure
        - list of the file moves
        - list of the created directories
        - list of the deleted directories
        - list of file base names which did not have a {.jpg, .txt} pair

    :param str base_directory:
        Base directory to search for images under.
    :return tuple:
        bool: indication of success
        msg: supporting description message
    """

    paths_valid = []
    paths_invalid = []
    for root, dirs, files in os.walk(base_directory):
        for fn in files:
            base, ext = path.splitext(fn)
            # for each assumed {.jpg, .txt} pair, use .jpg as the anchor file for looking for the
            # other two.
            if ext.lower() in (".jpg", ".jpeg"):
                base_path = path.join(root, base)
                if path.exists("{}.txt".format(base_path)):
                    log.debug("{} is a valid pair.".format(base_path))
                    paths_valid.append(base_path)
                else:
                    log.error("{} is not a valid pair.".format(base_path))
                    paths_invalid.append(base_path)

    return paths_valid, paths_invalid


def read_keyword(fn):
    keyword = None
    with open(fn, 'r') as fp:
        for line in fp:
            if "beeb" in line and ":" in line:
                keyword = line.split(":")[1].strip()
    return keyword


def do(dir_base):
    """
    - Make directories
    - Delete resulting empty directories
    - Make a backup of the photos
    - Send the backup to a local directory
    - Send the report to a new sub-domain of anthonyagnone.com

    Report Structure
        - list of the file moves
        - list of the created directories
        - list of the deleted directories
        - list of file base names which did not have a {.jpg, .txt} pair

    :param str dir_base:
        Base directory to search for images under.
    :return tuple:
        bool: indication of success
        msg: supporting description message
    """

    dir_unknowns = path.join(dir_base, 'unknown')
    paths_moved = []
    dirs_created = []
    dirs_removed = []
    keywords = set()

    fns_valid, fns_invalid = validate_file_pairs(dir_base)

    # report any invalid pairs
    if len(fns_invalid) > 0:
        log.error("{} invalid file pairs detected.".format(fns_invalid))
        os.mkdir(dir_unknowns)

    for fn in fns_valid:
        keyword = read_keyword(fn + ".txt")

        if keyword:
            dir_keyword = path.join(dir_base, keyword)

            # if this is a new keyword, create its directory
            if keyword not in keywords:
                log.msg("New keyword found: {}. Creating directory".format(keyword))
                os.mkdir(dir_keyword)
                dirs_created.append(dir_keyword)
                keywords |= set(keyword)

            # move the file into the keyword directory
            log.msg("Moving {} to {}.".format(fn, dir_keyword))
            for file_to_move in glob(fn + '*'):
                shutil.move(file_to_move, dir_keyword)
            os.remove(path.join(dir_keyword, path.basename(fn) + ".txt"))
        else:
            # keyword not successfully found -- add to unknowns
            for file_to_move in glob(fn + '*'):
                shutil.move(file_to_move, dir_unknowns)

    for fn in fns_invalid:
        log.msg("Moving {} to {}.".format(fn, dir_unknowns))
        for file_to_move in glob(fn + '*'):
            shutil.move(file_to_move, dir_unknowns)

    # remove any empty directories that the file movement creates
    for root, dirs, files in os.walk(dir_base):
        for d in dirs:
            dir_cur = path.join(root, d)
            if is_empty_directory(dir_cur):
                log.msg("Detected empty directory {}. Removing.".format(dir_cur))
                dirs_removed.append(dir_cur)
                os.rmdir(dir_cur)

    return 0, "Success"


def is_empty_directory(dir_name):
    return len(os.listdir(dir_name)) == 0


def undo():
    pass
