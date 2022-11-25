import unittest

from MergeGoogleDocWithIpynb.Utility import Utility


class test_Utility(unittest.TestCase):

    def test_standardizeStr(self):
        expect = "asdfaasda__dafj__asdfvnxc"
        self.assertEqual(expect, Utility.standardizeStr("asdf AASDA__\ndafj\t..asdfvNXC\n\n\n\t\n\t"))

    def test_getCodeCellId(self):
        expectNone = ["code ", "abcd 1", "", "# xxx code 1"]
        for i in expectNone:
            self.assertIsNone(Utility.getCodeCellId(i))

        expect = '1'
        needToTest = ["code1", "Code 1", "CODE   1", "code:1"]
        for i in needToTest:
            self.assertEqual(expect, Utility.getCodeCellId(i))

        expect = '1_a'
        needToTest = ["code1.a", "Code 1.A", "CODE   1_a", "code:1_A"]
        for i in needToTest:
            self.assertEqual(expect, Utility.getCodeCellId(i))

        self.assertEqual("10_12", Utility.getCodeCellId("code 10.12"))

        self.assertEqual("10_12_a", Utility.getCodeCellId("code 10.12.A"))

        self.assertEqual("10_12_34_b", Utility.getCodeCellId("code 10.12.34.b"))

        self.assertEqual("e_10_12_34_b", Utility.getCodeCellId("code e.10.12.34.b"))
