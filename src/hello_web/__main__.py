"""Run the local learning server."""

import os

from hello_web.app import create_app


def main():
    create_app().run(
        host="0.0.0.0",
        port="5001",
        debug=False,
    )


if __name__ == "__main__":
    main()
