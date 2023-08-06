# ElectronBonder
A client library for working with the Project Electron APIs.

## Credits
This code is basically stolen from [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake/).

## Requirements
ElectronBonder has the following requirements.

- Python 3.4 or higher
- ability to install packages via pip ([Pipenv](https://docs.pipenv.org/) is recommended for development)

## Installation
The easiest way to install ElectronBonder is via pip:

      pip3 install ElectronBonder

You'll need an internet connection to fetch ElectronBonder's dependencies.

## Usage
To start, you must create a client with a baseurl:

``` python
from electronbonder.client import ElectronBond

client = ElectronBond(baseurl="http://my.aspace.backend.url.edu:4567")
```


## Configuration

As per the example above, the client object should be configured by passing it arguments during creation.

Allowed configuration values are:

| **Setting** | **Description**                                                               |
|-------------|-------------------------------------------------------------------------------|
| baseurl     | The location (including port if not on port 80) of the application's API root |


## License
ElectronBonder source code is released under an MIT License.
