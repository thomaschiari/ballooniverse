# ballooniverse

Unnecessarily complex artificial intelligence chain created to generate a simple balloon popping game that runs in the browser.

The chain works better with reasoning models like `deepseek-reasoner` or `gemini-2.5-pro-exp-03-25` or you can implement a chain of thought using the system prompt (•‿•)

## How it works

The chain is a series of tools that are used to generate the game code and save it as a html file.

## How to run
First complete the `.env` file with your API keys just like the `.env.example` file.

Then run the script.
```bash
pip install -r requirements.txt
python main.py
```

## How to play

Open the `index.html` file in your browser.