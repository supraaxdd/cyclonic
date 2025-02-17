<div align="center">
    <img width="250" height="250" src="./assets/Cyclonic_Logo.png">
</div>

# Cyclonic Data Module
This module is part of the Cyclonic Project for my MTU Final Year Project.

This module is responsible for making data requests to the relevant APIs, to then be used in a machine learning model to predict possible wind speeds and directions for a specific area.


## Installation

### Prerequisites
Ensure that you have Python installed

### Installation Steps
Clone the master branch of this repository and go into the directory:

```bash
git clone https://github.com/supraaxdd/cyclonic-data.git
cd cyclonic-data
```

Install all the required pip packages:

```bash
pip install openmeteo_requests requests_cache retry_requests
```

Now you can run main.py

```bash
python main.py
```

## Running Unit Tests

To run unit tests, you need to execute the following command from the [tests/](./tests/) directory:

```bash
python -m unittest discover -v
```


## Authors

- [@supraaxdd](https://www.github.com/supraaxdd)

