"""
    to test example - run:

        python prog_with_cli.py sleep 3

        or

        python prog_with_cli.py play boogie

        or to get help:

        python prog_with_cli.py -h

"""

import os
from clifier import clifier


def main():
    # get abs path to config file
    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "cli.yaml")

    # initialise clifier
    cli = clifier.Clifier(config_path, prog_version="0.0.1")

    # create parser
    parser = cli.create_parser()
    args = parser.parse_args()

    # args - object with command line args from user input
    # put your logic here
    print(args)
    if 'game' in args:
        print("We will play a game: {}".format(args.game))
        if args.count:
            num = int(args.count)
            for i in range(1, num+1):
                print("Play {} time{}!".format(
                    i, "s" if i > 1 else ""))

    if 'time' in args:
        import time
        sleep_time = int(args.time)
        for i in range(0, sleep_time+1):
            if i == sleep_time:
                print("Wake up!")
            else:
                print("Sleep {} seconds".format(sleep_time - i))
                time.sleep(0.9)


if __name__ == "__main__":
    main()
