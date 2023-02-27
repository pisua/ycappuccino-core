#app="all"

from ycappuccino.core.api import CFQCN



class IClientIndexPath(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IClientIndexPath")

    def __init__(self):
        """ abstract constructor """
        pass

class IJwt(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IJwt")

    def __init__(self):
        """ abstract constructor """
        pass
class IJwtRightAccess(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("IJwtRightAccess")

    def __init__(self):
        """ abstract constructor """
        pass


class IEndpoint(object):
    """ interface of generic endpoint that manage all redirection of request with specific parameter """
    name = CFQCN.build("IEndpoint")

    def __init__(self):
        """ abstract constructor """

    def post(self, a_item_id, a_header, a_params, a_body):
        pass

    def put(self, a_item_id, a_header, a_params, a_body):
        pass

    def get(self, a_item_id, a_header, a_params):
        pass

    def delete(self, a_item_id, a_header, a_params):
        pass


class IHandlerEndpoint(object):
    """ interface of generic endpoint that manage all redirection of request with specific parameter """
    name = CFQCN.build("IHandlerEndpoint")

    def __init__(self):
        """ abstract constructor """

    def get_types(self):
        pass

    def post(self, a_item_id, a_header, a_params, a_body):
        pass

    def put(self, a_item_id, a_header, a_params, a_body):
        pass

    def get(self, a_item_id, a_header, a_params):
        pass

    def delete(self, a_item_id, a_header, a_params):
        pass
