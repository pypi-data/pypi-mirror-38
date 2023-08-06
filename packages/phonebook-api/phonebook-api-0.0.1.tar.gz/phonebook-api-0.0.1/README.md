# Messente Phonebook API

PhonebookApi - Python client for Messente Phonebook API

## Requirements

Python 2.7 and 3.4+

## Installation & Usage
### pip install

The latest released version is available via PyPI

```sh
pip install phonebook-api
```

For the latest (unreleased) version you may want to install from Github

```sh
git+https://github.com/messente/messente-phonebook-python.git
```

Then import the package:

```python
import phonebook_api
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import phonebook_api
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from phonebook_api import (
    BlacklistApi,
    ApiClient,
    Configuration
)
from phonebook_api.rest import ApiException

# Configure HTTP basic authorization: basicAuth
configuration = Configuration()
configuration.username = 'YOUR_MESSENTE_API_USERNAME'
configuration.password = 'YOUR_MESSENTE_API_PASSWORD'

# create an instance of the API class
api_instance = BlacklistApi(ApiClient(configuration))

try:
    response = api_instance.fetch_blacklist()
    print(response)
except ApiException as e:
    print("Exception when calling fetch_blacklist: %s\n" % e)

# try:
#     api_instance.add_to_blacklist({'phoneNumber': '+37255555555'})
# except ApiException as e:
#     print("Exception when calling add_to_blacklist: %s\n" % e)

# try:
#     api_instance.remove_from_blacklist('+37255555555')
# except ApiException as e:
#     print("Exception when calling remove_from_blacklist: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://api.messente.com/v1*

Class | Method | HTTP request |
------------ | ------------- | ------------- |
*BlacklistApi* | [**add_to_blacklist**](docs/BlacklistApi.md#add_to_blacklist) | **POST** /phonebook/blacklist |
*BlacklistApi* | [**fetch_blacklist**](docs/BlacklistApi.md#fetch_blacklist) | **GET** /phonebook/blacklist |
*BlacklistApi* | [**remove_from_blacklist**](docs/BlacklistApi.md#remove_from_blacklist) | **DELETE** /phonebook/blacklist/{phone_number} |


## Documentation For Models

 - [ErrorItem](docs/ErrorItem.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [FetchBlacklistSuccess](docs/FetchBlacklistSuccess.md)
 - [NumberToBlacklist](docs/NumberToBlacklist.md)
 - [ResponseErrorCode](docs/ResponseErrorCode.md)
 - [ResponseErrorTitle](docs/ResponseErrorTitle.md)


## Documentation For Authorization


## basicAuth

- **Type**: HTTP basic authentication


## Author

messente@messente.com


