from .version import Version
from .git import head_tag_description
try:
    from .__version__ import VERSION
except:
    VERSION='unknown'
