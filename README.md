# KDB Examples
KDB automation testing framework for web (desktop &amp; mobile) and mobile app (android &amp; iOS)


## Clone project from git (https://github.com/Trucnt/kdb-examples.git) to your disk. Ex: D:\kdb-examples

### Creation of virtual environments (https://docs.python.org/3.11/library/venv.html)
```bash
python -m venv "D:\kdb-examples\venv"
```

## Activating a virtual environment on Windows
```bash
D:
cd "D:\kdb-examples"
.\venv\Scripts\activate
where python
```

## Installing packages

### Upgrade pip
```bash
python -m pip install --upgrade pip
```

### behave
```bash
py -m pip install git+https://github.com/behave/behave@v1.2.7.dev5
```

### Installing using requirements files
```bash
py -m pip install -r "D:\kdb-examples\requirements.txt"
```

## Running test: behave -i "<feature_file_name>" -D profile="<profile_name>"
```bash
py -m behave -i "login_failure.feature"

py -m behave -i "rest_api_with_json" -D profile=example_api_dev
```
