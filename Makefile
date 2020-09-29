FRONTEND_SOURCE_URL=https://raw.githubusercontent.com/digital-land/digital-land-frontend/master

all: clean render

init:
	pip3 install --upgrade -r requirements.txt


server:
	cd docs && python3 -m http.server


render:
	python3 bin/render.py


clean:
	rm -rf docs/