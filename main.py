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
import argparse
import datetime


# prompt request function
class Request:
    def __init__(
        self,
        models,
        prompt,
        base_url,
        auth,
        parameters,
    ):
        self.models = models
        self.prompt = prompt
        self.url = base_url
        self.auth = auth
        self.parameters = {}
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth}",
        }

        if parameters:
            try:
                for parameter in parameters:
                    key, value = parameter.split("=", 1)
                    try:
                        corrected_value = int(value)
                    except ValueError:
                        try:
                            corrected_value = float(value)
                        except ValueError:
                            corrected_value = value
                    self.parameters[key] = corrected_value
            except ValueError:
                raise ValueError("Parameters must be in key=value format")

    def send_request(self, model):
        self.model = model
        self.payload = {
            "model": self.model,
            "prompt": self.prompt,
        }

        if self.parameters:
            self.payload.update(self.parameters)
        self.response = requests.post(self.url, headers=self.headers, json=self.payload)

        return self.response.json()


# clean the output into a dict and append it to a list of dicts
def parse_output(model_output, count, model):
    output = model_output
    run_output = {
        "model": model,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "run": count,
        "prompt": output["prompt"],
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

    model_response = {
        "model": model,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": output["content"],
    }

    data = [run_output, model_response]
    return data


def dir_maker():
    if not os.path.exists("output"):
        os.mkdir("output")

    if not os.path.exists("output/responses"):
        os.mkdir("output/responses")


def save_csv(benchmark):
    file_number = 1
    file_saved = False
    while file_saved == False:
        if os.path.exists(f"output/benchmarx_{file_number}.csv") == True:
            file_number += 1
        else:
            file_saved = True

    benchmark.to_csv(os.path.abspath(f"output/benchmarx_{file_number}.csv"))


def save_json(content, model):
    content.to_json(
        os.path.abspath(
            f"output/responses/{model}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        )
    )


def arg_parser():
    parser = argparse.ArgumentParser()
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


def main():
    dir_maker()
    benchmark = []
    args = vars(arg_parser())
    model_request = Request(**args)
    for model in model_request.models:
        count = 1
        while count < 4:
            model_output = model_request.send_request(model)
            run_output, model_response = parse_output(model_output, count, model)
            benchmark.append(run_output)
            content = model_response
            content = pd.DataFrame([content])
            save_json(content, model)
            count += 1
    benchmark = pd.DataFrame(benchmark)
    save_csv(benchmark)


if __name__ == "__main__":
    main()
