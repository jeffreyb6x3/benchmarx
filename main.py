# a benchmarking script for local llms using llama.cpp

# outline:
# args to pass any number of models and sampling_params
# function to build and send prompt to model using request module
# record the responses and metrics to a .csv file using pandas
# repeat 3x per model and config

# If offline:
#   Start a local OpenAI-compatible server with a web UI:
#   llama-server -hf QuantFactory/Qwen2.5-Coder-1.5B-Instruct-GGUF:Q4_K_M
#   port 8080

import pandas as pd
import requests
import os
from pathlib import Path
import argparse


# prompt request function
class Request:
    def __init__(
        self,
        models,
        n_ctx,
        prompt,
        base_url,
        n_predict,
        commands,
    ):
        self.models = models
        self.n_ctx = int(n_ctx)
        self.prompt = prompt
        self.url = base_url
        self.n_predict = n_predict
        self.commands = commands
        self.headers = {"Content-Type": "application/json"}

    def send_request(self, model):
        self.model = model
        self.payload = {
            "model": self.model,
            "prompt": self.prompt,
            "n_ctx": self.n_ctx,
            "n_predict": self.n_predict,
        }

        self.response = requests.post(self.url, headers=self.headers, json=self.payload)
        return self.response.json()


# cleab the output into a dictt and append it to a list of dicts
def parse_output(model_output, count, model):
    output = model_output
    run_output = {
        "model": model,
        "run": count,
        "prompt": output["prompt"],
        "content": output["content"],
        "tokens_predicted": output["tokens_predicted"],
        "tokens_evaluated": output["tokens_evaluated"],
        "temperature": output["generation_settings"]["temperature"],
        "top_k": output["generation_settings"]["top_k"],
        "top_p": output["generation_settings"]["top_p"],
        "n_predict": output["generation_settings"]["n_predict"],
        "prompt_ms": output["timings"]["prompt_ms"],
        "prompt_per_second": output["timings"]["prompt_per_second"],
        "predicted_n": output["timings"]["predicted_n"],
        "predicted_ms": output["timings"]["predicted_ms"],
        "predicted_per_second": output["timings"]["predicted_per_second"],
    }
    return run_output


def save_csv(record):
    file_number = 1
    file_saved = False
    while file_saved == False:
        if os.path.exists(f"output/benchmarx_{file_number}.csv") == True:
            file_number += 1
        else:
            file_saved = True

    record.to_csv(os.path.abspath(f"output/benchmarx_{file_number}.csv"))


# arg_parse function to pass args to the send_request function
def arg_parser():
    parser = (
        argparse.ArgumentParser()
    )  # calls an instance of the argparse.ArgumentParser
    parser.add_argument("models", nargs="+")
    parser.add_argument("--n_ctx", default=8000, nargs="?")
    parser.add_argument(
        "--prompt",
        default="Define the events of the clone wars from a marxist dialectical materialist perspective.",
        nargs="?",
    )
    parser.add_argument(
        "--base_url", default="http://localhost:2026/completion", nargs="?"
    )
    parser.add_argument("--n_predict", default=-1, nargs="?")
    parser.add_argument("--commands", default="", nargs="*")

    return parser.parse_args()


# sends a request for each model arg passed in args 3 times, appends its parsed output as a dict to a list, and returns that list of dicts as a dataframe.
def main():
    record = []
    args = vars(arg_parser())
    model_request = Request(**args)
    for model in model_request.models:
        count = 1
        while count < 4:
            model_output = model_request.send_request(model)
            # print(arg_parser())
            record.append(parse_output(model_output, count, model))
            count += 1
    record = pd.DataFrame(record)
    save_csv(record)


# main
if __name__ == "__main__":
    main()
