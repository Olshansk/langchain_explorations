# Langchain Explorations <!-- omit in toc -->

https://twitter.com/olshansky/status/1672827218563850240

- [Getting started](#getting-started)
  - [Prepare Your Secrets](#prepare-your-secrets)
  - [Option 1: Vitalik Articles (default)](#option-1-vitalik-articles-default)
  - [Option 2: Your data (custom)](#option-2-your-data-custom)
  - [Your own data](#your-own-data)
  - [Private Data](#private-data)
- [References \& Resources](#references--resources)
  - [Startup Stack to easily productionize](#startup-stack-to-easily-productionize)
- [Future Work / TODO / Improvements](#future-work--todo--improvements)

## Getting started

### Prepare Your Secrets

1. Get your OpenAI key from [here](https://platform.openai.com/account/api-keys); make sure you're logged in
2. Get your PinconeAI key from [here](https://app.pinecone.io/organizations/); make sure you're logged in
3. Create an index called `my-index` or `vitalik-index` as showing [here](https://github.com/Olshansk/langchain_explorations/assets/1892194/95e72119-525f-4f66-9ded-c210fb6f2df2) depending on which option you choose below

```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

Update the env vars appropriately.

### Option 1: Vitalik Articles (default)

Start the virtual environment and install the requirements:

```bash
$(make env_source)
make pip_install
```

Download Vitalik's articles

```bash
make download_vitalik_articles
```

Create the embeddings and upload them to Pinecone

### Option 2: Your data (custom)

Start the virtual environment and install the requirements:

```bash
$(make env_source)
make pip_install
```

Get your pdfs and put them in `./data/my_data`

Prepare the database with your pdfs

```bash
# DATADIR and INDEX_NAME are customizable but you can start with the defaults if you don't know what you're doing yet
make prepare_db DATADIR=data/my_data INDEX_NAME=my-index
```

### Your own data

### Private Data

## References & Resources

1. Initial reference for this repo: https://blog.bytebytego.com/p/how-to-build-a-smart-chatbot-in-10
2. Langchain docs: https://python.langchain.com/
3. A full book I haven't read yet: https://www.pinecone.io/learn/langchain-intro/
4. OpenAI API: https://beta.openai.com/docs/introduction

### Startup Stack to easily productionize

- Easily host infra: fly.io or render.com
- Easily deploy WIP app in python: https://streamlit.io/generative-ai
- Building a backend API w/ nothing: https://github.com/fern-api/fern

## Future Work / TODO / Improvements

- [ ] Notion - Add support for pulling data from notion
- [ ] Twitter - Use user tweet accounts to do this as well
- [ ] OpenAI - Use the OpenAI Chat Completion API directly
- [ ] Pinecone - Need to be able to update existing index
