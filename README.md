# benchmarx
an open-weight llm benchmarking script written in python for use with llama.cpp<br>

#this is a learning project, even posting it publicly is about learning. I am interested in any input from experienced developers. None of the code in this repo was created by machine inference "AI", despite the subject matter being explicitly llm related.

## what does this do?
In short, this lets you call any number of llms for inference via llama.cpp using the same settings for every run. The script will run each model 3 times and record all the results. Benchmark tables will be saved in /output. Actual model responses are each saved separately with a timestamp and model name in /output/responses. I may find a better way to store responses for comparison later - but model output quality is qualitative and requires manual human work at present so I am working to prioritize that.

## installation
1) clone this repo<br>
2) install requirements.txt<br>
    recommended: use a venv with uv. If that's unclear, research python virtual environments<br>
3) run main.py with appropriate arguments<br>

### requirements
python 3.14 or newer<br>
    - see requirements.txt for further python requirements<br>
llama.cpp<br>
    - this is not compatible with other openai apis as it uses the "completion" api. this is because I had trouble getting llama.cpp to work with more recent openai standards and the /completion endpoint is known and working with all the flags I needed. If you understand the api better than I do please submit a PR or hit my inbox<br>



## use
with benchmarx installed and llama.cpp running you will also need to know:<br>
    - the names of the models you wish to benchmark according to llama.cpp<br>
    - the port and url for your llama.cpp instance<br>
run main.py with the names of the models you are testing as the primary arguments, separated by comments. Optional arguments:<br>
    --prompt (default="Define the events of the clone wars from a marxist dialectcal materialist perspective.")<br>
    --base_url (default="http://localhost:2026/completion") #note this is not the standard llama.cpp default port, you will likely want to ajust this to port 8080 in 'main.py' or set it for each run<br>
    --parameters $[key=value] #pass extra parameters here<br>
        some example parameters:<br>

            n_predict 	    integer     Maximum tokens to generate
            temperature 	float 	    Sampling temperature (0.0-2.0)
            top_k 	        integer 	Top-k sampling
            top_p 	        float 	    Top-p (nucleus) sampling
            min_p 	        float 	    Minimum probability threshold
            repeat_penalty 	float 	    Repetition penalty (1.0 = no penalty)
            repeat_last_n 	integer 	Last n tokens to penalize
            penalize_nl 	boolean 	Penalize newline tokens
            stop 	        array 	    Stop sequences
            stream 	        boolean 	Enable streaming response
            seed 	        integer 	Random seed (-1 = random)
            grammar     	string 	    GBNF grammar for constrained output

### examples
installation:
```
git clone http://github.com/jeffreyb6x3/benchmarx \
uv venv .venv \
source .venv/bin/activate \
uv pip install requirements.txt
```

use:
```
python main.py GLM-4.7-Flash-GGUF Qwen3-32B-GGUF gpt-oss-120b-GGUF --base_url http://localhost:8080/completion --parameters n_predict=2024 stream=False
```

## future project goals
1) Remain compatible with llama.cpp updates<br>
2) Add support for more configuration options including number of runs or making every run "cold"<br>
3) Add support for other endpoints.
4) Move certain default settings to a config file for beter ux
