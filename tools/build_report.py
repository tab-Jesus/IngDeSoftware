"""Construye el informe académico con diseño reproducible."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'documentos/Informe_Unidad_3_Jesus_Davod_Campo.pdf'
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text', fontName='Helvetica', fontSize=10.5, leading=15, spaceAfter=10, textColor=colors.HexColor('#243449')))
styles.add(ParagraphStyle(name='TitleBig', fontName='Helvetica-Bold', fontSize=31, leading=37, textColor=colors.HexColor('#122b49'), spaceAfter=22))
styles.add(ParagraphStyle(name='SectionTitle', fontName='Helvetica-Bold', fontSize=21, leading=27, textColor=colors.HexColor('#122b49'), spaceAfter=18))
styles.add(ParagraphStyle(name='SmallText', fontName='Helvetica', fontSize=8.5, leading=12, spaceAfter=7))
story=[]

def p(text): story.append(Paragraph(text, styles['Text']))
def h(text): story.append(Paragraph(text, styles['SectionTitle']))
def page(): story.append(PageBreak())
def table(headers, rows, widths):
    data=[[Paragraph(str(v), styles['SmallText']) for v in row] for row in [headers]+rows]
    t=Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dbe9ef')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6f9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),1,colors.HexColor('#178c95'))]))
    story.append(t); story.append(Spacer(1,14))

story.append(Spacer(1,58))
p('UNIVERSIDAD DE CARTAGENA<br/>Programa de Ingeniería de Software')
story.append(Spacer(1,35))
story.append(Paragraph('Sistema de nómina<br/>orientado a objetos',styles['TitleBig']))
p('ACTIVIDAD UNIDAD TRES · INGENIERÍA DE SOFTWARE')
story.append(Spacer(1,38))
table(['Autor','Entrega'],[['Jesus Davod Campo','Implementación, pruebas y documentación']], [230,255])
p('Cartagena de Indias<br/>1 de noviembre de 2026')
story.append(Spacer(1,35))
p('<b>Alcance:</b> solución académica individual preparada a partir del enunciado proporcionado. La guía solicita entrega CIPA; no se han inventado integrantes. El video y la publicación remota requieren completar los pasos indicados al final.')
page()
h('1. Propósito y requisitos')
p('El sistema liquida ingresos, bonos, deducciones y beneficios para cuatro modalidades de empleados. Su diseño separa reglas de negocio, cálculo de descuentos y presentación, de modo que el comportamiento puede extenderse y verificarse sin depender de una interfaz gráfica.')
table(['Requisito de la guía','Implementación y aceptación'],[
('Asalariado','Salario mensual fijo. Bono del 10% únicamente con antigüedad mayor a cinco años.'),
('Por horas','Hasta 40 horas a tarifa normal; exceso a 1.5 veces. Sin bono monetario.'),
('Por comisión','Base más ventas por porcentaje. Bono del 3% de todas las ventas si superan $20.000.000.'),
('Temporal','Salario fijo; fechas inicial y final válidas. Sin bonos ni alimentación adicional.'),
('Descuentos y ARL','Política inyectada con tasas configurables y desglose por concepto.'),
('Beneficios','Alimentación de $1.000.000 para permanentes. Fondo del 2% para empleados por horas elegibles que acepten.'),
('Validaciones','Rechazo de valores negativos o no finitos, contratos invertidos, tasas inválidas y netos negativos.'),
('Ingeniería','POO, SOLID, código limpio, refactorización, pruebas y metodología documentados.')],[125,360])
p('<b>Entradas:</b> identificación, nombre, antigüedad y parámetros de la modalidad. <b>Salidas:</b> pago ordinario, bono, bruto, seguro, pensión, ahorro, neto, alimentación, ARL y costo modelado para la empresa.')
page()
h('2. Supuestos y fórmulas')
p('La guía contiene detalles no definidos. Para que los cálculos sean reproducibles se adoptan las siguientes decisiones académicas, ajustables si el docente especifica otra interpretación:')
table(['Concepto','Decisión explícita'],[
('Seguro y pensión','Se interpreta 4% para seguro y 4% para pensión. Si el 4% fuera combinado, las tasas se pueden modificar en DeductionPolicy.'),
('ARL','Se registra como costo empresarial separado. La tasa de 0.522% es ilustrativa y configurable, pues la guía no fija tarifa ni pagador.'),
('Alimentación','Beneficio empresarial separado del neto y del bruto usado como base de deducciones en este modelo.'),
('Fondo de ahorro','Retención del 2% del bruto, depositada al fondo; requiere más de un año y aceptación. No se presume aporte adicional de la empresa.'),
('Períodos','Las horas se comparan con 40 en el período ingresado. No se inventa conversión semanal a mensual. El temporal exige fecha dentro del contrato, sin prorrateo.'),
('Precisión','Decimal y redondeo HALF_UP a dos decimales por concepto; bruto = ordinario redondeado + bono redondeado.')],[115,370])
p('<b>Fórmulas comunes</b><br/>Seguro = bruto × tasa de seguro.<br/>Pensión = bruto × tasa de pensión.<br/>Ahorro = bruto × 2%, solo si corresponde.<br/>Neto = bruto - seguro - pensión - ahorro.<br/>Costo modelado de empresa = bruto + alimentación + ARL.')
p('Estos supuestos responden a un ejercicio de programación. No constituyen una liquidación laboral certificada ni un cálculo completo de obligaciones de una empresa.')
page()
h('3. Diseño y programación orientada a objetos')
p('<b>Abstracción:</b> Employee es una clase abstracta que define earnings y el contrato común. <b>Herencia:</b> Salaried, Hourly, Commission y Temporary especializan sus reglas. <b>Polimorfismo:</b> PayrollService solicita las mismas operaciones a cualquier empleado. <b>Encapsulación:</b> entidades inmutables y validación al construirlas mantienen estados válidos.')
table(['Capa / clase','Responsabilidad'],[
('Employee','Contrato: earnings(), validate_period(), food y saving_rate.'),
('Salaried / Hourly / Commission / Temporary','Reglas específicas de ingresos, beneficios y elegibilidad.'),
('DeductionPolicy','Tasas, deducciones y aporte ARL de la empresa.'),
('PayrollService','Valida período, solicita ingresos, aplica política y verifica neto.'),
('Payslip','Resultado inmutable del cálculo.'),
('__main__.py','Ejemplos ejecutables, presentación por consola y exportación CSV.')],[190,295])
p('<b>Relaciones del modelo</b><br/>Employee &lt;-- Salaried, Hourly, Commission, Temporary<br/>PayrollService --&gt; Employee<br/>PayrollService --&gt; DeductionPolicy<br/>PayrollService --&gt; Payslip<br/>Consola / CSV --&gt; PayrollService')
p('<b>Flujo:</b> crear empleado válido → validar fecha → calcular ordinario y bono → obtener bruto → aplicar deducciones y ahorro → rechazar neto negativo → devolver comprobante → presentar o exportar.')
p('Para incorporar otra modalidad se implementa Employee y se reutiliza el servicio. La interfaz no contiene reglas de cálculo; las pruebas pueden ejecutarse sin exportar archivos.')
page()
h('4. SOLID, limpieza y refactorización')
table(['Principio','Aplicación concreta'],[
('S · Responsabilidad única','Entidades para ingresos, política para tasas, servicio para orquestación y consola para salida.'),
('O · Abierto/cerrado','No hay una cadena de condicionales por tipo en el servicio. Cada variante implementa su cálculo y validación de período.'),
('L · Sustitución','Cada variante satisface el mismo contrato de ingresos y beneficios. Se permiten errores de elegibilidad documentados para períodos inválidos.'),
('I · Segregación','El contrato del dominio es pequeño y no obliga a los empleados a imprimir, exportar CSV ni almacenar datos.'),
('D · Inversión de dependencias','El servicio recibe la política en el constructor y opera con el contrato Employee. Otra política compatible puede sustituirse sin cambiar el cálculo de empleados.')],[130,355])
p('<b>Código limpio.</b> Nombres explícitos, funciones cortas, comentarios que explican decisiones, constantes decimales y validaciones cercanas a los datos. Las dataclasses reducen código repetido y expresan claramente los atributos del modelo.')
p('<b>Refactorización aplicada.</b> La comprobación del contrato temporal se trasladó desde una consulta del tipo concreto en el servicio hacia validate_period en las entidades. Con ello se eliminó la dependencia del servicio respecto a Temporary. También se concentraron las tasas en DeductionPolicy y el redondeo en money().')
p('<b>Corrección durante la verificación.</b> Una prueba usaba un costo empresarial esperado incorrecto para un salario de $100. El valor correcto es $1.000.100,52 por incluir alimentación de $1.000.000 y ARL de $0,52. Se corrigió el oráculo del test, conservando la regla del enunciado.')
page()
h('5. Resultados y pruebas unitarias')
p('Se ejecutaron 25 pruebas con unittest. Los casos verifican resultados calculados manualmente, límites estrictos, entradas inválidas y configuración alternativa. El registro reproducible está en evidencia/pruebas.txt.')
table(['Ejemplo ficticio','Bruto','Neto','Costo empresa'],[
('Asalariado: $3 millones, 6 años','$3.300.000','$3.036.000','$4.317.226'),
('Horas: 45 × $20.000, ahorro','$950.000','$855.000','$954.959'),
('Comisión: base $2 millones, ventas $25 millones, 5%','$4.000.000','$3.680.000','$5.020.880'),
('Temporal: salario $1.800.000','$1.800.000','$1.656.000','$1.809.396')],[180,100,100,105])
p('<b>Verificación manual del empleado por horas:</b> 40 × $20.000 + 5 × $30.000 = $950.000. Seguro: $38.000. Pensión: $38.000. Ahorro: $19.000. Neto: $855.000. ARL empresarial: $4.959. Sin alimentación ni bono.')
table(['Familia de pruebas','Comportamiento esperado'],[
('Fronteras','5 años: sin bono; más de 5: con bono. 40 horas: sin extras. $20 millones: sin bono adicional. Un año: sin ahorro.'),
('Validaciones','Horas, ventas y salarios negativos o no finitos se rechazan; nombres vacíos, tasas fuera de rango y antigüedad negativa también.'),
('Contrato y consistencia','Fechas inclusivas válidas; período externo e inversión de fechas rechazados. Neto negativo rechazado; cero permitido.'),
('Dinero y política','Redondeo 1.005 a 1.01; alimentación separada; tasas alternativas 2% + 2% producen neto 96 sobre bruto 100.')],[130,355])
p('<b>Resultado observado:</b> 25 pruebas aprobadas, sin fallos. No se afirma cobertura porcentual ni pruebas de integración bancaria. Cada cálculo individual usa un número fijo de operaciones: tiempo O(1); procesar n empleados requiere O(n) y la exportación actual conserva O(n) resultados en memoria.')
page()
h('6. Metodología y trazabilidad')
p('Se aplicó desarrollo incremental inspirado en Scrum, adaptado a una elaboración individual. No se atribuyen reuniones, roles grupales ni participación CIPA que no se hayan comprobado.')
table(['Incremento','Entregable y criterio de aceptación'],[
('1 · Análisis','Backlog: cuatro modalidades, deducciones, beneficios y validaciones. Aceptación: cada regla tiene una decisión explícita.'),
('2 · Construcción','Modelo POO, política, servicio y CLI. Aceptación: los cuatro ejemplos devuelven desglose coherente y CSV.'),
('3 · Verificación','Pruebas de cálculo, fronteras y errores. Aceptación: 25 pruebas pasan con oráculos numéricos independientes.'),
('4 · Entrega','Informe, README, guion y paquete. Aceptación: instrucciones reproducibles y pendientes externos claramente identificados.')],[120,365])
p('<b>Control de versiones.</b> El paquete incluye repositorio Git local. Los commits registran la incorporación del código, las pruebas y la documentación en esta sesión; no simulan un historial de semanas ni autoría de terceros. Para inspeccionarlos: git log --oneline.')
p('<b>Definición de terminado técnico:</b> cuatro tipos implementados, cálculos con precisión decimal, validaciones activas, pruebas aprobadas, exportación funcional y documentación verificable. La entrega académica completa añade los enlaces reales de GitHub y YouTube y la revisión de modalidad CIPA.')
p('<b>Limitaciones:</b> demostración por consola con datos ficticios; sin persistencia, interfaz gráfica, prorrateo, obligaciones tributarias ni integración bancaria. Los costos reflejan únicamente los conceptos definidos para el ejercicio.')
page()
h('7. Ejecución, exposición y entrega')
p('<b>Requisitos:</b> Python 3.10 o superior. No se requieren paquetes externos para ejecutar la nómina y sus pruebas. Desde la carpeta del proyecto:')
table(['Paso','Comando'],[
('Demostración','python -m nomina'),
('Exportar CSV','python -m nomina --csv evidencia/nomina_ejemplo.csv'),
('Pruebas','python -m unittest discover -s tests -v'),
('Historial','git log --oneline')],[115,370])
p('<b>Exposición:</b> el guion adjunto propone una presentación de 6 a 8 minutos: objetivo, reglas y supuestos, diseño POO/SOLID, ejecución, pruebas, metodología y conclusiones. La grabación debe mostrar resultados reales y participación real de los integrantes que correspondan.')
p('<b>Pendientes para entregar en SIMA:</b><br/>1. Confirmar la entrega individual o identificar integrantes reales del CIPA.<br/>2. Crear y publicar el repositorio en la cuenta de GitHub del estudiante.<br/>3. Grabar y publicar la exposición en YouTube, comprobando acceso al enlace.<br/>4. Entregar el informe y las dos URL reales según indique la plataforma.')
p('El acceso al curso SIMA no pudo verificarse con la herramienta disponible. Se trabajó con las dos páginas completas del PDF local suministrado. No se ha enviado ni publicado contenido en la plataforma académica.')
h('Fuentes y material de consulta')
p('Fuente de requisitos: <i>ACTIVIDAD UNIDAD 3.pdf</i>, documento proporcionado por el estudiante, dos páginas, sin autor ni fecha indicados. Reglas de negocio y requisitos de entrega.')
p('Documentación técnica de consulta: Python Software Foundation, <i>decimal</i>, <i>unittest</i>, <i>abc</i> y <i>dataclasses</i>. Disponible en https://docs.python.org/3/library/ . Los resultados presentados provienen de la ejecución local, no de estos materiales de consulta.')

def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor('#178c95')); canvas.line(55,47,540,47)
    canvas.setFont('Helvetica',8); canvas.setFillColor(colors.HexColor('#53647a'))
    canvas.drawString(55,33,'Jesus Davod Campo | Ingeniería de Software | Unidad 3')
    canvas.drawRightString(540,33,str(doc.page))

OUT.parent.mkdir(parents=True, exist_ok=True)
SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=55, leftMargin=55, topMargin=48, bottomMargin=62, title='Sistema de nómina - Unidad 3', author='Jesus Davod Campo').build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
