from pelix.ipopo.decorators import ComponentFactory, Validate, Invalidate, Instantiate

@ComponentFactory("App-Factory")
@Instantiate("test")
class Application():
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

import sys
import inspect

print(inspect.getmembers(sys.modules[__name__], inspect.isclass))

