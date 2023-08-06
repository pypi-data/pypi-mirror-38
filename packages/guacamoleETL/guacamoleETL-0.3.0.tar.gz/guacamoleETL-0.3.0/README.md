# guacamoleETL - Document

An ETL pipeline tool that
* pre-process
  * extracts data from a .txt file ([Challenge_me.txt](Challenge_me.txt))
  * cleans up the data with invalid information
* transforms the data through given specifications into a matrix (list of lists)
* loads the data into a .csv file ([output.csv](output.csv))

## Installation
This tool can be installed with `pip`<br>
Copy-paste and run this command in the terminal
```
pip install guacamoleETL
```

## Usage
This ETL pipeline can be part of predictive model training and feed the data directly to the model
```py
import guacamoleETL

dataFile = 'Challenge_me.txt'

guacamoleETL.load(dataFile)
result = guacamoleETL.transform(dataFile)
predictive_model = model_training(result)
```

## Functions
* __extract_data(txt_file):__
  __Extract data from a .txt file to a temporary .csv file__<br>
  Leading or trailing whitespace are removed during the extraction
* __clean_up():__
  __Clean up the data with invalid information__<br>
  Rows with the placeholder '-' (NA) in any of the specified columns are excluded
* __transform(path):__
  __Transform the data from pre-process through given specifications into a matrix__<br>
  `engine-location` is split into two columns, `engine-location_front` and `engine-location_rear` and one-hot-encoded<br>
  `num-of-cylinders` is transformed from word into integer through a pre-defined dictionary<br>
  `engine-size` is transformed into integer<br>
  `weight` is transformed into integer<br>
  `horsepower` is transformed from German decimal notation string into float number<br>
  `aspiration` is modified as `aspiration_turbo` so that turbo engines are marked as 1<br>
  `price` is converted from minor units to major units<br>
  `make` is not transformed but kept in the dataset
* __load(path):__
  __Load the data from previous transformation into a .csv file__


## Architecture
All the functions are implemented in the [\_\_init\_\_.py](guacamoleETL/__init__.py), this decision is made based on the following reasons:
* After the package is imported, if we want to use the transform and load functions directly as sub-module, the functions must be imported or defined in `__init__.py`.
* Since they are all connected to each other, such as the transform function takes the result from pre-process (extract and clean up) and the load function also takes the result from transform function, it's easier to follow the flow if they are all in the same file.
* This might not be the best architecture implementation, but while starting from small, simplicity is always a good consideration.
