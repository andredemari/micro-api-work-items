.PHONY: install run test safety-check install-hooks

install:
	python -m pip install -r requirements.txt

run:
	python -m uvicorn app.main:app --reload

test:
	python -m pytest -q

safety-check:
	python scripts/safety_check.py

install-hooks:
	python scripts/install_git_hooks.py
