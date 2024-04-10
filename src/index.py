import argparse

from ui.ui import UI


def main():
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("--amount", type=int, default=0)
        parser.add_argument("--room-min-size", type=int, default=2)
        parser.add_argument("--room-max-size", type=int, default=4)
        parser.add_argument("--room-exact-size", type=int, default=0)
        parser.add_argument(
            "--can-overlap", action=argparse.BooleanOptionalAction, default=False)

        parser.add_argument("--map-size-x", type=int, default=100)
        parser.add_argument("--map-size-y", type=int, default=100)
        args = parser.parse_args()
        return args

    args = parse_args()
    ui = UI()
    ui.start()


if __name__ == "__main__":
    main()
