import os
import re
# Import various utilities from utils
# import utils.html
# import utils.filters

# Path of the current file -- best not to change this
FILEPATH = os.path.dirname(os.path.abspath(__file__))

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

#################
# Substitutions #
#################

# Substitutions for the linker
SUBSTITUTIONS = [
    # Add substitutinos of the form
    # (regex, sub_function),
    # (regex, sub_function, condition),
]


# Use the following to scrape "headers"
# TOC_BUILDER should be a subclass of utils.core.TocBuilder
# TOC_BUILDER = utils.html.HeaderParser

