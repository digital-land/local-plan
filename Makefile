FRONTEND_SOURCE_URL=https://raw.githubusercontent.com/digital-land/digital-land-frontend/master

all: clean render

init: base-files
	pip3 install --upgrade -r requirements.txt


base-files:
	curl -qsL '$(FRONTEND_SOURCE_URL)/application/templates/base.html' > templates/base.html
	curl -qsL '$(FRONTEND_SOURCE_URL)/application/templates/dlf-base.html' > templates/dlf-base.html


server:
	cd docs && python3 -m http.server


render:
	python3 bin/render.py


clean:
	rm -rf docs/