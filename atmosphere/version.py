"""
Atmosphere version.
"""
from os.path import abspath, dirname
from subprocess import Popen, PIPE


VERSION = (0, 10, 0, 'prod', 0)


def git_sha():
    loc = abspath(dirname(__file__))
    try:
        p = Popen(
            "cd \"%s\" && git log -1 --format=format:%%h" % loc,
            shell=True,
            stdout=PIPE,
            stderr=PIPE
        )
        return p.communicate()[0]
    except OSError:
        return None

def get_version(form='short'):
    """
    Returns the version string.

    Takes single argument ``form``, which should be one of the following
    strings:
    
    * ``short`` Returns major + minor branch version string with the format of
    B.b.t.
    * ``normal`` Returns human readable version string with the format of 
    B.b.t _type type_num.
    * ``verbose`` Returns a verbose version string with the format of
    B.b.t _type type_num@git_sha
    * ``all`` Returns a dict of all versions.
    """
    versions = {}
    branch = "%s.%s" % (VERSION[0], VERSION[1])
    tertiary = VERSION[2]
    type_ = VERSION[3]
    type_num = VERSION[4]
    
    versions["branch"] = branch
    v = versions["branch"]
    if tertiary:
        versions["tertiary"] = "." + str(tertiary)
        v += versions["tertiary"]
    versions['short'] = v
    if form is "short":
        return v
    v += " " + type_ + " " + str(type_num)
    versions["normal"] = v
    if form is "normal":
        return v
    versions["git_sha"] = "@" + git_sha()
    v += " " + versions["git_sha"]
    versions["verbose"] = v
    if form is "verbose":
        return v
    if form is "all":
        return versions