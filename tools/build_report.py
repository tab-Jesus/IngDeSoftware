"""Genera el informe académico del sistema de nómina en blanco y negro."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'documentos/Informe_Unidad_3_Jesus_Davod_Campo.pdf'
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyAcademic', fontName='Times-Roman', fontSize=11.5, leading=16, spaceAfter=11, alignment=4))
styles.add(ParagraphStyle(name='CoverAcademic', fontName='Times-Roman', fontSize=12, leading=19, spaceAfter=14, alignment=1))
styles.add(ParagraphStyle(name='TitleAcademic', fontName='Times-Bold', fontSize=25, leading=31, spaceAfter=22, alignment=1))
styles.add(ParagraphStyle(name='HeadingAcademic', fontName='Times-Bold', fontSize=17, leading=23, spaceAfter=17))
styles.add(ParagraphStyle(name='CellAcademic', fontName='Times-Roman', fontSize=10, leading=13, spaceAfter=4))
styles.add(ParagraphStyle(name='ReferenceAcademic', fontName='Times-Roman', fontSize=10.5, leading=14, spaceAfter=10))
story = []

def p(text):
    story.append(Paragraph(text, styles['BodyAcademic']))

def cp(text):
    story.append(Paragraph(text, styles['CoverAcademic']))

def h(text):
    story.append(Paragraph(text, styles['HeadingAcademic']))

def page():
    story.append(PageBreak())

def table(headers, rows, widths):
    data = [[Paragraph(str(v), styles['CellAcademic']) for v in row] for row in [[f'<b>{v}</b>' for v in headers]] + rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEABOVE', (0, 0), (-1, 0), .8, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), .6, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), .8, colors.black),
    ]))
    story.extend([t, Spacer(1, 14)])

story.append(Spacer(1, 58))
cp('UNIVERSIDAD DE CARTAGENA<br/>Programa de Ingeniería de Software')
story.append(Spacer(1, 35))
story.append(Paragraph('Sistema de nómina<br/>orientado a objetos', styles['TitleAcademic']))
cp('ACTIVIDAD UNIDAD TRES<br/>INGENIERÍA DE SOFTWARE')
story.append(Spacer(1, 38))
cp('<b>Jesus Davod Campo</b><br/>Autor')
story.append(Spacer(1, 25))
cp('Cartagena de Indias<br/>1 de noviembre de 2026')
story.append(Spacer(1, 35))
cp('<b>Repositorio del proyecto</b><br/><link href="https://github.com/tab-Jesus/IngDeSoftware">https://github.com/tab-Jesus/IngDeSoftware</link>')
story.append(Spacer(1, 12))
cp('<b>Video de exposición</b>')
story.append(Paragraph('<link href="https://drive.google.com/drive/folders/12X3QH36apLfZmf3hXu9CXgjdpZZKqqcB?hl=es">https://drive.google.com/drive/folders/12X3QH36apLfZmf3hXu9CXgjdpZZKqqcB?hl=es</link>', ParagraphStyle(name='VideoURL', fontName='Times-Roman', fontSize=10, leading=15, alignment=1)))

page()
h('1. Introducción, objetivos y requisitos')
p('El cálculo de una nómina requiere aplicar reglas diferentes según la modalidad de vinculación del empleado. El proyecto resuelve este problema mediante un modelo orientado a objetos que distingue los ingresos, los beneficios, las deducciones y el costo empresarial de cada liquidación. Las reglas funcionales corresponden a la Actividad Unidad Tres de Ingeniería de Software [1].')
p('<b>Objetivo general.</b> Desarrollar un sistema de nómina en Python que calcule los valores de cuatro modalidades de empleado mediante programación orientada a objetos y principios SOLID.')
p('<b>Objetivos específicos.</b> Modelar las modalidades de contratación; separar responsabilidades; validar los datos; calcular importes con precisión decimal; comprobar las reglas mediante pruebas unitarias y exportar resultados a CSV.')
table(['Requisito', 'Comportamiento implementado'], [
    ['Asalariado', 'Salario fijo mensual y bono del 10% cuando la antigüedad supera cinco años.'],
    ['Por horas', 'Hasta 40 horas a tarifa normal; las adicionales se pagan a 1,5 veces la tarifa. Sin bono monetario.'],
    ['Por comisión', 'Base más comisión sobre ventas. Bono del 3% sobre todas las ventas cuando superan $20.000.000.'],
    ['Temporal', 'Salario fijo y contrato con fechas inicial y final. Sin bonos ni alimentación adicional.'],
    ['Beneficios', 'Alimentación de $1.000.000 para permanentes. Ahorro del 2% para empleados por horas con más de un año y aceptación.'],
    ['Validaciones', 'Rechazo de horas y ventas negativas, datos no finitos y liquidaciones con neto negativo.'],
    ['Calidad', 'Diseño SOLID, funciones con responsabilidades delimitadas, comentarios, refactorización y pruebas unitarias.'],
], [115, 370])
p('<b>Alcance.</b> La aplicación procesa datos de demostración por consola y genera comprobantes desglosados y un reporte CSV. El dominio permite construir otros empleados y calcular nuevos escenarios mediante sus clases y servicios.')

page()
h('2. Reglas de cálculo y criterios del modelo')
p('La liquidación diferencia el salario bruto, el valor neto del empleado y el costo empresarial. Los porcentajes de seguro, pensión y ARL se concentran en una política configurable. Para los ejemplos y las pruebas se adoptaron los siguientes criterios:')
table(['Concepto', 'Criterio aplicado'], [
    ['Seguro y pensión', 'Se interpreta el porcentaje del enunciado como 4% del bruto para seguro y otro 4% para pensión. Esta distribución es un supuesto del modelo y puede modificarse en DeductionPolicy.'],
    ['ARL', 'Aporte empresarial separado del neto, calculado con una tasa ilustrativa configurable del 0,522%.'],
    ['Alimentación', 'Beneficio de $1.000.000 para asalariados y empleados por comisión; se registra separado del bruto y del neto.'],
    ['Ahorro', 'Retención del 2% del bruto destinada al fondo, únicamente para empleados por horas con más de un año y aceptación expresa.'],
    ['Período', 'El umbral de 40 horas se aplica a las horas ingresadas. En contratos temporales, la fecha de liquidación debe estar dentro del intervalo, incluidos sus extremos. Sin prorrateo.'],
    ['Precisión', 'Importes con Decimal [2]. Redondeo ROUND_HALF_UP a dos decimales por concepto. El bruto suma el ordinario y el bono previamente redondeados.'],
], [110, 375])
p('<b>Fórmulas generales</b><br/>Bruto = pago ordinario + bono monetario.<br/>Seguro = bruto × tasa de seguro.<br/>Pensión = bruto × tasa de pensión.<br/>Ahorro = bruto × 2%, cuando aplica.<br/>Neto = bruto - seguro - pensión - ahorro.<br/>Costo empresarial modelado = bruto + alimentación + ARL.')
p('Los límites de antigüedad y ventas se evalúan de forma estricta: exactamente cinco años no generan el bono del asalariado; exactamente un año no habilita el ahorro y ventas de $20.000.000 no activan el bono adicional de comisión.')

page()
h('3. Diseño orientado a objetos')
p('<b>Abstracción.</b> Employee define el contrato común del empleado mediante una clase abstracta de Python [3]. Su operación earnings() representa la obtención de ingresos, y validate_period() verifica la elegibilidad del período.')
p('<b>Herencia y polimorfismo.</b> Salaried, Hourly, Commission y Temporary especializan el contrato. El servicio invoca las mismas operaciones y recibe resultados calculados según la modalidad, sin consultar el tipo concreto del empleado.')
p('<b>Encapsulación.</b> Las entidades validan sus atributos al construirse y usan dataclasses inmutables [4]. De esta manera, los cálculos parten de objetos cuyo nombre, identificación y valores numéricos cumplen las restricciones del modelo.')
table(['Elemento', 'Responsabilidad'], [
    ['Employee', 'Contrato de ingresos, período, alimentación y tasa de ahorro.'],
    ['Clases de empleados', 'Reglas particulares de salario, bono, beneficios y elegibilidad.'],
    ['DeductionPolicy', 'Validación de tasas; cálculo de seguro, pensión y ARL empresarial.'],
    ['PayrollService', 'Coordinación de ingresos y deducciones; validación del neto y generación del resultado.'],
    ['Payslip', 'Comprobante inmutable con ingresos, descuentos, beneficios y costo empresarial.'],
    ['Consola y CSV', 'Presentación de ejemplos y exportación del desglose.'],
], [150, 335])
p('<b>Secuencia de liquidación.</b> Primero se valida el período. Después se obtienen y redondean el pago ordinario y el bono para formar el bruto. Se calculan seguro, pensión y ahorro; se verifica que el neto sea no negativo y se incorporan alimentación y ARL al comprobante.')
p('<b>Extensión.</b> Una modalidad adicional puede implementar el contrato Employee y reutilizar PayrollService. La separación entre dominio y salida permite desarrollar otras interfaces sobre las mismas reglas.')

page()
h('4. SOLID, código limpio y refactorización')
table(['Principio', 'Aplicación en el proyecto'], [
    ['S: responsabilidad única', 'Las entidades calculan ingresos; la política calcula descuentos; el servicio coordina; la consola presenta y exporta.'],
    ['O: abierto/cerrado', 'Las nuevas modalidades se incorporan mediante especialización de Employee, sin agregar condicionales por tipo al servicio.'],
    ['L: sustitución de Liskov', 'Las modalidades proporcionan las operaciones del contrato común y expresan su elegibilidad mediante validate_period().'],
    ['I: segregación de interfaces', 'El contrato del empleado se limita al dominio de nómina y no exige funciones de impresión, persistencia ni interfaz gráfica.'],
    ['D: inversión de dependencias', 'PayrollService utiliza el contrato Employee y recibe la política de descuentos por constructor, lo que permite sustituirla por otra compatible.'],
], [145, 340])
p('<b>Organización del código.</b> Se emplearon nombres descriptivos, funciones breves y validaciones próximas a la definición de los datos. Las operaciones amount() y money() centralizan la validación numérica y el redondeo para evitar repetir criterios en cada modalidad.')
p('<b>Comentarios.</b> Las cadenas de documentación explican los contratos de las clases y las decisiones relevantes, como el tratamiento de deducciones y la responsabilidad del servicio. Los comentarios complementan la lectura de los nombres y las operaciones.')
p('<b>Refactorización.</b> La comprobación del período temporal se trasladó al método validate_period() de la entidad. El servicio pasó de identificar una modalidad concreta a solicitar una validación polimórfica. También se separaron las tasas en DeductionPolicy y el resultado en Payslip.')
p('<b>Comprobación del comportamiento.</b> Los resultados esperados de las pruebas se expresan como valores numéricos explícitos. Esto permite contrastar la liquidación con cálculos manuales y comprobar la consistencia del servicio tras la reorganización de responsabilidades.')

page()
h('5. Pruebas unitarias y resultados')
p('La suite de validación contiene 25 pruebas ejecutadas con unittest [5]. Se comprobaron cálculos de las cuatro modalidades, condiciones de frontera, configuración alternativa de tasas, redondeo y rechazo de datos inválidos. El resultado de la ejecución fue de 25 pruebas aprobadas, sin fallos.')
table(['Caso de demostración', 'Bruto', 'Neto', 'Costo empresa'], [
    ['Asalariado: $3.000.000; 6 años', '$3.300.000', '$3.036.000', '$4.317.226'],
    ['Horas: 45 a $20.000; con ahorro', '$950.000', '$855.000', '$954.959'],
    ['Comisión: base $2.000.000; ventas $25.000.000; tasa 5%', '$4.000.000', '$3.680.000', '$5.020.880'],
    ['Temporal: salario $1.800.000', '$1.800.000', '$1.656.000', '$1.809.396'],
], [180, 100, 100, 105])
p('<b>Verificación del ejemplo por horas.</b> Las 40 horas normales suman $800.000 y las cinco horas extras suman $150.000. Sobre el bruto de $950.000 se descuentan $38.000 de seguro, $38.000 de pensión y $19.000 de ahorro. El neto es $855.000. La ARL empresarial es $4.959 y el costo modelado de la empresa es $954.959.')
table(['Grupo de pruebas', 'Casos comprobados'], [
    ['Resultados', 'Valores esperados para asalariado, horas, comisión y temporal; alimentación separada del neto.'],
    ['Fronteras', 'Cinco años y antigüedad superior; 40 horas; ventas iguales y superiores a $20.000.000; un año de antigüedad y aceptación del ahorro.'],
    ['Datos y contrato', 'Valores negativos y no finitos; nombre vacío; tasas fuera de rango; fechas invertidas, extremas y fuera del contrato.'],
    ['Consistencia', 'Neto negativo rechazado; cero permitido; redondeo de 1,005 a 1,01; tasas del 2% y 2% con neto de 96 sobre bruto de 100.'],
], [125, 360])
p('<b>Registro de resultados.</b> evidencia/pruebas.txt conserva la ejecución de la suite y evidencia/nomina_ejemplo.csv contiene el desglose de los cuatro empleados ficticios utilizados en la demostración. Los valores de la tabla están expresados en pesos colombianos.')

page()
h('6. Metodología y control de versiones')
p('El proyecto se desarrolló mediante una metodología incremental. Las reglas del problema se organizaron como requisitos, se implementó el dominio y se incorporaron la salida por consola, la exportación y las pruebas. La documentación consolida el diseño y los resultados de cada incremento.')
table(['Etapa', 'Trabajo realizado y criterio de aceptación'], [
    ['Análisis', 'Identificación de las cuatro modalidades, beneficios, deducciones y validaciones. Definición explícita de criterios para las tasas y el período.'],
    ['Diseño e implementación', 'Construcción de entidades, política, servicio y comprobante. Cálculo de los cuatro ejemplos con separación de responsabilidades.'],
    ['Verificación', 'Contraste con valores manuales y ejecución de 25 pruebas. Aceptación de la implementación al obtener los resultados esperados y rechazar las entradas inválidas evaluadas.'],
    ['Documentación', 'Descripción de reglas y diseño; organización del informe, la presentación y las instrucciones de ejecución.'],
], [125, 360])
p('<b>Control de versiones.</b> Los cambios del código, las pruebas y la documentación se registraron en Git. El repositorio permite consultar el historial, identificar las modificaciones de cada versión y recuperar estados anteriores. Los materiales se organizan en carpetas de dominio, pruebas, documentos, presentación y evidencias.')
p('<b>Criterio de finalización funcional.</b> Se completaron las cuatro modalidades, los descuentos configurables, los beneficios, las validaciones, la exportación CSV y las pruebas unitarias. El informe describe estos componentes y sus resultados de forma consistente con la implementación.')
p('<b>Eficiencia.</b> Cada liquidación ejecuta una cantidad fija de operaciones del dominio. Con precisión numérica acotada, procesar n empleados requiere tiempo O(n). La exportación de la demostración reúne los n resultados en una lista y utiliza memoria O(n).')
p('<b>Alcance de la versión.</b> La solución implementada funciona por consola y utiliza empleados de ejemplo. La persistencia de datos, el prorrateo de períodos, la interfaz gráfica y la integración con otros sistemas quedan como posibilidades de ampliación.')

page()
h('7. Conclusiones')
p('La programación orientada a objetos permitió representar cuatro formas de remuneración mediante un contrato común. Las clases especializadas conservan sus reglas de cálculo, mientras el servicio coordina la liquidación sin depender de una modalidad concreta.')
p('La separación de responsabilidades y la política configurable facilitan el mantenimiento del sistema. El uso de Decimal y el redondeo por concepto establecen un tratamiento consistente de los importes. Las 25 pruebas aprobadas respaldan los casos de cálculo, las condiciones de frontera y las validaciones evaluadas.')
p('Como continuación del proyecto se propone incorporar captura interactiva y almacenamiento de empleados, reutilizando el dominio y ampliando las pruebas para cubrir esas funciones.')
h('8. Ejecución y repositorio')
p('La aplicación requiere Python 3.10 o superior. El sistema de nómina y sus pruebas funcionan con la biblioteca estándar. Desde la carpeta del proyecto se ejecutan los siguientes comandos:')
table(['Operación', 'Comando'], [
    ['Demostración', 'python -m nomina'],
    ['Exportación CSV', 'python -m nomina --csv evidencia/nomina_ejemplo.csv'],
    ['Pruebas unitarias', 'python -m unittest discover -s tests -v'],
], [120, 365])
p('<b>Repositorio:</b> <link href="https://github.com/tab-Jesus/IngDeSoftware">https://github.com/tab-Jesus/IngDeSoftware</link>. El código fuente, los registros de pruebas, el reporte de ejemplo y la presentación acompañan el informe en las carpetas del proyecto.')
h('Referencias')
references = [
    '[1] <i>Actividad Unidad Tres.</i> Guía de trabajo de Ingeniería de Software.',
    '[2] Python Software Foundation. <i>decimal: Decimal fixed-point and floating-point arithmetic.</i> <link href="https://docs.python.org/3/library/decimal.html">https://docs.python.org/3/library/decimal.html</link>',
    '[3] Python Software Foundation. <i>abc: Abstract Base Classes.</i> <link href="https://docs.python.org/3/library/abc.html">https://docs.python.org/3/library/abc.html</link>',
    '[4] Python Software Foundation. <i>dataclasses: Data Classes.</i> <link href="https://docs.python.org/3/library/dataclasses.html">https://docs.python.org/3/library/dataclasses.html</link>',
    '[5] Python Software Foundation. <i>unittest: Unit testing framework.</i> <link href="https://docs.python.org/3/library/unittest.html">https://docs.python.org/3/library/unittest.html</link>',
]
for reference in references:
    story.append(Paragraph(reference, styles['ReferenceAcademic']))

def footer(canvas, doc):
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(.4)
    canvas.line(55, 47, 540, 47)
    canvas.setFont('Times-Roman', 8)
    canvas.drawString(55, 33, 'Jesus Davod Campo | Ingeniería de Software | Unidad 3')
    canvas.drawRightString(540, 33, str(doc.page))

OUT.parent.mkdir(parents=True, exist_ok=True)
SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=55, leftMargin=55,
                  topMargin=48, bottomMargin=62,
                  title='Sistema de nómina - Unidad 3', author='Jesus Davod Campo').build(
                      story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
