from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import sys
import logging
import click

suffixes = [".jpg", ".png", ".JPG", ".PNG"]
skip_log_format = "Skipped {}: EXIF analysis failed."


def place_pictures(target_dir="./", dir_suffix=""):
    logging.debug(target_dir)
    processed = 0
    for target_file in Path(target_dir).iterdir():
        if target_file.is_dir() or target_file.suffix not in suffixes:
            continue
        with Image.open(target_file) as image_file:
            try:
                exif = image_file._getexif()
            except AttributeError:
                logging.info(skip_log_format.format(target_file.name))
                continue
        date_info = exif[36867][:10].split(":")
        if len(date_info) != 3:
            logging.info(skip_log_format.format(target_file.name))
            continue
        move_dir_str = "_".join(date_info)
        logging.debug(move_dir_str)
        if dir_suffix != "":
            dir_suffix = "_" + dir_suffix
        move_path = Path("{0}/{1}{2}".format(target_dir, move_dir_str, dir_suffix))
        logging.debug(move_path)
        move_path.mkdir(exist_ok=True)
        logging.info("Move {0} to {1}".format(target_file.name, move_path))
        target_file.rename(move_path / target_file.name)
        processed += 1
    logging.info("Processed {} file(s)".format(processed))


@click.command()
@click.option('--suffix', default="", type=str, help="Directory name suffix (ex: 20XX_XX_XX_suffix)")
@click.option('--debug', default=False, is_flag=True, help="Print debug information")
@click.argument("dir_name", type=click.Path(exists=True), required=False)
def main(suffix, debug, dir_name):
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)
    if dir_name is None:
        dir_name = "./"
    place_pictures(dir_name, suffix)


if __name__ == "__main__":
    main()
    # place_pictures(sys.argv[1])
