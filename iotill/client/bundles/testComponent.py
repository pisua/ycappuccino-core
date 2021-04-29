

from pelix.ipopo.decorators import ComponentFactory, Validate, Invalidate, Instantiate


@ComponentFactory("Test-Factory")
@Instantiate("test")
class Application(object):
    """ test """

    def __init__(self):
        pass



    @Validate
    def validate(self, context=None):
        print("validate")

    @Invalidate
    def validate(self, context=None):
        print("invalidate")