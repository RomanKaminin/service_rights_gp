all: finale
    finale: install-requirements run-server

install-requirements:
	pip3 install -r service/requirements.txt

run-server:
	python3 server.py



