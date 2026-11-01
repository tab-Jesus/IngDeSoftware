"""Oráculos numéricos y fronteras de reglas de negocio."""
import unittest
from datetime import date
from decimal import Decimal as D
from nomina.domain import *

class PayrollTests(unittest.TestCase):
    def setUp(self):
        self.service = PayrollService()
        self.common = dict(identifier='1', name='Ejemplo')
        self.period = date(2026, 11, 1)

    def calculate(self, e):
        return self.service.calculate(e, self.period)

    def test_salaried_manual_oracle(self):
        p = self.calculate(Salaried(**self.common, salary=3000000, years=6))
        self.assertEqual((p.gross, p.net, p.food, p.arl, p.employer_cost),
                         (D('3300000'), D('3036000'), D('1000000'), D('17226'), D('4317226')))

    def test_five_years_no_bonus(self):
        self.assertEqual(Salaried(**self.common, salary=100, years=5).earnings()[1], 0)

    def test_over_five_bonus(self):
        self.assertEqual(Salaried(**self.common, salary=100, years='5.01').earnings()[1], 10)

    def test_hourly_manual_oracle(self):
        p = self.calculate(Hourly(**self.common, hours=45, hourly_rate=20000, years=2, accepts_savings=True))
        self.assertEqual((p.gross, p.savings, p.net, p.food), (D('950000'), D('19000'), D('855000'), 0))

    def test_forty_hours(self):
        self.assertEqual(Hourly(**self.common, hours=40, hourly_rate=100).earnings(), (4000, 0))

    def test_zero_hours(self):
        self.assertEqual(self.calculate(Hourly(**self.common, hours=0, hourly_rate=100)).net, 0)

    def test_one_year_no_savings(self):
        self.assertEqual(Hourly(**self.common, hours=1, hourly_rate=100, years=1, accepts_savings=True).saving_rate, 0)

    def test_savings_declined(self):
        self.assertEqual(Hourly(**self.common, hours=1, hourly_rate=100, years=2).saving_rate, 0)

    def test_commission_manual_oracle(self):
        p = self.calculate(Commission(**self.common, salary=2000000, sales=25000000, commission_rate='.05'))
        self.assertEqual((p.ordinary, p.bonus, p.net), (D('3250000'), D('750000'), D('3680000')))

    def test_sales_threshold(self):
        self.assertEqual(Commission(**self.common, salary=0, sales=20000000, commission_rate='.05').earnings()[1], 0)

    def test_sales_above_threshold(self):
        self.assertEqual(Commission(**self.common, salary=0, sales=20000001, commission_rate=0).earnings()[1], D('600000.03'))

    def test_zero_sales(self):
        self.assertEqual(Commission(**self.common, salary=100, sales=0, commission_rate='.05').earnings(), (100, 0))

    def temporary(self, **kw):
        return Temporary(**self.common, salary=1800000, start=date(2026, 1, 1), end=date(2026, 12, 31), **kw)

    def test_temporary_manual_oracle(self):
        p = self.calculate(self.temporary(years=8))
        self.assertEqual((p.net, p.food, p.bonus), (D('1656000'), 0, 0))

    def test_contract_boundaries(self):
        for day in (date(2026, 1, 1), date(2026, 12, 31)):
            self.assertEqual(self.service.calculate(self.temporary(), day).gross, 1800000)

    def test_outside_contract(self):
        with self.assertRaises(ValueError):
            self.service.calculate(self.temporary(), date(2027, 1, 1))

    def test_inverted_contract(self):
        with self.assertRaises(ValueError):
            Temporary(**self.common, salary=1, start=date(2026, 2, 1), end=date(2026, 1, 1))

    def test_negative_values(self):
        for value in (-1, 'NaN', 'Infinity'):
            for field in ('hours', 'hourly_rate'):
                data = dict(hours=1, hourly_rate=1)
                data[field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    Hourly(**self.common, **data)
            with self.assertRaises(ValueError):
                Commission(**self.common, salary=1, sales=value, commission_rate=0)
            with self.assertRaises(ValueError):
                Salaried(**self.common, salary=value)

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            Salaried(identifier='1', name=' ', salary=1)

    def test_negative_years(self):
        with self.assertRaises(ValueError):
            Salaried(**self.common, salary=1, years=-1)

    def test_invalid_commission(self):
        with self.assertRaises(ValueError):
            Commission(**self.common, salary=1, sales=1, commission_rate='1.01')

    def test_invalid_policy(self):
        for rate in ('-.1', '1.1', 'NaN'):
            with self.assertRaises(ValueError):
                DeductionPolicy(arl_rate=rate)

    def test_negative_net_rejected(self):
        service = PayrollService(DeductionPolicy(social_rate='.9', pension_rate='.9'))
        with self.assertRaises(ValueError):
            service.calculate(Salaried(**self.common, salary=100), self.period)

    def test_configurable_deductions(self):
        service = PayrollService(DeductionPolicy(social_rate='.02', pension_rate='.02', arl_rate=0))
        self.assertEqual(service.calculate(Salaried(**self.common, salary=100), self.period).net, 96)

    def test_round_half_up(self):
        self.assertEqual(money(D('1.005')), D('1.01'))

    def test_food_not_deducted(self):
        p = self.calculate(Salaried(**self.common, salary=100))
        self.assertEqual(p.net, 92)
        self.assertEqual(p.employer_cost, D('1000100.52'))

if __name__ == '__main__':
    unittest.main()
