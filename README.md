# Python ELASTICDUMP
A Python implementation of elasticdump. 

## Requirements
- Python 3.6+
- Requests
- Fire
- TQDM

## Setup
1. Install Python dependencies using `requirements.txt`
2. Run `python setup.py develop`.

## Usage
1. Create a dump
```
elasticdump dump --input=<url-with-index> --output=<output-file> --size=<size>
```
2. Restore a dump
elasticdump restore --output=<url-with-index> --input=<output-file> --size=<size>