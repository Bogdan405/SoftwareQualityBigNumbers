import inspect

UNITTEST_IGNORE_METHODS = ["__call__", "__eq__", "__hash__", "__init__", "__repr__", "__str__", "_addExpectedFailure",
                           "_addSkip", "_addUnexpectedSuccess", "_baseAssertEqual", "_callCleanup", "_callSetUp",
                           "_callTearDown", "_callTestMethod", "_deprecate", "_feedErrorsToResult", "_formatMessage",
                           "_getAssertEqualityFunc", "_truncateMessage", "addCleanup", "addTypeEqualityFunc",
                           "assertAlmostEqual", "assertAlmostEquals", "assertCountEqual", "assertDictContainsSubset",
                           "assertDictEqual", "assertEqual", "assertEquals", "assertFalse", "assertGreater",
                           "assertGreaterEqual", "assertIn", "assertIs", "assertIsInstance", "assertIsNone",
                           "assertIsNot", "assertIsNotNone", "assertLess", "assertLessEqual", "assertListEqual",
                           "assertLogs", "assertMultiLineEqual", "assertNoLogs", "assertNotAlmostEqual",
                           "assertNotAlmostEquals", "assertNotEqual", "assertNotEquals", "assertNotIn",
                           "assertNotIsInstance", "assertNotRegex", "assertNotRegexpMatches", "assertRaises",
                           "assertRaisesRegex", "assertRaisesRegexp", "assertRegex", "assertRegexpMatches",
                           "assertSequenceEqual", "assertSetEqual", "assertTrue", "assertTupleEqual", "assertWarns",
                           "assertWarnsRegex", "assert_", "countTestCases", "debug", "defaultTestResult", "doCleanups",
                           "fail", "failIf", "failIfAlmostEqual", "failIfEqual", "failUnless", "failUnlessAlmostEqual",
                           "failUnlessEqual", "failUnlessRaises", "id", "run", "setUp", "shortDescription", "skipTest",
                           "subTest", "tearDown"]


def get_local_suite(specific_class):
    return [specific_class(x[0]) for x in
            inspect.getmembers(specific_class, predicate=inspect.isfunction)
            if x[0] not in UNITTEST_IGNORE_METHODS]


def get_test_suite(test_cases):
    module_suite = []
    for case in test_cases:
        module_suite.extend(get_local_suite(case))
    return module_suite
