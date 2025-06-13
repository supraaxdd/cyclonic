<div align="center">
    <img width="250" height="250" src="./assets/Cyclonic_Logo.png">
</div>

# Cyclonic
This project is a continuation of my final year project for college.
To get started, please look at the [Installation](##Installation) section of this README. 

## Installation

### Prerequisites
Ensure that you have Anaconda installed.
Ensure that you have a machine with a DEDICATED GPU or else you will not be able to run this project.

### Installation Steps
Clone the master branch of this repository and go into the directory:

```bash
git clone https://github.com/supraaxdd/cyclonic.git
cd cyclonic
```

To run this project effectively, you should create an anaconda environment using the provided environment.yml file

```bash
conda env create --name cyclonic-env --file=environment.yml
```

and then activate the environment using:

```bash
conda activate cyclonic-env
```

## Using project modules together

### Data Module
This module is responsible for fetching and formatting the data for the AI model to use during training and predicting. 

Follow the steps on the README provided in the [data](https://github.com/supraaxdd/cyclonic/tree/master/data) module for more information on how to fetch data.

### AI Module
This module holds the source code behind the AI model. Here is where you train and use the model. Go to the README in the [ai](https://github.com/supraaxdd/cyclonic/tree/master/ai) folder for more information on how to train and use the model.