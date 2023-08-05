# dj-testreporter

```
pip install testreporter
```

[![PyPI version](https://badge.fury.io/py/testreporter.svg)](https://badge.fury.io/py/testreporter)

A thin wrapper around the default Django `DiscoverRunner` which can generate pretty reports from your tests

## Usage

**Once off**

```
python manage.py test --testrunner=testreporter.runners.BDDTestRunner
```

**Always use it**

`settings.py`
```
TEST_RUNNER='testreporter.runners.BDDTestRunner'
```

Example output:

```
* ************
* TEST SUMMARY
* ************
* -
* ---------------------
* MYPROJECT.TESTS.TEST_MODELS
* ---------------------
*
*  SomeModelTestCase:
*  ---------------------
*   ✓ a test that passes
*   ✗ a test that fails
```

It will also create a file `spec.txt`. You can commit that to version control and then you have automatic release notes in the diff for your pull request.