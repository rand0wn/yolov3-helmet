import xml.etree.ElementTree as et

xtree = et.parse("annotations.xml")
xroot = xtree.getroot()

with open('test.txt') as f:
    lines = f.read().splitlines()

test_id_list = [i.split('/')[-1].split('.')[0] for i in lines]

for node in xroot.iter('image'):

    rows = []
    id_ = node.attrib.get("id")
    
    if id_ in test_id_list:
	    name = node.attrib.get("name")
	    width = node.attrib.get("width")
	    height = node.attrib.get("height")

	    root1 = et.Element('root')
	    root1 = node

	    head_list = list()
	    for supply in root1.iter('box'):
	        label = supply.attrib.get("label")
	        if label == "head":
	            occluded = supply.attrib.get("occluded")
	            xtl = float(supply.attrib.get("xtl"))
	            ytl = float(supply.attrib.get("ytl"))
	            xbr = float(supply.attrib.get("xbr"))
	            ybr = float(supply.attrib.get("ybr"))
	            attr_dict = {}

	            root2 = et.Element('root')
	            root2 = supply
	            for at in root2.iter('attribute'):
	                attr_dict[str(at.attrib.get("name"))] = at.text

	            if attr_dict['mask'] == 'yes' and attr_dict['has_safety_helmet'] == 'yes':
	                rows.append((1, xtl, ytl, xbr, ybr))
	            elif attr_dict['mask'] == 'yes':
	                rows.append((2, xtl, ytl, xbr, ybr))
	            elif attr_dict['has_safety_helmet'] == 'yes':
	                rows.append((3, xtl, ytl, xbr, ybr))
	            else:
	                rows.append((0, xtl, ytl, xbr, ybr))
	            
	    with open("./input/ground-truth/"+str(id_)+".txt", "w") as text_file:
	    	for i in rows:
	            j = str(i).replace(',', '')
	            text_file.write(j[1:len(j)-1]+'\n')