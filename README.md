## FLAC->MP3 converter

### Overview

A simple script to convert a directory of FLAC files to a directory of MP3 files.

### Requirements

* Python 2.7
* ffmpeg compiled with `--enable-libmp3lame`


### Usage

    convert-flac.py [-i indir] [-o outdir] [-b bitrate] [--ffmpeg=FFMPEG]

Where:

    -i indir            input directory
    -o outdir           output directory
    -b bitrate          output bitrate (in kbits/s)
    --ffmpeg=FFMPEG     which ffmpeg to use
