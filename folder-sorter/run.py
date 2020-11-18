from os import listdir, mkdir
from os.path import isfile, join, isdir, join, exists
from shutil import move

inpath = input("Please enter text path to be sorted: ")
ingrouped = input("Group similar file types (y/n): ")
grouped = ingrouped[0] if ingrouped else "n"

groupings = {
    "documents": ["pdf", "txt", "csv"],
    "executables": ["dmg", "pkg"],
    "images": ["jpg", "jpeg", "png", "svg"]
}

if (isdir(inpath)):
    files = [f for f in listdir(inpath) if isfile(join(inpath, f))]

    print("Found {} files to be sorted".format(len(files)))
    for filename in files:
        fname_split = filename.split(".")
        ext = fname_split[len(fname_split)-1]

        targetpath = join(inpath, ext)
        if fname_split[0] == "":
            # dot files are hidden by default on osx, so this will be a visible
            # hidden folder with no visibile items in it. :D
            targetpath = join(inpath, "hidden")

        if grouped.lower() == "y":
            for grouping_folder, grouping_exts in groupings.items():
                if ext in grouping_exts:
                    targetpath = join(inpath, grouping_folder)
                    break

        if isdir(targetpath) == False:
            mkdir(targetpath)

        dst_filepath = join(targetpath, filename)
        if exists(dst_filepath):
            i = 1
            while True:
                tmp_filename = fname_split[0] + "_" + str(i) + "." + ext
                if not exists(join(targetpath, tmp_filename)):
                    print("renaming {} to {}".format(filename, tmp_filename))
                    dst_filepath = join(targetpath, tmp_filename)
                    break
                i += 1

        move(join(inpath, filename), dst_filepath)

    if len(files) > 0:
        print("Completed sorting files!")
else:
    print("Invalid directory given at ` {} `. Please verify and try again.".format(inpath))
