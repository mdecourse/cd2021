import os

"""CMSimfly Initialization setup
"""

# get current directory, on Windows, back slash at the end of the directory
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# config directory
config_dir = _curdir + "/config/"
class Init(object):
    # uwsgi as static class variable, can be accessed by Init.uwsgi
    uwsgi = False
    site_title = "CMSiMDE"
    #ip = "127.0.0.1"
    ip = "::"
    port = 9443
    def __init__(self):
        # hope to create downloads and images directories　
        if not os.path.isdir(_curdir + "/downloads"):
            try:
                os.makedirs(_curdir + "/downloads")
            except:
                print("mkdir error")
        if not os.path.isdir(_curdir + "/images"):
            try:
                os.makedirs(_curdir + "/images")
            except:
                print("mkdir error")


