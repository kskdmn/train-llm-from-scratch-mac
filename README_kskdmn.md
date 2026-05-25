# kskdmn Notes

## Installing the notebook output stripper

Run this command once after cloning the repository:

```bash
uv run nbstripout --install
```

This uses `uv run` to execute the `nbstripout` package from the project environment defined by `pyproject.toml` and `uv.lock`. If the environment is not ready yet, `uv` can create or update it before running the command.

`nbstripout --install` configures the current Git repository to clean Jupyter notebooks before they are committed. After it is installed, Git strips notebook cell outputs and execution counts from `.ipynb` files during commit, while keeping the actual notebook source cells intact.

This is useful for this repository because notebook outputs can be large, noisy, and machine-specific. Stripping them keeps diffs focused on code and markdown changes, makes reviews easier, and avoids committing generated output by accident.

The install is local to your clone because it writes Git filter settings under `.git/config`. Run it again when you clone the repository somewhere else.

Useful related commands:

```bash
uv run nbstripout --status
uv run nbstripout --uninstall
```

Use `--status` to check whether the filter is installed, and `--uninstall` if you need to remove the Git filter from the current clone.
