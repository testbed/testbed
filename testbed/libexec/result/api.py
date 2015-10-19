"""
Functionality common to more than one command.
"""
import logging
from testbed.libexec import testsuite
from testbed.libexec import product
from testbed.libexec import testplan


# pylint: disable=R0913
# pylint: disable=R0914
def set_result(context, product_name, branch_name, build, testsuite_name,
               test_name, result, keys):
    """ Get or create a testplan in a certain order.

    @param product_name Is the name of the product
    @param order order is the location of the testplan in the list of
                 testplans. The order effects the location the testplan
                 appears on web pages.
    """
    from testdb import models

    logging.info("result for %s %s %s", testsuite_name, test_name, result)
    context = models.Context.objects.get(name=context)
    (product1, _) = product.api.get_or_create(product_name, branch_name)

    testplan_name = product1.key_get("testplan", None)
    if testplan_name is None:
        testplan_name = "default"
        (testplan_key, _) = models.TestKey.get_or_create("testplan",
                                                         testplan_name)
        models.TestProductKeySet.objects.create(testproduct=product1,
                                                testkey=testplan_key)

    order = testplan.api.planorder_get_or_create(
        "testplan.%s" % testplan_name, testsuite_name, keys)

    build_key = models.TestKey.get_or_create("build", build)[0]
    (testsuite1, _) = models.Testsuite.get_or_create(context, testsuite_name,
                                                     order, build_key, [])
    (test, created) = models.Test.get_or_create(testsuite1, test_name, [])

    if result == "pass":
        test.status = 0
    else:
        test.status = 1
        test.save()
    return (test, created)


# pylint: disable=W0622
def list_result(context, testkeys, testsuite_name=None, test_name=None):
    """ Retrieve the list of products based on product and or branch_name. """

    testsuites = testsuite.api.list_testsuite(context, testkeys,
                                              testsuite_name)
    for testsuite_item in testsuites:
        if test_name:
            find = testsuite_item.filter(test__name=test_name)
        else:
            find = testsuite_item.test_set.all()

        for test in find:
            yield (testsuite_item, test)
