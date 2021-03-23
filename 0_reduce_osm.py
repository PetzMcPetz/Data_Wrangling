# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 23:05:21 2021

@author: Petzi
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

k = 10 # Parameter: take every k-th top level element

inname = "Berlin_OSM_v2"
outname = inname+"_k"+str(k)

infile = inname+".osm"  # Replace this with your osm file
outfile = outname+".osm"

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(outfile, 'w', encoding="utf8") as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

# with open(SAMPLE_FILE, 'wb') as output:
#     output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
#     output.write(b'<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(infile)):
        if i % k == 0:
            
            #Creates binary string
            #xmlstr = ET.tostring(element, encoding='utf8', method='xml')
            
            #Creates string
            xmlstr = ET.tostring(element, encoding='unicode', method='xml')
            output.write(xmlstr)

    output.write('</osm>')
    #output.write(b'</osm>')