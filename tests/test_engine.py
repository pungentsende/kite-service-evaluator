import unittest

from kite_evaluator.engine import evaluate


BASE = {"name": "demo", "network": "kite-testnet", "payTo": "0x0b4825f1280d32ce58f0ca0b46808f4d34ac8686", "routes": [{"path": "/v1/data", "amount": "0.01"}]}


class EvaluatorTests(unittest.TestCase):
    def test_accepts_a_small_manifest(self):
        self.assertEqual(evaluate(BASE), [])


    def test_reports_duplicate_paths_and_bad_amounts(self):
        findings = evaluate({**BASE, "routes": [{"path": "/x", "amount": "0"}, {"path": "/x", "amount": "nope"}]})
        self.assertEqual({item.code for item in findings}, {"invalid-amount", "duplicate-path"})


    def test_does_not_accept_a_non_evm_recipient(self):
        self.assertTrue(any(item.code == "invalid-pay-to" for item in evaluate({**BASE, "payTo": "alice"})))
