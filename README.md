# README

Convert a collection of texts to a collection of frog-parses of the sentences contained within the texts.

Refer to [parse_configs.json](parse_configs.json) and [config_instructions.md](Docs/config_instructions.md).

It is necessary to define a conversion module/function to convert the format of the input texts to the format assumed by "parse.py". Refer to the example [converters/KB_sampling.py](converters/KB_sampling.py) conversion function. This converts file format of the files found in specified "sample_dir" resulting from "KB_sampling" process, to the format assumed by "parse_channel.py".

## Obtain frog-parses of samples


Note: the script is run within lamachine via docker.

```
docker run -p 8080:80 -it -v "$(pwd)/":/scripts -v "$HOME/Data/":/data proycon/lamachine:latest

python3 parse.py
```

## Obtain frog-parses of samples via the IISG rekenserver

* login to the vpn
* ssh onto the server
```
ssh ryanb@rc01.dev.clariah.nl
```
* screen
```
screen -S parsing
```

* create server side folder necessary
```
mkdir -p Data/pilot2/samples
```

* upload sampled ocr collections (of interest) from Data folder
```
# open (local system) terminal in Data area

scp -r pilot2/samples/publication_date_content__sabio_distribution/ ryanb@rc02.dev.clariah.nl:/home/ryanb/Data/pilot2/samples/
```

* upload parsing pipeline component from Scripts area
```
# open (local system) terminal in pilot2/ code folder

scp -r B_parse_samples/ ryanb@rc02.dev.clariah.nl:/home/ryanb/pilot2/
```

* chmod the Data and pilot2 to enable docker to access (?)
```
# in the rekenserver terminal
cd $HOME
chmod -R 777 Data
chmod -R 777 pilot2
```

* amend the parse\_configs.json files such that e.g., n\_processes = 50

* perform parsing 

```python
# in the rekenserver terminal

cd $HOME/pilot2/B_parse_samples

docker run -p 8080:80 -it -v "$(pwd)/":/scripts -v "$HOME/Data/pilot2":/data proycon/lamachine:latest

cd /scripts

python3 parse.py
```
