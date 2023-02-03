import os, sys


def main(argv):
    folder = argv[1]
    for file in os.listdir(folder):
        if file.endswith(".h264"):
            filename = str(os.path.join(folder, file))
            filename_mp4 = filename[:-5] + ".mp4"
            command = "ffmpeg -r 30 -i " + filename + " -vcodec copy " + filename_mp4
            os.system(command)


if __name__ == "__main__":
    main(sys.argv)
