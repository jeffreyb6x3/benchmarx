# benchmarx
an llm open-weight model benchmarking script written in python



## installation
1) clone this repo
2) install requirements.txt
    recommended: use a venv with uv. conda, containers, or rawdogging it into your system interpreter will also work I guess
3) run main.py with appropriate arguments

### requirements
python 3.14 or newer
    - see requirements.txt for further python requirements
    - or just install it without reading it. Be honest, that's what you were going to do anyway
llama.cpp openai compatible api
    - note: this may or may not work for other-than-llama.cpp providers. this script relies on exactly the output json llama.cpp and hasn't been tested with other providers including cloud providers as it is intended for benchmarking local models



## use
with benchmarx installed and llama.cpp running you will also need to know:
    - the names of the models you wish to benchmark according to llama.cpp
    - the port and url for your llama.cpp instance
run main.py with the names of the models you are testing as the primary arguments, separated by comments. Optional arguments:
    --prompt (default="Define the events of the clone wars from a marxist dialectcal materialist perspective.")
    --base_url (default="http://localhost:2026/completion") #note this is not the standard llama.cpp default port, you will likely want to ajust this to port 8080 in 'main.py' or set it for each run
    --parameters $[key=value] #pass extra parameters here
        some example parameters:

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
git clone [repo-url] \
uv venv .venv \
uv pip install requirements.txt
```

use:
```
python main.py GLM-4.7-Flash-GGUF Qwen3-32B-GGUF gpt-oss-120b-GGUF --base_url http://localhost:8080/completion --parameters n_predict=2024 stream=False
```
