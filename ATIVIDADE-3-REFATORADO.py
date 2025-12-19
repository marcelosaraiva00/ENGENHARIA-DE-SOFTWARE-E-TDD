class SalaryCalculator:
    INSS_RATE = 0.08
    INSS_MAX = 500.00

    IR_LIMIT_1 = 2000.00
    IR_LIMIT_2 = 4000.00
    IR_RATE_1 = 0.10
    IR_RATE_2 = 0.20

    TRANSPORT_RATE = 0.06
    DEPENDENT_DEDUCTION = 150.00

    def calculate_net_salary(
        self,
        gross_salary: float,
        dependents: int = 0,
        has_transport_voucher: bool = False
    ) -> float:
        self._validate_inputs(gross_salary, dependents)

        inss = self._calculate_inss(gross_salary)
        ir = self._calculate_ir(gross_salary, dependents)
        transport = self._calculate_transport(gross_salary, has_transport_voucher)

        net_salary = gross_salary - inss - ir - transport
        return round(net_salary, 2)

    # ---------------- Métodos privados ----------------

    def _validate_inputs(self, gross_salary, dependents):
        if gross_salary <= 0:
            raise ValueError("Salário bruto deve ser maior que zero")
        if dependents < 0:
            raise ValueError("Número de dependentes inválido")

    def _calculate_inss(self, gross_salary):
        return min(gross_salary * self.INSS_RATE, self.INSS_MAX)

    def _calculate_ir(self, gross_salary, dependents):
        ir = self._base_ir(gross_salary)
        deduction = dependents * self.DEPENDENT_DEDUCTION
        return max(ir - deduction, 0.0)

    def _base_ir(self, gross_salary):
        if gross_salary <= self.IR_LIMIT_1:
            return 0.0
        if gross_salary <= self.IR_LIMIT_2:
            return gross_salary * self.IR_RATE_1
        return gross_salary * self.IR_RATE_2

    def _calculate_transport(self, gross_salary, has_transport_voucher):
        return gross_salary * self.TRANSPORT_RATE if has_transport_voucher else 0.0
