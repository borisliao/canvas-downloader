import argparse
from canvasapi import Canvas

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
            course_id.append(course.id)
            if args.verbose:
                print(str(course.id) + ": " + course.name)
            else:
                print(course.name)
        except AttributeError:
            if args.verbose:
                print(f"{WARNING}{course.id}: "
                      f"Course name not found{ENDC}")
            pass
        