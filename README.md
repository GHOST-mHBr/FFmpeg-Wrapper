# FFmpeg-Wrapper
If you have downloaded a course and want to compress all videos inside it, you can use this python script

## Prerequisites
You need FFmpeg as the compressor and the following python 3rd-party modules:
* termcolor

## How it works?
The script first searches and finds all `*.mp4` files. Keep in mind  that it just works with `mp4` and if you want to change it, you can read the script and change that.
Then, it will compress them and store the converted files in this format `<origianl_name>-comp.mp4`. So note that your origianl videos shouldn't have this format ('<something>-comp.mp4') for their names. 
Finally the script checks if there is a compressed with the same length as the origianal file and if so, it will __REMOVE__ the original video. You can disable this with `--no-remove` option.

Note that if you terminate the script using SIGINT signal (by pressing ctrl+c for example), it will remove the video that was converting.

## Running the script
To run the script you need to clone the repo or copy the script.
If you prefer to cloen it, run this:
```bash
> git clone https://github.com/GHOST-mHBr/FFmpeg-Wrapper && cd FFmpeg-Wrapper
```
After that, enter the following command:
```bash
> python3 comp.py <PATH>
```

There is some options you can use:
```bash
> python3 comp.py -h
```
```
usage: RecurVidComp [-h] [--no-confirm] [--ffmpeg-args FFMPEG_ARGS]
                    [--no-remove]
                    path

A python script that scans and compresses all video file of a directory with
recursive searching

positional arguments:
  path                  The start path for searching and converting

options:
  -h, --help            show this help message and exit
  --no-confirm          Disables confirmation for each convertion. default is
                        false
  --ffmpeg-args FFMPEG_ARGS
                        Any additional argument to pass to ffmpeg.
  --no-remove           Disable removing the origianl video after compression.
                        default is false
```
