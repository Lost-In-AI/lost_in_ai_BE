# -------- Virtual environment --------
# Create a new Python virtual environment venv
# Note: "source venv/bin/activate" here only runs in a subshell, so it does not persist in your shell
venv:
	python3 -m venv venv && source venv/bin/activate

# -------- Dependencies installation --------
# Install all required packages from requirements.txt inside the venv
install:
	source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# -------- Package management --------
# To install a new package inside the venv and update requirements.txt run: make install-pkg pkg=requests
install-pkg:
	venv/bin/pip install $(pkg)
	venv/bin/pip freeze > requirements.txt

# To uninstall a package and update requirements.txt run: make uninstall-pkg pkg=requests
uninstall-pkg:
	venv/bin/pip uninstall -y $(pkg)
	venv/bin/pip freeze > requirements.txt

# -------- Style management --------
# Run flake8 linter on the "app" directory to check code style
style:
	flake8 app
