"""
web python manage.py test --testrunner=testreporter.runners.BDDTestRunner
"""
from django.test.runner import DiscoverRunner
from unittest import TextTestRunner
import copy

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def p(msg, msg_list, is_error=False):
    if not is_error:
        print ("{0}{1}{2}" . format (bcolors.OKBLUE, msg, bcolors.ENDC))
    else:
        print ("{0}{1}{2}" . format (bcolors.FAIL, msg, bcolors.ENDC))
    msg_list.append(msg)

class BDDTestRunner(DiscoverRunner):

    def __init__(self, pattern=None, top_level=None, verbosity=1,
                 interactive=True, failfast=False, keepdb=False,
                 reverse=False, debug_mode=False, debug_sql=False, parallel=0,
                 tags=None, exclude_tags=None, **kwargs):

        super().__init__(pattern=pattern, top_level=top_level, verbosity=verbosity,
                 interactive=interactive, failfast=failfast, keepdb=keepdb,
                 reverse=reverse, debug_mode=debug_mode, debug_sql=debug_sql, parallel=parallel,
                 tags=tags, exclude_tags=exclude_tags, **kwargs)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        This is lifted straight from: https://github.com/django/django/blob/master/django/test/runner.py
        """
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        old_config = self.setup_databases()
        run_failed = False
        report = []
        try:
            self.run_checks()
            all_tests = [test for test in suite._tests]
            result = self.run_suite(suite)
            self.report_results(result, all_tests)
        except Exception:
            run_failed = True
            raise
        finally:
            try:
                self.teardown_databases(old_config)
                self.teardown_test_environment()
            except Exception:
                # Silence teardown exceptions if an exception was raised during
                # runs to avoid shadowing it.
                if not run_failed:
                    raise
        return self.suite_result(suite, result)


    def report_results(self, result, all_tests):

        report = []

        p("************", report)
        p("TEST SUMMARY", report)
        p("************", report)

        # all_tests = [test for test in  dir(testcase) if test.startswith('test_')]

        failures = [method._testMethodName for method, err in result.failures]
        errors = [method._testMethodName for method, err in result.errors]

        # successfull_tests = set(all_tests).difference(failures).difference(errors)
        last_testcase = None
        last_testmodule = None

        for test in all_tests:
            testmodule_name = test.__module__
            testcase_name = test.__class__.__name__
            testcase_docstring = test.__class__.__doc__
            if testcase_docstring is not None: testcase_docstring.strip()

            test_name = test._testMethodName
            pretty_test_name = test_name[5:].replace('_', ' ')

            if testmodule_name != last_testmodule:
                p("-", report)
                p("---------------------", report)
                p(testmodule_name.upper(), report)
                p("---------------------", report)

            if testcase_name != last_testcase:
                p(" ", report)
                p(" {}: {}".format(testcase_name, testcase_docstring or ''), report)
                p(" ---------------------", report)

            if test_name in failures:
                p("  ✗ {}".format(pretty_test_name), report, is_error=True)
            elif test_name in errors:
                p("  ✗ {}".format(pretty_test_name), report, is_error=True)
            else:
                p("  ✓ {}".format(pretty_test_name), report)

            last_testcase = testcase_name
            last_testmodule = testmodule_name

        f = open('spec.txt', 'w')
        for line in report:
            f.write(line + '\n')
        f.close()

