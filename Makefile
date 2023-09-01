nvenv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt
run:
	venv/bin/python main.py
update-packages:
	venv/bin/pip install --upgrade -r requirements.txt