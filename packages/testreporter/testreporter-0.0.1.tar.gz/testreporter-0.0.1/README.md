# dj-testreporter

A think wrapper around the default Django `DiscoverRunner` which can generate pretty reports from your tests

## Usage

**Once off**

```
python manage.py test --testrunner=dj_testreporter.runners.BDDTestRunner
```

**Always use it**

`settings.py`
```
TEST_RUNNER='dj_testreporter.runners.BDDTestRunner'
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