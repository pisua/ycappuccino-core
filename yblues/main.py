import ycappuccino.core
import ycappuccino.mongo
import logging
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Setup logs
    logging.basicConfig(level=logging.INFO)

    ycappuccino.core.init()
    # Run the server
    ycappuccino.core.start()

