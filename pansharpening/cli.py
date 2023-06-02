import argparse

from pansharpening.image_handling import Compression
from pathlib import Path


def parser():
    parser = argparse.ArgumentParser(
        prog="pansharpening",
        description="Pansharpening pipeline",
    )
    parser.add_argument(
        "--stream",
        "-s",
        help="process streamed imagery and discard inputs (default: `%(default)s`)",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--compression",
        "-c",
        help="choose the compression algorithm of the raster output (default: `%(default)s`)",
        choices=Compression.__members__,
        default="LERC",
        type=str,
    )
    parser.add_argument(
        "--raw",
        "-r",
        help="derive from raw Pleiades Neo imagery (default: `%(default)s`)",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--out",
        "-o",
        help="change the output destination directory (default: `%(default)s`)",
        default=Path(__file__).parent / "output",
        type=Path,
    )
    parser.add_argument(
        "--file",
        "-f",
        help="TOML file input of source imagery (default: `%(default)s`)",
        default=Path(__file__).parent / "data/imagery-sources.toml",
        type=Path,
    )
    return parser.parse_args()
