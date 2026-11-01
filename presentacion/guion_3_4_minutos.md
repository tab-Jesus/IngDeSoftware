# Guion de exposición · 3 a 4 minutos

**Jesus Davod Campo · Ingeniería de Software · Universidad de Cartagena**

Tiempo orientativo: 3:40, a un ritmo de 125 a 135 palabras por minuto, incluyendo pausas breves para cambiar de diapositiva. No leas las indicaciones entre corchetes.

## 1. Sistema de nómina · 0:00–0:30

Buenos días. Mi nombre es Jesus Davod Campo y voy a presentar el sistema de nómina desarrollado para la Unidad Tres de Ingeniería de Software.

El objetivo es calcular cuánto recibe un empleado según su modalidad de contratación, considerando ingresos, beneficios y deducciones. Para resolverlo utilicé Python y programación orientada a objetos, separando las reglas del negocio de la presentación de los resultados.

[Avanza a las modalidades.]

## 2. Cuatro modalidades · 0:30–1:20

El sistema contempla cuatro tipos de empleados. El asalariado recibe un salario fijo y un bono del diez por ciento cuando supera cinco años en la empresa. El empleado por horas recibe su tarifa normal hasta cuarenta horas; las adicionales se pagan a una vez y media esa tarifa.

El empleado por comisión recibe salario base más un porcentaje de sus ventas. Si estas superan veinte millones de pesos, obtiene un bono adicional del tres por ciento sobre las ventas. Finalmente, el temporal recibe un salario fijo dentro de las fechas de su contrato.

También se consideran alimentación para los permanentes y ahorro voluntario para empleados por horas que cumplen la antigüedad requerida.

[Avanza al diseño.]

## 3. Diseño con SOLID · 1:20–2:00

La clase Employee define el comportamiento común y cada modalidad implementa su propia forma de calcular ingresos. Esto permite usar polimorfismo y agregar nuevos tipos de empleado sin introducir condicionales por tipo en el servicio.

Los porcentajes de descuentos están separados en DeductionPolicy, mientras PayrollService coordina el cálculo. Esta distribución aplica responsabilidad única e inversión de dependencias.

Durante la refactorización, la validación del período temporal se trasladó a la entidad correspondiente. Así, el servicio quedó más sencillo y las reglas permanecieron verificables mediante pruebas.

[Avanza al ejemplo numérico.]

## 4. Ejemplo de liquidación · 2:00–2:55

En este ejemplo, el empleado trabaja cuarenta y cinco horas a una tarifa de veinte mil pesos. Las cuarenta horas normales suman ochocientos mil pesos y las cinco extras suman ciento cincuenta mil. El salario bruto es, por tanto, de novecientos cincuenta mil pesos.

Para el ejercicio se asume un cuatro por ciento de seguro y otro cuatro por ciento de pensión. Cada descuento equivale a treinta y ocho mil pesos. Como el empleado cumple los requisitos y acepta el fondo, también se descuentan diecinueve mil pesos de ahorro.

El resultado es un neto de ochocientos cincuenta y cinco mil pesos. La ARL se registra aparte como costo empresarial. Estos supuestos están documentados y las tasas pueden configurarse.

[Avanza a las pruebas.]

## 5. Verificación y cierre · 2:55–3:40

La solución cuenta con veinticinco pruebas unitarias aprobadas. Verifican cálculos manuales, límites de antigüedad, horas y ventas, además del rechazo de entradas inválidas y salarios netos negativos.

El desarrollo se organizó en incrementos de análisis, implementación, verificación y documentación. En GitHub están disponibles el código, el informe, los resultados de ejemplo y los materiales de exposición.

Con este proyecto se demuestra cómo la programación orientada a objetos y los principios SOLID ayudan a organizar reglas diferentes y comprobar su funcionamiento. Como mejora futura se podría incorporar una interfaz de captura y almacenamiento de empleados. Muchas gracias.
