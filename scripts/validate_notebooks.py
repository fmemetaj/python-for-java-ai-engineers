"""Execute all seven notebooks in independent kernels (no manual Jupyter interaction)."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
ROOT = Path(__file__).resolve().parents[1]
paths = sorted((ROOT / "notebooks").glob("*.ipynb"))
assert len(paths) == 7, f"Expected seven notebooks, got {len(paths)}"
for path in paths:
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    NotebookClient(notebook,timeout=90,kernel_name="python3",resources={"metadata":{"path":str(ROOT)}}).execute()
    print("PASS",path.name)
print("All seven notebooks passed")
