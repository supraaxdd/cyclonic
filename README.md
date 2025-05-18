<div align="center">
    <img width="250" height="250" src="./assets/Cyclonic_Logo.png">
</div>

# Cyclonic Data Module
This module is part of the Cyclonic Project for my MTU Final Year Project.

This module is responsible for making data requests to the relevant APIs, to then be used in a machine learning model to predict possible wind speeds and directions for a specific area.


## Installation

### Prerequisites
Ensure that you have Anaconda installed

### Installation Steps
Clone the master branch of this repository and go into the directory:

```bash
git clone https://github.com/supraaxdd/cyclonic-data.git
cd cyclonic-data
```

To use this project effectively with the Cyclonic AI module, you should create an anaconda environment using the provided environment.yml file

```bash
conda env create --name cyclonic-env --file=environment.yml
```

Now you can run main.py

```bash
python main.py
```

If you would like to include debug information from the logger, create a `.env` file in the project directory with the following content:
```env
LOG_LEVEL=DEBUG
```

## Getting past of future data
The main script provides options which control how you would like to fetch the data.

If you would like to get past data, you need to use the `-p` or `--previous` argument like so:

```bash
python .\main.py -p
```

If you would like to get future data, omit the `-p` argument.


By default, it will fetch the past or future 14 days. If you would like to fetch data beyond 14 days, you may do so by using the `-d [NUMBER_OF_DAYS]` or `--days [NUMBER_OF_DAYS]` argument:

```bash
python .\main.py -p -d 30
```

*NOTE: YOU MAY ONLY FETCH UP TO 15 DAYS WORTH OF DATA INTO THE FUTURE*

When the command is ran, the module calls on the OpenMeteo API to fetch the data and outputs the formatted JSON result into the `output` folder.

## Running Unit Tests

To run unit tests, you need to execute the following command from the [tests/](./tests/) directory:

```bash
python -m unittest discover -v
```


## Authors

- [@supraaxdd](https://www.github.com/supraaxdd)

