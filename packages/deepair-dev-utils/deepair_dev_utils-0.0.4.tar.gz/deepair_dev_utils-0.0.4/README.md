## Deep Developer Utilities

This package consists of developer utilities specifically used for data operations and handeling within deep air environment.

## Package structure

`deepair_dev_utils`
.
├── general
│   ├── __init__.py
│   └── tools.py
├── __init__.py
└── loader
    ├── __init__.py
    └── tools.py

2 directories, 5 files

## Dependencies

**Note**: The following python3 packages are necessary for this package to run:

* numpy
* scipy
* pandas
* sklearn
* tqdm

## Function Declarations

Here are the signatures for the functions in the package that can be used for deepair-dev.

### general.py

Below are the functions that can be accessed by importing this module as `from deepair_dev_utils.general.tools import <function_name>`.

`log`:
```
def log(message):
    '''
        prints message on console
        input :
            message     : msg to print (string)
    '''
```

`get_data`:
```
def get_data(path):
    '''
        Single file loader function
        input :
            path     : abs path to load from (string)
    '''
```

`daterange`:
```
def daterange(s_date, e_date):
    '''
        To return a list of all the dates from
        start date to end date (excluding end date)
        input :
            s_date     : start date (datetime)
            e_date     : end date (datetime)
        returns :
            list of dates
    '''
```

`jsonReader`:
```
def jsonReader(path):
    '''
        JSON File Reader (from absolute path).
        Args:
            path   : absolute path of json file (string)
        Return:
            data   : loaded JSON
    '''
```

`jsonWriter`:
```
def jsonWriter(data, path):
    '''
        JSON File Writer (to absolute path).
        Args:
            data   : data to write (JSON/DICT/STRING)
            path   : absolute path of json file (string)
    '''
```

`ddmmyyyy2datetime`:
```
def ddmmyyyy2datetime(start_date):
    '''
        Convert dd-mm-yyyy to std data time format.
        Args:
            start_date   : date with dd-mm-yyyy (string)
        Return:
            date   : converted format
    '''
```

### Loader

This subpackage contains tools for loading data as `Handler`.

#### Handler

Below are the functions that can be accessed by importing this module as `from deepair_dev_utils.loader.tools import Handler`.

Then create an object to access the fuctions. example `obj = Handler()` and then `obj.<function_name>`

`__init__`:
```
def __init__(self, verbose=True):
    '''
        Handlder (class) constructor.
        inputs:
            verbose: Indicator for log and progress bar (bool)
    '''
```

`loader`:
```
def loader(self, dir_path, start_date, end_date,
           prefix='', postfix='', ext='.csv'):
    '''
        Primary loader function to load the data from start date to
        end date in concatinated (single dataframe) format.
        inputs:
            dir_path    : absolute path to the directory path (series)
            start_date  : load start date in dd-mm-yyyy format (string)
            end_date    : load end date in dd-mm-yyyy format (string)
            prefix      : file prefix [if necessary] (string)
            postfix     : file postfix [if necessary] (string)
            ext         : file extension [default is .csv] (string)
        return:
            df:  loaded concatenated dataframe (pandas df)
    '''
```

`single_loader`:
```
def single_loader(self, dir_path, start_date, end_date,
                  prefix='', postfix='', ext='.csv'):
    '''
        Single loader function to load the data from start date to
        end date in individual datewise (each dataframe is of one date)
        format.
        inputs:
            dir_path    : absolute path to the directory path (series)
            start_date  : load start date in dd-mm-yyyy format (string)
            end_date    : load end date in dd-mm-yyyy format (string)
            prefix      : file prefix [if necessary] (string)
            postfix     : file postfix [if necessary] (string)
            ext         : file extension [default is .csv] (string)
        return:
            data:  list of data frames datewise (list)
    '''
```

`batch_loader`:
```
def batch_loader(self, dir_path, start_date, end_date,
                 batch_size=1, prefix='', postfix='', ext='.csv'):
    '''
        Batch loader function to load the data from start date to
        end date in batches (each dataframe is in the form of batch datewise)
        format.
        inputs:
            dir_path    : absolute path to the directory path (series)
            start_date  : load start date in dd-mm-yyyy format (string)
            end_date    : load end date in dd-mm-yyyy format (string)
            batch_size  : batch size (int)
            prefix      : file prefix [if necessary] (string)
            postfix     : file postfix [if necessary] (string)
            ext         : file extension [default is .csv] (string)
        return:
            data:  list of data frames datewise (list)
    '''
```

`_load_action`:
```
def _load_action(self, df):
    '''
        @abstractmethod
        User defined Bottle neck pipeline within load.
        NOTE -> Default job of this function is pass i.e. do nothing
        inputs:
            df:  Dataframe to apply this method on (pandas df)
        return:
            df:  Modified dataframe (pandas df)
    '''
```
