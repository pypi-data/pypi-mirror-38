import os
import sys
import pkg_resources

__version__ = pkg_resources.require("esrally")[0].version

# Allow an alternative program name be set in case Rally is invoked a wrapper script
PROGRAM_NAME = os.getenv("RALLY_ALTERNATIVE_BINARY_NAME", os.path.basename(sys.argv[0]))


if __version__.endswith("dev0"):
    DOC_LINK = "https://esrally.readthedocs.io/en/latest/"
else:
    DOC_LINK = "https://esrally.readthedocs.io/en/%s/" % __version__

BANNER = r"""
    ____        ____
   / __ \____ _/ / /_  __
  / /_/ / __ `/ / / / / /
 / _, _/ /_/ / / / /_/ /
/_/ |_|\__,_/_/_/\__, /
                /____/
"""


SKULL = '''
                 uuuuuuu
             uu$$$$$$$$$$$uu
          uu$$$$$$$$$$$$$$$$$uu
         u$$$$$$$$$$$$$$$$$$$$$u
        u$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$"   "$$$"   "$$$$$$u
       "$$$$"      u$u       $$$$"
        $$$u       u$u       u$$$
        $$$u      u$$$u      u$$$
         "$$$$uu$$$   $$$uu$$$$"
          "$$$$$$$"   "$$$$$$$"
            u$$$$$$$u$$$$$$$u
             u$"$"$"$"$"$"$u
  uuu        $$u$ $ $ $ $u$$       uuu
 u$$$$        $$$$$u$u$u$$$       u$$$$
  $$$$$uu      "$$$$$$$$$"     uu$$$$$$
u$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$
$$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"
"""      ""$$$$$$$$$$$uu ""$"""
uuuu ""$$$$$$$$$$uuu
u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$
$$$$$$$$$$""""           ""$$$$$$$$$$$"
   "$$$$$"                      ""$$$$""
     $$$"                         $$$$"
'''


def check_python_version():
    if sys.version_info.major != 3 or sys.version_info.minor < 4:
        raise RuntimeError("Rally requires at least Python 3.4 but you are using:\n\nPython %s" % str(sys.version))
