# 01 — Pick your editor (Cursor is optional)

An editor is a choice, not a prerequisite. This repository works with **Cursor, VS Code, browser-based JupyterLab, or another IDE**.

## Common setup, independent of editor

From the repository root:

```bash
uv python install 3.12
uv sync --locked --group dev
```

That creates the local environment `.venv` and installs the notebooks' dependencies.

## Cursor

1. Open **File → Open Folder**, and choose this repo's root, not the notebooks folder.
2. Install the recommended **Python**, **Jupyter**, and **Ruff** extensions if prompted (see `.vscode/extensions.json`).
3. Press **Ctrl/Cmd+Shift+P → Python: Select Interpreter**.
4. Select `.venv/Scripts/python.exe` on Windows, or `.venv/bin/python` on macOS/Linux.
5. Open `notebooks/00_getting_started.ipynb`. Choose a notebook **kernel** from the same `.venv`.
6. Run cells one by one. View Markdown by opening notebook or preview mode. If it opens as JSON, choose **Open With → Jupyter Notebook**.
7. Cursor's learning-first rule is committed in `.cursor/rules/learning-first.mdc`. Check **Cursor Settings → Rules** if it does not appear.

**Useful AI prompt:** "I'm a Java developer learning Python. Explain this cell using a Java comparison, then give one hint without solving the exercise."

**Safe learning approach:** use Cursor's read-only **Ask** mode for explanations; switch to **Agent** only when you intend to edit files. Review any generated code and rerun tests.

## VS Code

Install the same Python, Jupyter and Ruff extensions, select your `.venv` interpreter using **Python: Select Interpreter**, then choose the kernel in each notebook. Cursor-specific rules are not needed.

## Pure JupyterLab (no IDE)

```bash
uv run jupyter lab
```

Open notebook 00, use the environment's kernel, and run cells in order.

## Other IDEs

Open the repository root and configure its Python interpreter to the `.venv` created by `uv`. If the IDE has no reliable notebook support, launch JupyterLab from its terminal.

## When the interpreter is missing

From the repo root:

```bash
uv run python -m ipykernel install --user --name java-ai-python --display-name "Python (java-ai-python)"
```

Restart your editor and select the new kernel. **Do not use the global system Python** by accident; it may not have Pydantic installed.

[Return to guide index](README.md)
