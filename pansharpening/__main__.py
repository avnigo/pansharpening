import logging
import tomllib

from pathlib import Path

from osgeo import gdal
from osgeo_utils.gdal_pansharpen import gdal_pansharpen
from pansharpening.image_handling import ImageType, Image, ImageCollection, Compression
from pansharpening.cli import parser


def load_source_locations(
    sourcefile: Path = Path(__file__).parent / "data" / "imagery-sources.toml",
    source_type: str = "pansharpening",
    input_arguments: list = [],
    stream: bool = False,
) -> ImageCollection:
    """Loads source locations from TOML file into an ImageCollection object for easier handling."""

    if source_type == "orthorectification":
        raise NotImplementedError("Skipping file download, use preprocessed sources.")

    logging.info("> Streaming mode ON" if stream else "> Cached mode ON")
    return ImageCollection(
        images={
            ImageType[image_type]: Image(url=url, streamable=stream)
            for image_type, url in (
                tomllib.loads(sourcefile.read_text())[source_type].items()
                if not input_arguments
                else zip(["PANCHROMATIC", "RGB"], input_arguments)
            )
        }
    )


def set_gdal_config() -> None:
    gdal.SetConfigOption("VSI_CACHE", "YES")
    # gdal.SetConfigOption("VSI_CACHE_SIZE", "1000000000")
    # gdal.SetConfigOption("GDAL_CACHEMAX", "64")


def ortho_correct(sourcefile, stream) -> ImageCollection:
    # TODO: Correct raw imagery and return those as ImageCollection sources
    return load_source_locations(
        sourcefile, stream=stream, source_type="orthorectification"
    )


def pansharpen(
    panchromatic: str, rgb: str, out_dir: Path, compression: Compression
) -> None:
    if compression == Compression.JPEG:
        raise NotImplementedError("Needs conversion.")

    logging.info("> Pansharpening (%-progress):")
    gdal_pansharpen(
        pan_name=panchromatic,
        spectral_names=[rgb],
        dst_filename=(
            filename := out_dir / f"pansharpened-{compression.name}.tif"
        ).as_posix(),
        num_threads="ALL_CPUS",
        creation_options=[*compression.value, "TILED=YES", "BIGTIFF=YES"],
    )
    logging.info(f"> Pansharpened raster output available: {filename}")


def main(
    sourcefile: Path,
    stream: bool,
    compression: str,
    out_dir: Path,
    input_arguments: list,
    ortho=False,
):
    set_gdal_config()

    sources = (
        ortho_correct(sourcefile, stream=stream)
        if ortho
        else load_source_locations(
            sourcefile, stream=stream, input_arguments=input_arguments
        )
    )

    print(sources)
    quit()
    pansharpen(
        panchromatic=sources.images[ImageType.PANCHROMATIC].path,
        rgb=sources.images[ImageType.RGB].path,
        out_dir=out_dir,
        compression=Compression[compression],
    )


if __name__ == "__main__":
    args = parser()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s — %(levelname)s: %(message)s"
    )

    args.out.mkdir(exist_ok=True)

    main(
        sourcefile=args.file,
        stream=args.stream,
        compression=args.compression,
        out_dir=args.out,
        ortho=args.raw,
        input_arguments=[args.panchromatic, args.rgb],
    )
