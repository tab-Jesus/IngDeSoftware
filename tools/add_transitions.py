"""Agrega transiciones de fundido a las diapositivas sin alterar el contenido."""
import re
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

source = Path(sys.argv[1])
with ZipFile(source) as archive:
    items = [(info, archive.read(info.filename)) for info in archive.infolist()]
ns = 'http://schemas.openxmlformats.org/presentationml/2006/main'
with ZipFile(source, 'w', ZIP_DEFLATED) as archive:
    for info, data in items:
        if re.fullmatch(r'ppt/slides/slide\d+\.xml', info.filename):
            tree = etree.fromstring(data)
            transition = etree.Element(f'{{{ns}}}transition', spd='med', advClick='1')
            etree.SubElement(transition, f'{{{ns}}}fade')
            insertion = next((i for i, e in enumerate(tree) if etree.QName(e).localname in ('timing', 'extLst')), len(tree))
            tree.insert(insertion, transition)
            data = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
        archive.writestr(info, data)
