# coding=utf-8
"""
tests converted from util.VersionStr
"""

from versio.version import Version
from versio.version_scheme import Simple5VersionScheme


# noinspection PyDocstring
class Version5(Version):
    def __init__(self, version_str):
        super(Version5, self).__init__(version_str=version_str, scheme=Simple5VersionScheme)


VersionStr = Version5


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testLessThan():
    assert not VersionStr("3.2.0.20046") < "3.2.0.846"
    assert not VersionStr("3.2.0.200") < "3.2.0.2"
    assert VersionStr("3.6.2.3.1") < "3.6.3.0"
    assert not VersionStr("10.0.0.0") < VersionStr("9.6.0.0")
    assert not (VersionStr("10.0.0.0") < "10.0.0.0")
    assert not ("0.2.10.0.0") < VersionStr("0.0.10.0.0")
    assert ("0.0.1.0.0") < VersionStr("0.0.10.0.0")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testLessEqual():
    assert not VersionStr("3.2.01.00") <= VersionStr("3.2.0.0")
    assert not VersionStr("3.2.0.20046") <= "3.2.0.846"
    assert not VersionStr("3.2.0.200") <= "3.2.0.2"
    assert VersionStr("3.6.2.3.1") <= "3.6.3.0"
    assert not VersionStr("10.0.0.0") <= ("9.6.0.0")
    assert VersionStr("10.0.0.0") <= ("10.0.0.0")
    assert not ("0.2.10.0.0") <= VersionStr("0.0.10.0.0")
    assert ("0.0.1.0.0") <= VersionStr("0.0.10.0.0")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testGreaterThan():
    assert VersionStr("3.2.01.00") > VersionStr("3.2.0.0")
    assert VersionStr("3.2.0.20046") > "3.2.0.846"
    assert VersionStr("3.2.0.200") > VersionStr("3.2.0.2")
    assert not VersionStr("3.6.2.3.1") > "3.6.3.0"
    assert VersionStr("10.0.0.0") > ("9.6.0.0")
    assert not VersionStr("10.0.0.0") > ("10.0.0.0")
    assert ("0.2.10.0.0") > VersionStr("0.0.10.0.0")
    assert not ("0.0.1.0.0") > VersionStr("0.0.10.0.0")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testGreaterEqual():
    assert VersionStr("3.2.01.00") >= VersionStr("3.2.0.0")
    assert VersionStr("3.2.0.20046") >= "3.2.0.846"
    assert VersionStr("3.2.0.200") >= "3.2.0.2"
    assert not VersionStr("3.6.2.3.1") >= "3.6.3.0"
    assert VersionStr("10.0.0.0") >= VersionStr("9.6.0.0")
    assert VersionStr("10.0.0.0") >= ("10.0.0.0")
    assert ("0.2.10.0.0") >= VersionStr("0.0.10.0.0")
    assert not ("0.0.1.0.0") >= VersionStr("0.0.10.0.0")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testEqual():
    assert not VersionStr("3.2.01.00") == VersionStr("3.2.0.0")
    assert not VersionStr("3.2.0.20046") == "3.2.0.846"
    assert not VersionStr("3.2.0.200") == "3.2.0.2"
    assert not VersionStr("3.6.2.3.1") == "3.6.3.0"
    assert not VersionStr("10.0.0.0") == ("9.6.0.0")
    assert VersionStr("10.0.0.0") == ("10.0.0.0")
    assert not ("0.2.10.0.0") == VersionStr("0.0.10.0.0")
    assert not ("0.0.1.0.0") == VersionStr("0.0.10.0.0")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testNotEqual():
    assert VersionStr("3.2.01.00") != VersionStr("3.2.0.0")
    assert VersionStr("3.2.0.20046") != "3.2.0.846"
    assert VersionStr("3.2.0.200") != "3.2.0.2"
    assert VersionStr("3.6.2.3.1") != "3.6.3.0"
    assert VersionStr("10.0.0.0") != ("9.6.0.0")
    assert not VersionStr("10.0.0.0") != ("10.0.0.0")
    assert ("0.2.10.0.0") != VersionStr("0.0.10.0.0")
    assert ("0.0.1.0.0") != VersionStr("0.0.10.0.0")
