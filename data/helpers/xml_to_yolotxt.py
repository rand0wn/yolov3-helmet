import pandas as pd
import xml.etree.ElementTree as et
import shutil 


xtree = et.parse("annotations.xml")
xroot = xtree.getroot()

df_cols = ["id", "name", "width", "height", "head_list"]

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return x,y,w,h

for node in xroot.iter('image'):
    rows = []
    id_ = node.attrib.get("id")
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
            xtl = supply.attrib.get("xtl")
            ytl = supply.attrib.get("ytl")
            xbr = supply.attrib.get("xbr")
            ybr = supply.attrib.get("ybr")
            #print(convert([float(width), float(height)], [float(xtl), float(xbr), float(ytl), float(ybr)]))         
            
            x, y, w, h = convert([float(width), float(height)], [float(xtl), float(xbr), float(ytl), float(ybr)])

            attr_dict = {}

            root2 = et.Element('root')
            root2 = supply
            for at in root2.iter('attribute'):
                attr_dict[str(at.attrib.get("name"))] = at.text

            if attr_dict['mask'] == 'yes' and attr_dict['has_safety_helmet'] == 'yes':
                rows.append((1, x, y, w, h))
            elif attr_dict['mask'] == 'yes':
                rows.append((2, x, y, w, h))
            elif attr_dict['has_safety_helmet'] == 'yes':
                rows.append((3, x, y, w, h))
            else:
                rows.append((0, x, y, w, h))

        #print(attr_dict)
    #print(rows)
    #print(id_)
    
    with open("./labels/"+str(id_)+".txt", "w") as text_file:
        for i in rows:
            j = str(i).replace(',', '')
            text_file.write(j[1:len(j)-1]+'\n')

    shutil.copyfile("./images_total/"+id_+".jpg", "./images/"+id_+".jpg")
#print(rows)