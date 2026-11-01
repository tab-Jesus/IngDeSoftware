# Sistema de nómina - Actividad Unidad 3

**Autor: Jesus Davod Campo. Universidad de Cartagena. Ingeniería de Software.**

Solución académica en Python 3.10 o superior, con programación orientada a objetos,
cuatro tipos de empleados, políticas configurables y 25 pruebas unitarias.
La biblioteca estándar basta para ejecutar el sistema y sus pruebas.

## Ejecutar

Desde esta carpeta, en PowerShell o una terminal:

```powershell
python -m nomina
python -m nomina --csv evidencia/nomina_ejemplo.csv
python -m unittest discover -s tests -v
```

Los cuatro empleados del ejemplo son ficticios. Para liquidar otros datos, cree
instancias en Python de las clases de `nomina/domain.py` y use
`PayrollService().calculate(empleado, fecha_del_periodo)`.

## Organización

- `nomina/domain.py`: entidades, validación, política y servicio.
- `nomina/__main__.py`: demostración de consola y salida CSV.
- `tests/test_payroll.py`: pruebas de resultados, fronteras y entradas inválidas.
- `documentos/Informe_Unidad_3_Jesus_Davod_Campo.pdf`: informe académico.
- `documentos/guion_exposicion.md`: guion para grabar la exposición.
- `evidencia/`: CSV y registro real de pruebas.
- `tools/build_report.py`: fuente del informe; requiere ReportLab y PyMuPDF para QA.

## Decisiones ante ambigüedades de la guía

1. Seguro social: 4% del bruto; pensión: otro 4%. Es una interpretación académica.
   Si el docente indica 4% combinado, configurar 2% y 2% u otra distribución aprobada.
2. ARL: costo de la empresa, con tasa ilustrativa configurable de 0.522%.
   La guía no define tarifa ni pagador. No es una liquidación legal certificada.
3. Bruto = ordinario + bonos monetarios; la alimentación se entrega como beneficio
   separado cubierto por la empresa y no aumenta la base de deducciones del ejemplo.
4. Fondo: 2% del bruto retenido del pago y depositado al fondo, solo con antigüedad
   estrictamente mayor a un año y aceptación expresa. La guía no precisa financiación;
   aquí se interpreta como ahorro del empleado.
5. El umbral de 40 horas se aplica a las horas del período ingresado, sin presumir
   semanas ni multiplicar por cuatro. La guía combina referencias mensuales y horas
   sin definir el calendario. La demo evalúa cada regla para un período académico.
6. Contrato temporal: fecha del período dentro del rango inclusivo. Sin prorrateo,
   porque la guía no fija una regla para meses parciales.
7. Importes con Decimal y redondeo a dos decimales HALF_UP por concepto.

## SOLID y código limpio

SRP: cada entidad calcula sus ingresos; la política calcula descuentos; el servicio
orquesta; la CLI presenta y exporta. OCP: nuevas modalidades implementan `Employee`
sin añadir condicionales al servicio. LSP: todas las variantes respetan `earnings`,
`validate_period`, `food` y `saving_rate`; el contrato exige datos válidos y permite
rechazar un período no elegible. ISP: contrato pequeño sin métodos de interfaz de
usuario ni persistencia. DIP: `PayrollService` recibe la política por constructor y
usa el contrato `Employee`; se puede sustituir por otra política con las mismas
operaciones. Dataclasses inmutables, nombres explícitos y funciones cortas.

## Metodología

Desarrollo incremental inspirado en Scrum para una entrega individual: backlog de
reglas, modelado, implementación, verificación y documentación. No se afirma que
se hayan realizado ceremonias ni trabajo grupal. Criterio de terminado: los cuatro
tipos funcionan, todas las pruebas pasan y los supuestos están documentados.

La refactorización aplicada consistió en trasladar la validación del período a
`validate_period`, eliminando del servicio la consulta del tipo concreto temporal.
La política concentra porcentajes y evita repetición. Una prueba detectó un error
del valor esperado del costo con alimentación; se corrigió el oráculo, manteniendo
el beneficio de $1.000.000 definido por la guía.

## GitHub y exposición: pendientes externos

El paquete contiene un repositorio Git local con cambios reales. No prueba actividad
de integrantes de un CIPA. La publicación remota y la grabación no se han realizado.
Para publicar, cree un repositorio vacío en su cuenta de GitHub y ejecute:

```powershell
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

Sustituya USUARIO y REPOSITORIO por sus datos; no copie la URL de ejemplo como evidencia.
Grabe el guion con su voz, mostrando ejecución y pruebas; publique en YouTube y
entregue las URL reales en SIMA. La consigna dice entrega CIPA: confirme con el
docente si admite entrega individual o incorpore únicamente integrantes reales.

## Límites

Sin base de datos, interfaz gráfica, liquidación tributaria, prestaciones legales,
prorrateo o integración bancaria. No eran requeridos por el enunciado. Los costos
reportados comprenden únicamente los conceptos modelados en esta actividad.
