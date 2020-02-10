import argparse
from canvasapi import Canvas
from pathlib import Path
from urllib.request import urlretrieve
from threading import Thread
# from urllib.parse import unquote

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser()

parser.add_argument("api", help="API key of a Canvas account")
parser.add_argument("url", help="url of the canvas page")
parser.add_argument("-v", "--verbose", action="count",
                    help="prints potential errors")
parser.add_argument("-c", "--courseid", nargs='+',
                    help="accepts one or many course id's to be selected from")

args = parser.parse_args()
canvas = Canvas(args.url, args.api)

course_id = []

# Get all courseid's
if args.courseid:
    course_id = args.courseid
    pass
else:
    for course in canvas.get_courses():
        try:
            if args.verbose:
                print(str(course.id) + ": " + course.name)
            else:
                print(course.name)
            course_id.append(course.id)
        except AttributeError:
            if args.verbose:
                print(f"{WARNING}{course.id}: "
                      f"Course name not found{ENDC}")


# Recursivly download files from given Folder and the list:directory
def file_dl(folder, dir):
    for folder in folder.get_folders():
        file_dl(folder, f"{dir}{folder.name}/")
    Path(dir).mkdir(parents=True, exist_ok=True)
    for file in folder.get_files():
        if not Path(dir + file.display_name).is_file():
            print(dir + file.display_name)
            Thread(target=urlretrieve,
                   args=(file.url, dir+file.display_name)).start()
        else:
            print(WARNING + "Skipped " + dir + file.display_name + ENDC)


for id in course_id:
    course = canvas.get_course(id)
    print(course.name)

    root_folder = None
    for folder in course.get_folders():
        if folder.name == "course files":
            root_folder = folder
            break

    if root_folder is None:
        print(f"{FAIL}  Cannot find the root folder{ENDC}")
    else:
        try:
            file_dl(root_folder, f"Courses/{course.name}/")
        except Canvas.exceptions.Unauthorized as e:
            print(f"{FAIL}  Cannot access files: {e}{ENDC}")
