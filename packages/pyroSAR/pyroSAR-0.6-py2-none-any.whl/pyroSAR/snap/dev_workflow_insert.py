from xml.dom import minidom
import xml.etree.ElementTree as ET

from pyroSAR.snap.auxil import parse_node, insert_node, parse_recipe

workflow = parse_recipe('geocode')

insert_node(workflow, parse_node('Subset'), before='Read')
insert_node(workflow, parse_node('Subset'), after='Write')

rough_string = ET.tostring(workflow, 'utf-8')
reparsed = minidom.parseString(rough_string)
print(reparsed.toprettyxml(indent='\t', newl=''))
