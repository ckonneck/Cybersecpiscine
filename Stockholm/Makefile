VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

.PHONY: venv ssl pynacl

build: venv

venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install cryptography
	$(PIP) install pynacl
	$(PIP) install -r requirements.txt || true


ssl:
	$(PYTHON) ssl/stockholmssl.py $(ARGS)
ssl_rev:
	$(PYTHON) ssl/stockholmssl.py -r

pynacl:
	$(PYTHON) pynacl/stockholmpynacl.py $(ARGS)
pynacl_rev:
	$(PYTHON) pynacl/stockholmpynacl.py -r

help:
	$(PYTHON) pynacl/stockholmpynacl.py -help
clean:
	@echo "WARNING: This will delete all encryption keys!";
	@echo "If they are deleted while files are still encrypted, you won't be able to reverse the encryption again."
	@if [ "$(CONFIRM)" = "yes" ]; then \
	    rm -rf sodium.key key.txt iv.txt; \
	    echo "Cleaned!"; \
	else \
	    echo "Add CONFIRM=yes to actually clean (e.g., make clean CONFIRM=yes)"; \
	fi