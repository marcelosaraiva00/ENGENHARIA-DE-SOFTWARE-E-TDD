class SalaryCalculator:
    # Configurações centralizadas (Métrica: Facilidade de Manutenção)
    INSS_RATE = 0.08
    INSS_MAX = 500.00
    VT_RATE = 0.06
    DEP_DEDUCTION = 150.00
    
    IR_BRACKETS = [
        (4000, 0.20),
        (2000, 0.10),
        (0, 0.00)
    ]

    def calculate_net_salary(self, gross_salary, dependents=0, has_transport_voucher=False):
        self._validate_inputs(gross_salary, dependents)

        inss = self._calculate_inss(gross_salary)
        ir = self._calculate_ir(gross_salary, dependents)
        vt = self._calculate_vt(gross_salary, has_transport_voucher)

        return round(gross_salary - inss - ir - vt, 2)

    def _validate_inputs(self, salary, dep):
        if salary <= 0:
            raise ValueError("Salário bruto deve ser maior que zero")
        if dep < 0:
            raise ValueError("Número de dependentes não pode ser negativo")

    def _calculate_inss(self, salary):
        return min(salary * self.INSS_RATE, self.INSS_MAX)

    def _calculate_ir(self, salary, dep):
        # Encontra a alíquota baseada na faixa salarial
        rate = 0
        for limit, r in self.IR_BRACKETS:
            if salary > limit:
                rate = r
                break
        
        ir_raw = salary * rate
        return max(0, ir_raw - (dep * self.DEP_DEDUCTION))

    def _calculate_vt(self, salary, active):
        return (salary * self.VT_RATE) if active else 0
