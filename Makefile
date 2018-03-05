all: venv
	@echo "Need to run 'source venv/bin/activate' to activate virtualenv"
	@echo "Then, you can use 'python to_spotify.py'"

venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

