from templar.api.config import ConfigBuilder

import os.path

config = ConfigBuilder().add_template_dirs(os.path.dirname(__file__)).build()
