import argparse


def arg_parser():
    parser = (
        argparse.ArgumentParser()
    )  # calls an instance of the argparse.ArgumentParser
    parser.add_argument("models", nargs="+")
    parser.add_argument(
        "--prompt",
        default="Describe the events of the clone wars from a marxist dialectical materialist perspective.",
        nargs="?",
    )
    parser.add_argument(
        "--base_url", default="http://localhost:2026/completion", nargs="?"
    )
    parser.add_argument("--auth", default="password123", nargs="?")
    parser.add_argument("--parameters", nargs="*")

    return parser.parse_args()


args = vars((arg_parser()))
print(args)

test_list = args["parameters"]
print(test_list)

test_dict = dict(parameter.split("=") for parameter in test_list)
print(test_dict)

second_dict = {"x": 11, "y": 12}
second_dict.update(test_dict)
print(second_dict)
