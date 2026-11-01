"""Modelos y políticas: importes decimales, sin dependencias de interfaz."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

D = Decimal

def amount(value):
    result = D(str(value))
    if not result.is_finite() or result < 0:
        raise ValueError('El valor debe ser finito y no negativo')
    return result

def money(value):
    return value.quantize(D('0.01'), rounding=ROUND_HALF_UP)

@dataclass(frozen=True, kw_only=True)
class Employee(ABC):
    identifier: str
    name: str
    years: Decimal = D('0')

    def __post_init__(self):
        if not self.identifier.strip() or not self.name.strip():
            raise ValueError('Identificador y nombre son obligatorios')
        object.__setattr__(self, 'years', amount(self.years))

    @abstractmethod
    def earnings(self):
        """Retorna pago ordinario y bono monetario del período."""

    def validate_period(self, period: date):
        """Los empleados sin contrato temporal aceptan cualquier período."""

    @property
    def food(self):
        return D('0')

    @property
    def saving_rate(self):
        return D('0')

@dataclass(frozen=True, kw_only=True)
class Salaried(Employee):
    salary: Decimal

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(self, 'salary', amount(self.salary))

    def earnings(self):
        return self.salary, self.salary * D('0.10') if self.years > 5 else D('0')

    @property
    def food(self):
        return D('1000000')

@dataclass(frozen=True, kw_only=True)
class Hourly(Employee):
    hours: Decimal
    hourly_rate: Decimal
    accepts_savings: bool = False

    def __post_init__(self):
        super().__post_init__()
        for field in ('hours', 'hourly_rate'):
            object.__setattr__(self, field, amount(getattr(self, field)))
        if not isinstance(self.accepts_savings, bool):
            raise ValueError('La aceptación del fondo debe ser booleana')

    def earnings(self):
        regular = min(self.hours, D('40')) * self.hourly_rate
        overtime = max(self.hours - 40, D('0')) * self.hourly_rate * D('1.5')
        return regular + overtime, D('0')

    @property
    def saving_rate(self):
        return D('0.02') if self.years > 1 and self.accepts_savings else D('0')

@dataclass(frozen=True, kw_only=True)
class Commission(Employee):
    salary: Decimal
    sales: Decimal
    commission_rate: Decimal

    def __post_init__(self):
        super().__post_init__()
        for field in ('salary', 'sales', 'commission_rate'):
            object.__setattr__(self, field, amount(getattr(self, field)))
        if self.commission_rate > 1:
            raise ValueError('La comisión debe estar entre 0 y 1')

    def earnings(self):
        base = self.salary + self.sales * self.commission_rate
        return base, self.sales * D('0.03') if self.sales > 20000000 else D('0')

    @property
    def food(self):
        return D('1000000')

@dataclass(frozen=True, kw_only=True)
class Temporary(Employee):
    salary: Decimal
    start: date
    end: date

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(self, 'salary', amount(self.salary))
        if self.end < self.start:
            raise ValueError('La fecha final debe ser posterior o igual a la inicial')

    def earnings(self):
        return self.salary, D('0')

    def validate_period(self, period: date):
        if not self.start <= period <= self.end:
            raise ValueError('El período está fuera del contrato temporal')

@dataclass(frozen=True)
class DeductionPolicy:
    """Supuesto académico: 4% seguro y 4% pensión; ARL a cargo de empresa."""
    social_rate: Decimal = D('0.04')
    pension_rate: Decimal = D('0.04')
    arl_rate: Decimal = D('0.00522')

    def __post_init__(self):
        for field in ('social_rate', 'pension_rate', 'arl_rate'):
            value = amount(getattr(self, field))
            if value > 1:
                raise ValueError('Las tasas deben estar entre 0 y 1')
            object.__setattr__(self, field, value)

    def deductions(self, gross):
        return money(gross * self.social_rate), money(gross * self.pension_rate)

    def employer_arl(self, gross):
        return money(gross * self.arl_rate)

@dataclass(frozen=True)
class Payslip:
    identifier: str
    name: str
    ordinary: Decimal
    bonus: Decimal
    gross: Decimal
    social: Decimal
    pension: Decimal
    savings: Decimal
    net: Decimal
    food: Decimal
    arl: Decimal
    employer_cost: Decimal

class PayrollService:
    """Depende del contrato de empleado y de una política inyectada."""
    def __init__(self, policy=None):
        self.policy = policy if policy is not None else DeductionPolicy()

    def calculate(self, employee: Employee, period: date):
        employee.validate_period(period)
        ordinary, bonus = map(money, employee.earnings())
        gross = ordinary + bonus
        social, pension = self.policy.deductions(gross)
        savings = money(gross * employee.saving_rate)
        net = gross - social - pension - savings
        if net < 0:
            raise ValueError('Las deducciones generan un salario neto negativo')
        food = money(employee.food)
        arl = self.policy.employer_arl(gross)
        return Payslip(employee.identifier, employee.name, ordinary, bonus, gross,
                       social, pension, savings, net, food, arl, gross + food + arl)
