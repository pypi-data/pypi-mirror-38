# Django Young America

[Ya - Young America](https://yaengage.com/) API integration for Django applications

#### Installation
```python
pip install django-young-america
```

#### Usage
```python
from youngamerica.models import YaClient
profile = {
    'first_name': 'John',
    'last_name': 'Smith',
    'email': 'john.smith@example.com',
    'zip_code': '12345',
    'date_of_birth': '12/30/1900',
    'tag_info': 'tag',
    'entry_date': '08-26-2018',
    'address': '',
    'city': '',
    'state': '',
}
ya = YaClient()
response = ya.send(profile)
```

#### Configuration
Add these variables to your Django settings
```python
from os import getenv

YA_DATETIME_FORMAT = '%m/%d/%Y %I:%M:%S %p'
YA_TIMEZONE = 'America/Chicago'
YA_CLIENT_ID = getenv('YA_CLIENT_ID', '')
YA_VENDOR_CODE = getenv('YA_VENDOR_CODE', '')
YA_RETURN_ID_FLAG = getenv('YA_RETURN_ID_FLAG', 'Y')
YA_ENTRY_METHOD = getenv('YA_ENTRY_METHOD', '3')

YA_ENDPOINT_URL = getenv('YA_ENDPOINT_URL', 'http://e-webservices.yastaging.com/SubmissionServices.asmx')
YA_SWEEPS_ID = getenv('YA_SWEEPS_ID', '')
YA_SWEEPS_TOKEN = getenv('YA_SWEEPS_TOKEN', '')
YA_DISCOUNT_ID = getenv('YA_DISCOUNT_ID', '')
YA_DISCOUNT_TOKEN = getenv('YA_DISCOUNT_TOKEN', '')
YA_DISCOUNT_ITEM = getenv('YA_DISCOUNT_ITEM', '')

```