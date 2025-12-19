class SalaryCalculator:

    INSS_RATE = 0.08
    IR_LIMIT = 2000.00
    IR_RATE = 0.10

    def calculate_net_salary(self, gross_salary):
        self._validate_salary(gross_salary)

        inss_discount = self._calculate_inss(gross_salary)
        ir_discount = self._calculate_ir(gross_salary)

        net_salary = gross_salary - inss_discount - ir_discount
        return round(net_salary, 2)

    def _validate_salary(self, gross_salary):
        if gross_salary <= 0:
            raise ValueError("Salário bruto deve ser maior que zero")

    def _calculate_inss(self, gross_salary):
        return gross_salary * self.INSS_RATE

    def _calculate_ir(self, gross_salary):
        if gross_salary <= self.IR_LIMIT:
            return 0.0
        return gross_salary * self.IR_RATE