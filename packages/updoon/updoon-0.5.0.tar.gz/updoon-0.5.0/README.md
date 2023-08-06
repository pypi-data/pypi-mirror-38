# updoon

The `updoon` package is a collection of python function 
and classes to download or synchronize datasets.

(I just dump all my **data engineering** snippets.)

### Installation

Check the source code at https://github.com/ulf1/updoon

```sh
pip install updoon
```

### Load the package

I am going to use the ud shortcut

```python
import updoon as ud
```

### Versioning
- X: Major changes for the package
- Y: New function, class, module was added
- Z: Bugfixes, minor changes

This package will be `0.X.Y` for an unseen future. 

An version `1.X.Y` might involve heavy refactoring, using base classes, etc. I personally have no interest in doing library architecture. Thus, I will not be the driving force for any `X>0` version.


### Notes to myself

1. Update setup.py (version, requirements)
2. Update CHANGES.txt (what's added, changed, removed?)
3. Run:  `python setup.py sdist upload -r pypi`


### Function and Classes

Quandl

* `quandl_apikey_set` -- Store Quandl API Key locally
* `quandl_apikey` -- Read locally stored Quandl API Key.

FRED2

* `fred_apikey_set` -- Store FRED API Key locally
* `fred_apikey` -- Read locally stored FRED API Key.





