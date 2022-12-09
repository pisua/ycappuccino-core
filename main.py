import ycappuccino.core
import ycappuccino.mongo
import logging
import argparse

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Setup logs
    logging.basicConfig(level=logging.INFO)
    root_path = None
    parser = argparse.ArgumentParser(description='argument for app application')
    parser.add_argument('--root-path', type=str,  help='root path of the application')
    parser.add_argument('--port', default=5000, type=int, help='http port of the application')

    args = parser.parse_args()

    ycappuccino.core.init(root_path=args.root_path, port=args.port)
    # Run the server
    ycappuccino.core.start()

