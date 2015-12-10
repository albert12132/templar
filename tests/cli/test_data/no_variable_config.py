# A valid config file must contain a variable called 'config' that is a Config
# object.

from templar.api.config import ConfigBuilder
configuration = ConfigBuilder().build()
