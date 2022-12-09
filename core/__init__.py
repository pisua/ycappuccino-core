# YCappuccino ycappuccino.core default need to have a interaction with client

import core.framework


def init(root_path=None,port=9000):
    core.framework.init(root_path, port)


def start():
    core.framework.start()
