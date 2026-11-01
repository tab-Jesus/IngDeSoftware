# Guion de exposición - aproximadamente 6 a 8 minutos

**Presenta: Jesus Davod Campo.** Guion propuesto; video pendiente de grabar.

## 0:00 - Presentación y objetivo

Mi nombre es Jesus Davod Campo. Presento la actividad de la Unidad Tres de
Ingeniería de Software de la Universidad de Cartagena. Desarrollé un sistema
académico de nómina en Python usando programación orientada a objetos.

## 0:40 - Reglas y supuestos

Existen cuatro modalidades: asalariado, por horas, por comisión y temporal.
El asalariado recibe un bono del 10% solo después de cinco años. Las horas
superiores a cuarenta se pagan a una vez y media. La comisión depende de ventas;
si superan veinte millones, se suma un bono del 3% sobre todas las ventas.
Los temporales no tienen bonos ni alimentación adicional.

Mostrar el README. Explicar que usamos 4% para cada deducción y ARL de ejemplo
a cargo de la empresa. La guía no resuelve esos detalles; los valores se pueden
configurar y no se presentan como asesoría de nómina colombiana.

## 1:40 - Diseño orientado a objetos y SOLID

Abrir domain.py. Employee representa el contrato común. Las cuatro clases hijas
implementan earnings. El servicio no necesita preguntar qué tipo de empleado
recibe. La validación del período también es polimórfica.
DeductionPolicy separa los descuentos y puede inyectarse. Payslip es el resultado
inmutable. Explicar encapsulación mediante modelos válidos e inmutables,
abstracción mediante Employee, herencia y polimorfismo mediante sus variantes.

## 2:50 - Demostración real

Ejecutar `python -m nomina --csv evidencia/nomina_ejemplo.csv`.
Explicar asalariado: tres millones más trescientos mil de bono; los descuentos
de seguro y pensión son ciento treinta y dos mil cada uno; neto tres millones
treinta y seis mil. Alimentación y ARL se muestran separados.
Explicar horas: 40 por $20.000 más cinco por $30.000 = $950.000; descuentos
de $38.000, $38.000 y ahorro de $19.000; neto de $855.000.
Mostrar también comisión: bruto de cuatro millones y neto de $3.680.000;
temporal: bruto de $1.800.000 y neto de $1.656.000. Abrir el CSV.

## 4:10 - Pruebas y refactorización

Ejecutar `python -m unittest discover -s tests -v`. Mostrar el resultado real.
Abrir pruebas de cinco años, cuarenta horas, veinte millones y un año de
antigüedad. Explicar por qué exactamente el umbral no activa el beneficio.
Mostrar rechazo de valores negativos y del neto negativo.
Explicar el traslado de validate_period a las entidades y la separación de tasas.

## 5:20 - Metodología y control de versiones

Mostrar `git log --oneline`. Explicar los incrementos realmente registrados.
No atribuir cambios a integrantes que no participaron. Explicar backlog,
criterios de aceptación y verificación. Si ya publicó el repositorio, abrir
la dirección real en GitHub; si no, indicar que la publicación sigue pendiente.

## 6:10 - Cierre

La solución implementa las reglas con clases extensibles y cálculos decimales.
Los supuestos están documentados, las pruebas son reproducibles y la salida
puede exportarse a CSV. Como ampliaciones se podrían agregar almacenamiento
y una interfaz de captura, conservando las reglas del dominio.

## Antes de entregar

- Publicar el repositorio real y verificar los archivos visibles.
- Grabar la exposición y publicar el video; comprobar que el enlace sea accesible.
- Entregar PDF, enlace GitHub y enlace YouTube en SIMA según indique el docente.
- Confirmar la modalidad CIPA; registrar solo los participantes reales.
