PY ?= python

.PHONY: install run test safety-check install-hooks verify

install:
	$(PY) -m pip install -r requirements.txt

run:
	$(PY) -m uvicorn app.main:app --reload

test:
	$(PY) -m pytest -q

safety-check:
	$(PY) scripts/safety_check.py

install-hooks:
	$(PY) scripts/install_git_hooks.py

verify: test safety-check
