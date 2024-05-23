# Paho MQTT Python Client Implementation Example

* [Github Repo](https://github.com/eclipse/paho.mqtt.python)
* [Full Documentation](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)

## [Step 1. Get `creds.json`](https://github.com/LinkLabs/mqtt-client-examples/blob/main/README.md#getting-mqtt-credentials)

## Step 2. Ensure Python Enviornment

Requirements:

* [Python + Pip](https://www.python.org/downloads/)
* Optional: [Poetry Package Manager](https://python-poetry.org/docs/)

## Step 3.a Prepare Python Virtual Enviornment (with Poetry)

```
poetry install
```

## Step 4.a Run Demo Applicaiton (with Poetry)

```
poetry run python main.py
```

## Step 3.b Prepare Python Virtual Enviornment (Manually)

### Create a virutal enviornment:

```
python -m venv /path/to/new/virtual/environment
```

### Activate virtual enviornment:

| Platform | Shell | Command to activate virtual environment |
| -------- | ----- | --------------------------------------- |
| POSIX    | bash/zsh | `$ source <venv>/bin/activate` |
| POSIX    | fish | `$ source <venv>/bin/activate.fish` |
| POSIX    | csh/tcsh | `$ source <venv>/bin/activate.csh` |
| POSIX    | PowerShell | `$ <venv>/bin/Activate.ps1` |
| Windows | cmd.exe | `C:\> <venv>\Scripts\activate.bat` |
| Windows | PowerShell | `PS C:\> <venv>\Scripts\Activate.ps1` |

More information: https://docs.python.org/3/library/venv.html

### Install MQTT Dependency

```
pip install paho-mqtt
```

## Step 4.b Run Demo Application (Manually)

```
python3 main.py
```


