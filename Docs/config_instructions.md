# configuration instructions for parse_configs.json

Each config::dict in parse_configs.json is run separately by parse.py

## Example parse_configs.json

```
{
    "name": "example",
    "samples_dir": "/data/project_WIP/KB_sampling/example",
    "output_dir": "/data/project_WIP/frog_dep_parse/example",
    "n_processes": 1,
    "convert": "converters.KB_sampling.convert",
    "ucto_configurationfile": "tokconfig-nld"
}
```

## Those keys used by parse.py and/or parse_channel.py

* "convert" (str): the conversion function to be used to convert the information format of the jsons in "samples_dir" to the format assumed by the scripts. Write new conversion functions as required

* "samples_dir" (str): the path to the folder containing json text collections to be parsed. 

* "output_dir" (str): the path to the folder to put the parsed collections from samples_dir. The output files are named the same as the input files.

* "n_processes" (int): the number of parallel processes to run (instances of frog), splitting the file in "samples_dir" into "n_processes" sets.

* "ucto_configurationfile": the tokenisation settings to by used by ucto, in performing sentence segmentation on strings.
