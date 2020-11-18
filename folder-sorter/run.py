from os import listdir, mkdir
from os.path import isfile, join, isdir, join
from shutil import move

inpath = input("Please enter text path to be sorted: ")
files = [f for f in listdir(inpath) if isfile(join(inpath, f))]

print("Found {} files to be sorted".format(len(files)))
for filename in files:
    ext = filename.split(".")[1]
    targetpath = join(inpath, ext)
    if isdir(targetpath) == False:
        mkdir(targetpath)

    move(join(inpath, filename), targetpath)
