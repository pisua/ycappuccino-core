

from pelix.ipopo.decorators import ComponentFactory, Validate, Invalidate, Instantiate


@ComponentFactory("App-Factory")
@Instantiate("test")
class Application(object):
    """ test """

    def __init__(self):
        pass

    def run(self):
        pass

    @Validate
    def validate(self, context):
        print("validate")

    @Invalidate
    def validate(self, context):
        print("invalidate")