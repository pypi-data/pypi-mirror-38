# VariantGrid API

Command line tool and Python library to connect to the [Shariant](https://shariant.org.au) variant database.

### Installing

Install the [Pip Package](https://pypi.python.org/pypi/variantgrid_api). On Linux this is via:

```
sudo pip install variantgrid_api
```

or if you have downloaded the source code and wish to install from the local copy, run from this directory
```
sudo pip install -e .
```

### Command line Example

Retrieve a list of classified variants
```
vg_api classifications --user XXX --password YYYY --all
```

### Configuration Files

Create ~/.vg_api to store command line parameters so you don't have to pass them each time, eg:

```
user = XXX
password = YYY
```
### Classifications (reading)

Retrieve the complete set of keys that can be used in variant evidence
```
vg_api classifications --keys
```

Retrieve a list of classified variants
```
vg_api classifications --all
```

Retrieve a specific classified variant
```
vg_api classifications --id 5
```
Retrieve a specific version
```
vg_api classifications --id 5 --version 1
```
Retrieve using a lab id, where the lab id is B5886D3C-3E86-4F56-A550-1417D8AB1563
```
vg_api classifications --id L_B5886D3C-3E86-4F56-A550-1417D8AB1563
```

### Classifications (uploading)

Inserting or replacing a record with a lab id of B5886D3C-3E86-4F56-A550-1417D8AB1563
```
vg_api classification_upload --id L_B5886D3C-3E86-4F56-A550-1417D8AB1563 < record_data.json
```

where the contents of record_data would look like
```
{
    "condition": "OMIM:3242",
    "BA1": "NM",
    "age": 7,
    etc
}

```

Updating a few fields
```
vg_api classification_upload --method PATCH --id L_B5886D3C-3E86-4F56-A550-1417D8AB1563 < delta.json
```

### Python

You can make your own API calls via Python: 


```
from variantgrid_api import VariantGridAPI

In [1]: api = VariantGridAPI(login, password)

In [2]: api.shariant_classification('4')
Out[2]: 
{
    "id": 3,
    "data": {
        "x": {
            "value": "y"
        }
    },
    "versions": 1,
    "version": "latest",
    ....
}
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
