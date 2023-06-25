SHELL := /bin/bash

.SILENT:

.PHONY: help
.DEFAULT_GOAL := help
help:  ## Prints all the targets in all the Makefiles
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: list
list:  ## List all make targets
	@${MAKE} -pRrn : -f $(MAKEFILE_LIST) 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | sort

###############################
### Script Specific Targets ###
###############################

## TODO: Parameterize
.PHONY: prepare_db
prepare_db:  ## Prepare the vectorized db
	python3 prepare_db.py

## TODO: Parameterize
.PHONY: query_db
query_db:  ## Query the vectorized db
	python3 query_db.py

.PHONY: streamlit_app
streamlit_app:  ## Run the streamlit app
	streamlit run streamlit_app.py

####################
### Data Targets ###
####################

.PHONY: download_vitalik_articles
download_vitalik_articles:  ## Download vitalik's articles
	python3 data_helpers/vitalik_to_pdf.py

# https://github.com/JustAnotherArchivist/snscrape
.PHONY: download_twitter_user_tweets ## Download twitter user tweets (user=)
download_twitter_user_tweets:
	snscrape --jsonl --max-results 10000 twitter-user $(user) > data/$(user).json

##########################
### Env Common Targets ###
##########################

.PHONY: env_create
env_create:  ## Create the env; must be execute like so: $(make env_create)
	python3 -m venv venv

.PHONY: env_source
env_source:  ## Source the env; must be execute like so: $(make env_source)
	@echo 'source venv/bin/activate'

##########################
### Pip Common Targets ###
##########################

.PHONY: pip_freeze
pip_freeze:  ## Freeze the pip requirements
	pip freeze > requirements.txt

.PHONY: pip_install
pip_install:  ## Install the pip requirements
	pip install -r requirements.txt

#############################
### Python Common Targets ###
#############################

.PHONY: py_format
py_format:  ## Format the python code
	black .
	isort .