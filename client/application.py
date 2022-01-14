

from pelix.ipopo.decorators import ComponentFactory, Validate, Invalidate, Instantiate, Requires


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

@ComponentFactory("App-Factory2")
@Instantiate("test2")
@Requires("_test", specification="App-Factory")
class Application2(object):
    """ test """

    def __init__(self):
        self._test = None
        pass

    def run(self):
        pass

    @Validate
    def validate(self, context):
        print("validate")

    @Invalidate
    def validate(self, context):
        print("invalidate")