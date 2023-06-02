# Pansharpening tool

A Python processing script which takes the panchromatic and multispectral rasters as an input, and outputs the pansharpened raster.

# Setup

1. If `GDAL` libraries are not on the system, `conda` is the simplest way to install them:

```console
$ conda env create -f pansharpening.yml
```

- If `GDAL` libraries are available, skip to step (3), but it's a good idea to create a virtual environment:

```console
$ python -m venv venv && source vevn/bin/activate # on Unix
```

2. Activate the newly created environment:

```console
$ conda activate pansharpening
```

3. From inside the directory that includes the `pyproject.toml` file:

```console
$ python -m pip install .
```

# Usage

```console
$ python -m pansharpening -h

usage: pansharpening [-h] [--stream] [--raw] [--file FILE]

Pansharpening pipeline

options:
  -h, --help            show this help message and exit
  --stream, -s          process streamed imagery and discard inputs (default: `False`)
  --compression {DEFLATE,LERC,LERC_DEFLATE,LERC_ZSTD,LZW,PACKBITS,JPEG}, -c {DEFLATE,LERC,LERC_DEFLATE,LERC_ZSTD,LZW,PACKBITS,JPEG}
                        choose the compression algorithm of the raster output (default: `LERC`)
  --raw, -r             derive from raw Pleiades Neo imagery (default: `False`)
  --out OUT, -o OUT     change the output destination directory (default: `./output`)
  --file FILE, -f FILE  TOML file input of source imagery (default: `./data/imagery-sources.toml`)
```

- By default, the raster inputs are cached to disk after the first download, but the `--stream` option changes the processing on-the-fly and discards inputs after finished:

```console
$ python -m pansharpening -s
```

- The pansharpened raster is available in the `output` directory.
- Change sources file in `data/imagery-sources.toml`, or provide another sources file using the `--file` option.
- Change the output directory of the pansharpened raster using the `--out` option.
- Alternative compression options are configurable through the `--compression` flag:

```console
$ python -m pansharpening -c PACKBITS
```
