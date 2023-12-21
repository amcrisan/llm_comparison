# Getting started

Requires pipenv to be installed. Running these notebooks doesn't require access to any particular hardware, but you will need to set up an OpenAI/Hugging account and get your own API keys. 

To get started installing dependencies, run:
```bash
pipenv install --dev
```

**Jupyter Notebook**

To set up the Jupyter notebook kernel run:

```bash
python -m ipykernel install --user --name=my-virtualenv-name
```

a notebook can be run in vscode, but the dev install also includes Jupyter lab so you can also run:

```bash
pipenv run notebook
```

There are two notebooks that can be run. ```llm_responses.ipynb``` is very much scratch notes, working out ideas. I've retained it because it goes a little more deeply into methods and it might be useful to someone else thinking through some similar problems. A cleaned-up version is ```llm_responses_with_library.iynb``` which uses the code from llm_comparison. 

**Running streamlit app**

```bash
pipenv run app
```

# Setting up the environment

You'll need your own API codes to access the OpenAI methods and to use the HuggingFace inference endpoints. There is a template for a .env file that runs with this notebook. 