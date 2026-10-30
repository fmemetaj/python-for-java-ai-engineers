# 0.2 Notebooks (Jupyter)   [NEW — no Java equivalent] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_02/tests/test_skip.py` passes. **Still recommended:** kernel state is the #1 setup surprise for Java developers (F2).

Related explainer: [notebook 00](../../notebooks/00_getting_started.ipynb) and the lab notebook in this folder.

## 1. Concept

A Jupyter notebook is a file of **cells** (markdown or code) executed by a long-lived **kernel** process. The kernel keeps every name you have bound until you restart it. Execution order is whatever you choose, not top-to-bottom of the file.

## 2. Intuition

Think of the kernel as a single JVM that you never shut down between clicks. Each cell is a snippet you send to that JVM. If you run cell 3 before cell 1, cell 3 sees whatever is already in memory — or a `NameError` if nothing is. The `.ipynb` file stores source (and sometimes old outputs); it is not a script with a guaranteed order.

```
cell 1  →  kernel namespace  {x: 1}
cell 3  →  kernel namespace  {x: 1, y: x+1}
restart →  kernel namespace  {}
```

## 3. Why it exists

Java has no standard "document of runnable snippets with hidden state." You have a class, a `main`, JUnit methods, or JShell. Notebooks exist so you can interleave explanation, a tiny experiment, and a plot without packaging a project. AI work uses them for exploration. Production code still belongs in `.py` modules — this course grades exercises as `.py` + pytest for that reason.

What you'd do in Java instead: a scratch `main`, JShell, or a test method. Those restart cleanly. Notebooks do not, unless you restart the kernel.

## 4. Step-by-step examples

**Example 1 — cells share one namespace.** Bind `tickets = []` in one cell, `tickets.append("login")` in the next. The list is the same object.

**Example 2 — later assignment wins.** Run `count = 1`, then `count = 2`. Any later cell sees `2`. Re-run only the first cell and `count` is `1` again — outputs above the cell may now lie.

**Example 3 — out-of-order `NameError`.** A cell that reads `client` fails if you never ran the cell that created it. Restart + **Run All** is the reset button.

**Example 4 — kernel ≠ editor Python.** The notebook kernel must be this repo's `.venv`. A system kernel will raise `ModuleNotFoundError: pydantic` even after `uv sync`.

**Example 5 — saved outputs are history, not proof.** An open notebook can show a number from yesterday's run. Re-run the cell.

Runnable simulation (same ideas, no Jupyter required):

```bash
uv run python concepts/0_02/examples.py
```

Lab notebook (optional explainer): [hidden_state.ipynb](hidden_state.ipynb).

## 5. Common pitfalls

- Running cells out of order, then "fixing" the wrong cell.
- Leaving a kernel running overnight; variables refer to old objects.
- Selecting a global Python instead of `.venv` (Windows: `.venv\Scripts\python.exe`; macOS/Linux: `.venv/bin/python`).
- Opening `.ipynb` as JSON. Use **Open With → Jupyter Notebook**.
- Mixing WSL paths with a Windows kernel, or the reverse.

## 6. Exercises

Two exercises, both graded by pytest (no notebook kernel required):

1. **Guided:** simulate kernel assignments (`exercises/kernel.py` → `last_value`).
2. **Open:** decide whether a name is missing after a partial run (`missing_after_partial_run`).

```bash
uv run pytest concepts/0_02
```

- Hint 1: walk assignments in order; the last write to a name wins.
- Hint 2: a name is missing when it never appears on the left-hand side of the executed cells.
- Solution: `solutions/kernel.py`.

## 7. Check

1. You run cells 1, 2, 4, then edit cell 1 and do not re-run it. Which version of the variable does cell 4 see?
2. You restart the kernel and run only the last cell. What exception is likely?
3. Why does `uv sync` not fix `ModuleNotFoundError` in a notebook that uses a different kernel?
4. Is a green check on an old cell output evidence that the current source still works?

## Setup / troubleshooting

1. Open the **repository folder**, not a single notebook.
2. Command Palette → **Python: Select Interpreter** → `.venv`.
3. In the notebook kernel picker, choose that same interpreter.
4. If the kernel is missing:

```bash
uv run python -m ipykernel install --user --name java-ai-python --display-name "Python (java-ai-python)"
```

Cursor is optional. `uv run jupyter lab` works in a browser. Full notes: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** a teammate "proves" a RAG cell works by scrolling to an old output. Restart, Run All, then trust it.

**What you learned:** notebooks are a kernel plus an unordered log of cells, not a Java class with a single `main`.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
