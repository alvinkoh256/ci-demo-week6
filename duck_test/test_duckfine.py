import unittest
from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def test_init_sets_member_and_zero_owed(self):
        d = DuckFine('m1')
        self.assertEqual(d.member_id, 'm1')
        self.assertEqual(d.total_owed, 0.0)

    def test_no_fee_when_on_time(self):
        d = DuckFine('m1')
        self.assertEqual(d.charge(0), 0.0)

    def test_no_fee_within_grace_period(self):
        d = DuckFine('m1')
        self.assertEqual(d.charge(2), 0.0)

    def test_fee_after_grace_period(self):
        d = DuckFine('m1')
        self.assertAlmostEqual(d.charge(3), 0.50)

    def test_fee_scales_per_day(self):
        d = DuckFine('m1')
        self.assertAlmostEqual(d.charge(6), 2.00)

    def test_deluxe_doubles_fee(self):
        d = DuckFine('m1')
        self.assertAlmostEqual(d.charge(6, deluxe=True), 4.00)

    def test_deluxe_within_grace_still_zero(self):
        d = DuckFine('m1')
        self.assertEqual(d.charge(2, deluxe=True), 0.0)

    def test_fee_capped_at_max(self):
        d = DuckFine('m1')
        self.assertAlmostEqual(d.charge(100), 5.00)

    def test_deluxe_fee_capped_at_max(self):
        d = DuckFine('m1')
        self.assertAlmostEqual(d.charge(12, deluxe=True), 5.00)

    def test_total_owed_accumulates(self):
        d = DuckFine('m1')
        d.charge(3)
        d.charge(4)
        self.assertAlmostEqual(d.total_owed, 0.50 + 1.00)

    def test_negative_days_raises(self):
        d = DuckFine('m1')
        with self.assertRaises(ValueError):
            d.charge(-1)


if __name__ == '__main__':
    unittest.main()
