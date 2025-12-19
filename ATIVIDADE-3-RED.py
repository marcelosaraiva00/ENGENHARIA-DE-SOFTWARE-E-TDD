class SalaryCalculator:
    INSS_RATE = 0.08
    INSS_TETO = 500.00
    VT_RATE = 0.06
    DEP_DEDUCTION = 150.00

    def calculate_net_salary(self, gross_salary, dependents=0, has_transport_voucher=False):
        # Validações (Passa nos testes de ValueError)
        if gross_salary <= 0:
            raise ValueError("Salário deve ser maior que zero.")
        if dependents < 0:
            raise ValueError("Número de dependentes não pode ser negativo.")

        # Cálculo INSS com Teto
        inss = min(gross_salary * self.INSS_RATE, self.INSS_TETO)

        # Cálculo IR Progressivo
        if gross_salary <= 2000:
            ir_base = 0
        elif gross_salary <= 4000:
            ir_base = gross_salary * 0.10
        else:
            ir_base = gross_salary * 0.20

        # Dedução por dependentes (Não pode ser negativo)
        ir_final = max(0, ir_base - (dependents * self.DEP_DEDUCTION))

        # Vale-Transporte
        vt_discount = (gross_salary * self.VT_RATE) if has_transport_voucher else 0

        # Resultado Final
        net_salary = gross_salary - inss - ir_final - vt_discount
        return round(net_salary, 2)
