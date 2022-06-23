"""
For each config, for each sample collection, split and parse the splits
"""
import json
import multiprocessing
import os
import pathlib
import subprocess
import typing

import numpy as np
from more_itertools import divide
from tqdm import tqdm

def main():

    # ------
    # Load configs
    # ------
    with open("parse_configs.json", "r") as f:
        configs = json.load(f)

    # ------
    # Iterate over configs
    # ------
    for config in configs:

        # ------
        # Load current config's variables
        # ------

        # number of ...
        n_processes = int(config["n_processes"])

        # where to load ocr samples
        samples_dir: pathlib.Path = (
            pathlib.Path(config["samples_dir"]).expanduser().resolve()
        )

        # where to save output prse files
        output_dir: pathlib.Path = (
            pathlib.Path(config["output_dir"]).expanduser().resolve()
        )

        # ucto langauge config
        ucto_configurationfile:str = config["ucto_configurationfile"]

        # convert function
        convert = config["convert"]

        # ------
        # ignore if samples_dir doesn't exist or output_dir exists (already ran)
        # ------
        if output_dir.exists():

            print(f"{str(output_dir)} exists ... skipping")
            continue

        elif not samples_dir.exists():

            print(f"{str(samples_dir)} does not exist ... skipping")
            continue

        else:

            # ------
            # create output_dir
            # ------
            output_dir.mkdir(parents=True)

            # ------
            # split the samples wrt., the current config
            # ------

            # list of paths to samples in samples_dir
            samples_paths: list[str] = [
                str(p) for p in samples_dir.glob("*.json") if p.name != "config.json"
            ]

            # amend the n_processes, such that n_process <= len(samples_paths)
            n_processes = min(n_processes, len(samples_paths))

            # n_processes number chunks
            samples_paths_splits = np.array_split(samples_paths, n_processes)

            # ------
            # each split will be passed to its own process
            # this is done via a temporary config for each channel ...
            # ------

            channels_configs = {}
            for i, split_paths in enumerate(samples_paths_splits):

                channels_configs[i] = {
                    "samples_paths": list(split_paths),
                    "output_dir": str(output_dir),
                    "ucto_configurationfile": ucto_configurationfile,
                    "convert":convert
                }

            with open("channels_configs.json", "w") as f:
                json.dump(channels_configs, f, indent=4)

            # ------
            # get an iterable of commands for parallelisation
            # ------

            # i.e., python3 parse_channel.py $(temporary config item number)
            commands = [
                f"python3 parse_channel.py {i}"
                for i, _ in enumerate(samples_paths_splits)
            ]

            # ------
            # run commands in parallel
            # ------
            pool = multiprocessing.Pool(n_processes)
            pool.map(run_command, commands)

            # ------
            # delete the temporary channels_configs.json
            # ------
            pathlib.Path("channels_configs.json").unlink()


def run_command(command):
    """run command and wait for completion before returning"""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
    except:
        pass


if __name__ == "__main__":
    main()
