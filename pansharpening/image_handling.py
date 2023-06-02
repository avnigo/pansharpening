import multiprocessing
import requests

from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto


class Compression(Enum):
    """Define GDAL creation options for compression."""

    DEFLATE = ["COMPRESS=DEFLATE"]  # 3.57 GB @ 52s
    LERC = ["COMPRESS=LERC"]  # 3.02 GB @ 25s
    LERC_DEFLATE = ["COMPRESS=LERC_DEFLATE"]  # 2.98 GB @ 53s
    LERC_ZSTD = ["COMPRESS=LERC_ZSTD"]  # 3.02 GB @ 43s
    LZW = ["COMPRESS=LZW", "PREDICTOR=2"]  # 3.72 GB @ 44s
    PACKBITS = ["COMPRESS=PACKBITS"]  # 4.73 GB @ 15s
    JPEG = ["COMPRESS=JPEG"]  # needs conversion


class ImageType(Enum):
    PANCHROMATIC = auto()
    RGB = auto()
    NED = auto()
    PNEO = auto()


@dataclass
class Image:
    url: str
    streamable: bool = False

    def __post_init__(self):
        """All Images have a URL and path, either on disk or /vsicurl if streamable"""
        self.url = f"/vsicurl/{self.url}" if self.streamable else self.url
        self.path = (
            (Path(__file__).parent / "data" / Path(self.url).name).as_posix()
            if not self.streamable
            else self.url
        )


@dataclass
class ImageCollection:
    images: dict[ImageType, Image]

    def __post_init__(self):
        """Download all Images if not indicated as streamable."""
        if all(not image.streamable for image in self.images.values()):
            self.download_collection()

    def download_file(self, images) -> None:
        """Download single image from URL."""
        if (filename := Path(images.path)).exists():
            return
        print(f"> Downloading [queued]: {(url := images.url)} ...")
        with open(filename, "wb") as f:
            f.write(requests.get(url).content)
            print(f"+ {filename} downloaded")

    def download_collection(self) -> None:
        """Download complete ImageCollection in a parallel manner."""
        with multiprocessing.Pool(processes=len(self.images)) as pool:
            pool.map(self.download_file, self.images.values())
