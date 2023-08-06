# text-indexer

[![Build Status](https://travis-ci.org/Yoctol/text-indexer.svg?branch=master)](https://travis-ci.org/Yoctol/text-indexer) 
[![PyPI version](https://badge.fury.io/py/text-indexer.svg)](https://badge.fury.io/py/text-indexer)

Indexer transforms list of strings to list of integers according to the string2int mapping function(e.q. a look-up table).

## Getting Started

### Prerequisites

1. Please create a virtual environment with python 3.6
2. Type the following command in terminal: 
```
make install
```

### Running the tests

```
make test
```

## How to completely save and load indexer?

### 1. Save
```python
from text_indexer.io import save_indexer
custom_indexer_instance = XXIndexer()
save_indexer(indexer=custom_indexer_instance, output_dir='directory-to-export-indexer')
```
If output_dir is `/home/user/example/`, you will get a tar file  `/home/user/example-all.tar.gz` after calling 
`save_indexer`.

### 2. Load
```python
from text_indexer.io import load_indexer
your_indexer = load_indexer(path='indexer-tar-filepath')
```
