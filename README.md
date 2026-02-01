# zxdf
A package manager for AI skills 

## Development

### Setup

We use `uv` as the package and project manager for all the Python packages in this repository. Before contributing, make sure you have `uv` installed (see [installation guide](https://docs.astral.sh/uv/getting-started/installation/)).

1. Clone the GitHub repo and open a terminal at the root of the git repository `zxdf`.
2. At the root of the repo, run the following command to setup the virtual envionrment:
```
uv sync
```
3. Install the library in editable mode to test the actual CLI using the following command:
```bash
   uv pip install -e .
```
Verify the installation:
```bash
   zxdf --help
```