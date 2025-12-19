import unittest


class SalaryCalculator:
    INSS_RATE = 0.08
    IR_LIMIT = 2000.00
    IR_RATE = 0.10

    def calculate_net_salary(self, gross_salary):
        if gross_salary <= 0:
            raise ValueError("Salário bruto deve ser maior que zero")

        inss = gross_salary * self.INSS_RATE

        if gross_salary <= self.IR_LIMIT:
            ir = 0
        else:
            ir = gross_salary * self.IR_RATE

        net_salary = gross_salary - inss - ir
        return round(net_salary, 2)


class TestSalaryCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = SalaryCalculator()

    def test_should_raise_error_for_zero_salary(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_net_salary(0)

    def test_should_raise_error_for_negative_salary(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_net_salary(-100)

    def test_should_round_result_to_two_decimal_places(self):
        gross_salary = 1999.99
        result = self.calculator.calculate_net_salary(gross_salary)
        decimal_part = str(result).split(".")[1]
        self.assertEqual(len(decimal_part), 2)


if __name__ == "__main__":
    unittest.main()