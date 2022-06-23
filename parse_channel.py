""" 
This script is called by parse.py to perform perform dependency parsing  on a
selection of ocr samples.

'parse.py' creates multiple processes and a file channels_config.json.
Each process calls this script, passing a channel number as an arg.
The paths of ocr sample collection files to be parse by the specific channel
are given by channels_config[channel number].

Run (by parse.py):
    # python3 parse_channel.py channel_number ...
"""

from __future__ import annotations

import re
import json
import pathlib
import subprocess
import sys
import typing

import frog
import ucto
from tqdm import tqdm

# parse_channel.py assumes that each sample is a list of (ocr_name::str,
# list_of_strings::str) tuple. Import the converters to convert from source to
# required format.
for p in pathlib.Path("converters").glob("*.py"):
    exec(f"import converters.{p.stem}")


def main(args):

    # get the channel number from input arg
    channel_number: str = args[0]

    # ------
    # load the relevant config
    # ------
    with open("channels_configs.json", "r") as f:
        configs = json.load(f)

    # config containing samples paths to be parsed by this channel
    config: dict = configs[channel_number]

    # ------
    # load config variables
    # ------
    output_dir: pathlib.Path = pathlib.Path(config["output_dir"])

    samples_paths: list[pathlib.Path] = [
        pathlib.Path(p) for p in config["samples_paths"]
    ]

    # ucto language configuration
    ucto_configurationfile = config["ucto_configurationfile"]


    # sample converter function
    convert:typing.Callable = eval(config["convert"])

    # ------
    # ready frog instance for the current process
    # ------
    frog_instance = frog.Frog(frog.FrogOptions(parse=True))

    # ------
    # setup ucto
    # ------
    tokenizer = ucto.Tokenizer(ucto_configurationfile)

    # ------
    # iterate over samples, parse and save to output_dir
    # ------
    for sample_path in tqdm(samples_paths, desc=f"process: {channel_number}"):

        # get sample file name (w/o extension), i.e., the jsru query that generated its content
        sample_name:str = re.match(".*/(.*).json", str(sample_path)).groups()[0]

        # load the sample json
        with open(sample_path, "r") as f:
            sample = json.load(f)

        # convert the sample to the format assumed by this script
        converted_sample = [convert(t) for t in sample]

        # get a list of (ocr_name:str, parsed sentences:list)
        parsed_sample = [
            (
                label,
                get_parse(list_of_strings, frog_instance=frog_instance, tokenizer=tokenizer),
            )
            for label, list_of_strings in converted_sample
        ]

        # save to output_dir
        with open(output_dir / f"{sample_name}.json", "w") as f:
            json.dump(parsed_sample, f, indent=4, ensure_ascii=False)


def get_parse(list_of_strings: list[str], *, frog_instance, tokenizer) -> list:
    """Return a list of (ocr_name, list of frog(sentence)) tuples for each sentences in ocr."""

    # list of sentences via ucto segmenter
    sentences = []
    for s in list_of_strings:

        try:

            # tokenize with ucto
            tokenizer.process(s)

            # get sentences
            sentences += list(tokenizer.sentences())

        except:
            pass

    # iterable of frog output for each sentence
    parsed_sentences = []
    for s in sentences:
        parse = frog_instance.process(s)
        parsed_sentences.append((s, parse))

    return parsed_sentences


if __name__ == "__main__":
    main(sys.argv[1:])
