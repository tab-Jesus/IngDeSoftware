"""Demostración reproducible y exportación CSV sin librerías externas."""
import argparse
import csv
from dataclasses import asdict
from datetime import date
from pathlib import Path
from .domain import Salaried, Hourly, Commission, Temporary, PayrollService

def main():
    parser = argparse.ArgumentParser(description='Nómina académica - Unidad 3')
    parser.add_argument('--csv', type=Path, help='Ruta del reporte CSV')
    args = parser.parse_args()
    employees = [
        Salaried(identifier='E01', name='Empleado asalariado (ejemplo)', years=6, salary=3000000),
        Hourly(identifier='E02', name='Empleado por horas (ejemplo)', years=2,
               hours=45, hourly_rate=20000, accepts_savings=True),
        Commission(identifier='E03', name='Empleado por comisión (ejemplo)', years=3,
                   salary=2000000, sales=25000000, commission_rate='0.05'),
        Temporary(identifier='E04', name='Empleado temporal (ejemplo)', salary=1800000,
                  start=date(2026, 1, 1), end=date(2026, 12, 31)),
    ]
    service = PayrollService()
    rows = [asdict(service.calculate(e, date(2026, 11, 1))) for e in employees]
    for row in rows:
        print(f"{row['identifier']} | bruto: ${row['gross']:,.2f} | neto: ${row['net']:,.2f} | costo empresa: ${row['employer_cost']:,.2f}")
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open('w', encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f'Reporte guardado en {args.csv}')

if __name__ == '__main__':
    main()
