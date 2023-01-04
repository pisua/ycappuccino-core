# YCappuccino ycappuccino.core default need to have a interaction with client

import ycappuccino.core.framework


def init(root_path=None, app=None, port=9000):
    ycappuccino.core.framework.init(root_path, app, port)


def start():
    ycappuccino.core.framework.start()
