import os
import re

# Path of the current file -- best not to change this
FILEPATH = os.path.dirname(os.path.abspath(__file__))

#################
# Substitutions #
#################

# Substitutions for the linker
SUBSTITUTIONS = [
    # Add substitutinos of the form
    # (regex, sub_function),
]


# Use the following to scrape "headers"
# header_regex = re.compile(r"")
# def header_translate(match):
#     pass
# def table_of_contents(headers):
#     pass

#############
# Templates #
#############

# List of directories in which to search for templates
TEMPLATE_DIRS = [
    FILEPATH,
    # Add directories that contain templates
    # os.path.join(FILEPATH, 'example'),
]

# Variables that can be used in templates
VARIABLES = {
    # Add variables here, like the following
    # 'example': 'something here',
}
