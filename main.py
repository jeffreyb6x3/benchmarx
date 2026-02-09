# a benchmarking script for local llms using llama.cpp

#outline:
#args to pass any number of models and sampling_params
#function to build and send prompt to model using request module
#record the responses and metrics to a .csv file using pandas
#repeat 3x per model and config

# If offline:
#   Start a local OpenAI-compatible server with a web UI:
#   llama-server -hf QuantFactory/Qwen2.5-Coder-1.5B-Instruct-GGUF:Q4_K_M
#   port 8080

import pandas
import requests
import time
import json
import argparse

# prompt request function
class Request:
    def __init__(self, models="GLM-4.7-Flash", n_ctx="8000", prompt="hello world", base_url="http://trampinheavy:2220/v1", commands=""):
       self.models = arg_parser().models
       self.n_ctx = arg_parser().n_ctx
       self.prompt = arg_parser().prompt
       self.url = arg_parser().base_url
       self.commands = arg_parser().commands

    def send_request(self, model):
        print(
        f"""Model: {model}
        Context Length: {self.n_ctx}
        Prompt: {self.prompt}
        Commands: {self.commands}
        URL: {self.url}"""
        )
    
    
#arg_parse function to pass args to the send_request function
def arg_parser():
    parser = argparse.ArgumentParser() #calls an instance of the argparse.ArgumentParser
    parser.add_argument('models', nargs='+')
    parser.add_argument('--n_ctx', nargs='?')
    parser.add_argument('--prompt', nargs='?')
    parser.add_argument('--base_url', nargs='?')
    parser.add_argument('--commands', nargs='*')
    parser.parse_args()

    return parser.parse_args()

# sends a request for each model arg passed in args 3 times
def main():
    args = arg_parser()
    model_request = Request(args)
    for model in model_request.models:
        count = 0
        request_count = 1
        while count <3:
            model_request.send_request(model)
            #print(arg_parser())
            count += 1

#main
if __name__ == '__main__':
    main()
