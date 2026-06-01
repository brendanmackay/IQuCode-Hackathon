# Qiskit Hackathon Starter

This folder is set up as a small Python/Qiskit workspace.

## Activate the environment

```bash
source .venv/bin/activate
```

## Install or refresh packages

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name qiskit-hackathon --display-name "Python (Qiskit Hackathon)"
```

## Run the starter circuit

```bash
python src/starter.py
```

## Start notebooks

```bash
jupyter lab
```

For IBM Quantum hardware access, create an IBM Quantum account token and keep it out of git, for example in a local `.env` file.
