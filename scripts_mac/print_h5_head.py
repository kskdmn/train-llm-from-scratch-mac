import argparse
import logging
from pathlib import Path
from typing import Optional

import h5py
import numpy as np


logger = logging.getLogger(__name__)


def _format_value(value) -> str:
    if isinstance(value, np.ndarray):
        return np.array2string(value, threshold=20)
    if isinstance(value, np.generic):
        return str(value.item())
    return str(value)


def _print_dataset_preview(path: str, dataset: h5py.Dataset, lines: int) -> None:
    print(f"{path} shape={dataset.shape} dtype={dataset.dtype}")

    if dataset.shape == ():
        print(f"[0] {_format_value(dataset[()])}")
        return

    preview_count = min(lines, dataset.shape[0])
    for index in range(preview_count):
        print(f"[{index}] {_format_value(dataset[index])}")


def _iter_datasets(h5_file: h5py.File) -> list[tuple[str, h5py.Dataset]]:
    datasets = []

    def collect_dataset(name: str, obj) -> None:
        if isinstance(obj, h5py.Dataset):
            datasets.append((f"/{name}", obj))

    h5_file.visititems(collect_dataset)
    return datasets


def print_h5_head(h5_path: str | Path, lines: int = 10, dataset: Optional[str] = None) -> None:
    if lines < 1:
        raise ValueError("--lines must be at least 1")

    with h5py.File(h5_path, "r") as h5_file:
        if dataset is not None:
            dataset_path = dataset if dataset.startswith("/") else f"/{dataset}"
            h5_dataset = h5_file[dataset_path]
            if not isinstance(h5_dataset, h5py.Dataset):
                raise TypeError(f"{dataset_path} is not an HDF5 dataset")
            _print_dataset_preview(dataset_path, h5_dataset, lines)
            return

        datasets = _iter_datasets(h5_file)
        if not datasets:
            raise ValueError(f"No datasets found in {h5_path}")

        for index, (dataset_path, h5_dataset) in enumerate(datasets):
            if index > 0:
                print()
            _print_dataset_preview(dataset_path, h5_dataset, lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Print the first rows or entries of HDF5 datasets.")
    parser.add_argument("h5_file", help="Path to the HDF5 file.")
    parser.add_argument("--lines", type=int, default=10, help="Number of rows or entries to print.")
    parser.add_argument("--dataset", help="Optional dataset path to preview, such as tokens or /tokens.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.ERROR, format="%(levelname)s:%(name)s:%(message)s")

    try:
        print_h5_head(args.h5_file, lines=args.lines, dataset=args.dataset)
    except Exception as error:
        logger.exception("Failed to print HDF5 head: %s", error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
