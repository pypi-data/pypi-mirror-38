# The Boring XNAT Library (BXL)

[![PyPI version](https://badge.fury.io/py/bxl.svg)](https://badge.fury.io/py/bxl)
[![pipeline status](https://gitlab.com/bbrc/xnat/bxl/badges/master/pipeline.svg)](https://gitlab.com/bbrc/xnat/bxl/commits/master)
[![coverage report](https://gitlab.com/bbrc/xnat/bxl/badges/master/coverage.svg)](https://gitlab.com/bbrc/xnat/bxl/commits/master)


BXL is a library for interacting with the REST interface of XNAT ([Extensible Neuroimaging Archive Toolkit](https://www.xnat.org/)),
an open-source imaging informatics software platform.

## Usage

### Installation

BXL is available at [PyPI](https://pypi.org/project/bxl/), the Python Package Index.

With [pip](https://pypi.org/project/pip/) package management system:
```commandline
 pip install bxl
```

Without pip:
```commandline
 git clone https://gitlab.com/bbrc/xnat/bxl.git .
 cd ./bxl
 python setup.py install

```

### Credentials handling

The `xnat.Connection()` class constructor expects a `credentials` argument to be passed when instantiated,
* If is a `tuple`, it will proceed to a basic authentication procedure against the `host` XNAT instance.
* If is a `basestring`, it will reuse it as a cookie for authentication against the `host` XNAT instance.   
* Otherwise (or if authentication procedure failed in the aforementioned cases), it will remain offline.

### Examples

Connect to XNAT instance using an existing JSESSIONID token and get a list of user-visible XNAT projects
```python
 import bxl.xnat as xlib

 c = xlib.Connection(hostname='http://myxnat.org',credentials='1A12346385E876546C99B4179E20986A')
 data = c.get_projects()
 
 projects = { item['ID'] : item['URI'] for item in data.values() }
 print projects
 
 c.close_jsession()            

```

Connect via ['with' statement](https://docs.python.org/2.5/whatsnew/pep-343.html) to create a new Female subject 'dummy' in the 'test' project
```python
 from bxl import xnat

 with xnat.Connection(hostname='http://myxnat.org',credentials=(usr,pwd)) as c :
     response = c._put_resource(URI = c.host + '/data/projects/test/subjects/dummy',
                                options = {'gender' : 'female'} )
     subject_uid = response.content
     print 'New subject %s created!' %subject_uid

```
