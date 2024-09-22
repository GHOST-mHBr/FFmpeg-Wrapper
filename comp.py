import glob
import sys
import os
import subprocess
from termcolor import cprint, colored
import signal
import re
import argparse

# cprint("Hello!")
compname=""
fullname=""
videoName=""

def cleanUp():
    if os.path.isfile(compname) and os.path.isfile(videoName) and round(get_len(compname)) != round(get_len(videoName)):
        cprint("\nCleaning up...", "yellow")
        os.remove(compname)

        
def get_len(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of",
                        "default=noprint_wrappers=1:nokey=1", filename],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    if result.returncode != 0:
        cprint(f"Error calculating length of the video:", "red")
        cprint(filename)
        # cprint(f"Here is the stderr of ffmpeg:", "red")
        # cprint(result.stderr)
        # cprint(f"And here is the stdout of ffmpeg:", "red")
        # cprint(result.stdout)
        cleanUp()
        cprint("Quiting", "red")
        exit(-1)
    
    return float(result.stdout)


def sigint_handler(sig, frame):    
    cleanUp()
    cprint("\nQuiting", "red")
    sys.exit(0)


argparser = argparse.ArgumentParser(prog="RecurVidComp", description="A python script that scans and compresses all video file of a directory with recursive searching")
argparser.add_argument("--no-confirm", action="store_true", help="Disables confirmation for each convertion.\ndefault is false", required=False)
argparser.add_argument("--ffmpeg-args",type=str, action="store", help = "any additional argument to pass to ffmpeg.")
argparser.add_argument("path", action="store", help="The start path for searching and converting")
args = argparser.parse_args()
directory = args.path
# print(directory)
# exit(-1)
commands = str(args.ffmpeg_args)
no_conf = args.no_confirm
# print(no_conf)
# exit(-1)

signal.signal(signal.SIGINT, sigint_handler)

videos = glob.glob(f'{directory}/**/*.mp4', recursive=True)
filesToCompress = list(filter(lambda x : not re.match(".*-comp.mp4",x) , videos))

numOfAll = len(videos)
numOfUncompressed = len(filesToCompress)
numOfCompressed = numOfAll - numOfUncompressed

cprint(f"Found {numOfUncompressed} files to compress and {numOfCompressed} compressed files", "green")
# exit(-1)
for video in filesToCompress:
    videoName = video
    fullname = video.split("/")[-1]
    basenameList = video.split(".")
    basename = ".".join(basenameList[0:len(basenameList)-1])
    # print(basename)
    # exit(-1)
    compname = f'{basename}-comp.mp4'
    txt = colored('Processing', "yellow")
    txt += f' "{video}"'
    cprint(txt)

    if not no_conf:
        print("continue?[y/n]:", end="")
        res=input()
    else:
        res="y"

    if res == "y":
        if len(commands) < 0:
            fres=subprocess.run(["ffmpeg", "-i", video, commands, compname],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            fres=subprocess.run(["ffmpeg", "-i", video, compname], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            
        if fres.returncode == 0:
            if os.path.isfile(compname) and round(get_len(compname)) == round(get_len(video)):
                os.remove(video)
                numOfCompressed += 1
                numOfUncompressed -= 1
                cprint("Done processing", "green")
                cprint(f"{numOfCompressed} videos from {numOfAll} converted successfully ({round(100*numOfCompressed/numOfAll)}%)\n" , "green")
            else:
                cprint(f'WARNING: It seems like there is a problem with this file: \n"{video}"\nSince the available compressed file and the origianl one have different durations.\nConsider removing converted or the original one.\nSkipping for now!',"yellow")
        else:
            cprint(f"ffmpeg error\nstdout: {fres.stdout}\nstderr: {fres.stderr}\n")
            
    elif res=="n":
        cprint("Skipped", "blue")
