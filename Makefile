FRONTEND_SOURCE_URL=https://raw.githubusercontent.com/digital-land/digital-land-frontend/master
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
DOCS_DIR=./docs/

all: clean render

init:
	pip3 install --upgrade -r requirements.txt


server:
	cd docs && python3 -m http.server


render:
	python3 bin/render.py


clean::
	rm -rf $(DOCS_DIR)
	mkdir -p $(DOCS_DIR)
	
	
commit-docs::
	git add docs
	git diff --quiet && git diff --staged --quiet || (git commit -m "Rebuilt docs $(shell date +%F)"; git push origin $(BRANCH))
