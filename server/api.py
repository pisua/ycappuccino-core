import logging


class CFQCN(object):
    """
    CFQCN class : Ful Qualified Class Name
    """

    @staticmethod
    def build(a_classname):
        w_fqdn = '.'.join([CFQCN.__module__, a_classname])
        w_log = logging.getLogger(__name__)
        w_log.info("FQCN '{0}' ...".format(w_fqdn))
        return w_fqdn


class IActivityLogger(object):
    """ interface of generic endpoint that manage all redirection of request with specific parameter """
    name = CFQCN.build("IActivityLogger")

    def __init__(self):
        """ abstract constructor """


class IConfiguration(object):
    """
    Configuration manager.s
    """
    name = CFQCN.build("IConfiguration")

    def get(self, key):
        """
        Get configuration value.

        :param key: type: str       Configuration key.
        :return:    type: str       Configuration value, or None.
        """
        raise Exception("not implemeted")

    def has(self, key):
        """
        Determine whether a configuration exists.

        :param key: type: str       Configuration key.
        :return:    type: boolean
        """
        raise Exception("not implemeted")

    def set(self, key, value):
        """
        Set configuration value.

        :param key:     type: str   Configuration key.
        :param value:   type: str   Configuration value.
        """
        raise Exception("not implemeted")



class IConfigurable(object):
    """
    component is reconfigurable on the fly. it allow to get the current config property and ask for update the config
    """
    name = CFQCN.build("IConfigurable")

    def update_configuration(self, a_new_config_properties):
        """
        update the current config with this properties represent as a dictionnary key:value
        @param a_new_config_properties : dictionnary key->value to update to this component
        @return a boolean if the configuration is taken in account
        """
        print("not implemeted")
        return False

    def get_config_properties(self):
        """
        return the current config properties as a list
        """
        print("not implemeted")


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


class IService(object):
    """ """
    name = CFQCN.build("IService")

    def __init__(self):
        pass


class IManager(object):
    """ """
    name = CFQCN.build("IManager")

    def __init__(self):
        pass

    def get_item(self):
        pass

    def is_secure(self):
        pass

    def get_one(self, a_id):
        pass

    def get_many(self, a_params):
        pass

    def up_sert(self, a_id, a_new_field):
        pass

    def up_sert_many(self, a_params, a_new_field):
        pass

    def delete(self, a_id):
        pass

    def delete_many(self, a_params):
        pass


class IItemManager(IManager):
    """ """
    name = CFQCN.build("IItemManager")

    def __init__(self):
        super(IManager, self).__init__()



class IStorage(object):
    """"""
    name = CFQCN.build("IStorage")

    def __init__(self):
        pass

    def get_one(self, a_id, a_expand):
        pass

    def get_item(self):
        pass

    def get_many(self, a_filter, a_expand):
        pass

    def up_sert(self, a_id, a_new_fields):
        pass

    def up_sert_many(self, a_filter, a_new_fields):
        pass

    def delete(self, a_id):
        pass

    def delete_many(self, a_filter):
        pass
