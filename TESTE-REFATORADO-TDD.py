from __future__ import annotations
import unittest
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Union, Dict

Number = Union[int, float, str, Decimal]


@dataclass(frozen=True)
class SalaryRules:
    """
    Regras fiscais isoladas para facilitar manutenção.
    Alterar alíquotas/limites não exige mexer na lógica.
    """
    inss_rate: Decimal = Decimal("0.08")
    ir_limit: Decimal = Decimal("2000.00")
    ir_rate: Decimal = Decimal("0.10")
    money_scale: Decimal = Decimal("0.01")  # 2 casas decimais
    rounding_mode = ROUND_HALF_UP


class SalaryCalculator:
    def __init__(self, rules: SalaryRules | None = None) -> None:
        self._rules = rules or SalaryRules()

    def calculate_net_salary(self, gross_salary: Number) -> Decimal:
        gross = self._parse_money(gross_salary)
        self._validate_salary(gross)

        discounts = self._calculate_discounts(gross)
        net = gross - discounts["inss"] - discounts["ir"]

        return self._quantize_money(net)

    def calculate_discounts(self, gross_salary: Number) -> Dict[str, Decimal]:
        """
        Método auxiliar para testes: facilita validar INSS/IR isoladamente,
        ajudando a reduzir defeitos detectados tardiamente.
        """
        gross = self._parse_money(gross_salary)
        self._validate_salary(gross)
        return self._calculate_discounts(gross)

    def _calculate_discounts(self, gross: Decimal) -> Dict[str, Decimal]:
        inss = self._calculate_inss(gross)
        ir = self._calculate_ir(gross)
        return {"inss": inss, "ir": ir}

    def _validate_salary(self, gross_salary: Decimal) -> None:
        if gross_salary <= 0:
            raise ValueError("Salário bruto deve ser maior que zero")

    def _calculate_inss(self, gross_salary: Decimal) -> Decimal:
        return self._quantize_money(gross_salary * self._rules.inss_rate)

    def _calculate_ir(self, gross_salary: Decimal) -> Decimal:
        if gross_salary <= self._rules.ir_limit:
            return self._quantize_money(Decimal("0"))
        return self._quantize_money(gross_salary * self._rules.ir_rate)

    def _parse_money(self, value: Number) -> Decimal:
        try:
            # str(...) evita alguns problemas clássicos de float binário
            dec = Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            raise TypeError("Salário bruto deve ser numérico") from None
        return dec

    def _quantize_money(self, value: Decimal) -> Decimal:
        return value.quantize(self._rules.money_scale, rounding=self._rules.rounding_mode)
