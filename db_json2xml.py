import json as JS
import xml.etree.ElementTree as ET
from os import listdir, remove, rename
from PIL import Image

IMAGE_DIR = "Database_2/Medical mask/Medical mask/Medical Mask/images"
ANNOT_DIR = "Database_2/Medical mask/Medical mask/Medical Mask/annotations"

index = 853
for annot_name in listdir(ANNOT_DIR):
    file = ANNOT_DIR + "/" + annot_name
    with open(file, "r") as json_file:
        data = JS.load(json_file)

        #root
        root = ET.Element("annotation")
        #folder
        folder = ET.SubElement(root, "folder")
        folder.text = "images"
        #filename
        filename = ET.SubElement(root, "filename")
        image_name = str(data["FileName"])
        j = str(data["FileName"]).find(".")
        ext = image_name[-j:]
        filename.text = str(index) + ext

        im = Image.open(IMAGE_DIR+"/"+data["FileName"])
        wdt, hgt = im.size
        im.close()

        image_name = IMAGE_DIR + "/" + str(index) + ext
        rename(IMAGE_DIR + "/" + data["FileName"], image_name)

        #size
        size = ET.SubElement(root, "size")
            #width
        width = ET.SubElement(size, "width")
        width.text = str(wdt)
            #height
        height = ET.SubElement(size, "height")
        height.text = str(hgt)
            #depth
        depth = ET.SubElement(size, "depth")
        depth.text = str(3)

        for i in range(data["NumOfAnno"]):
            old_lbl = data["Annotations"][i]["classname"]
            if old_lbl == "face_no_mask":
                lbl = "without_mask"
            elif old_lbl == "face_with_mask":
                lbl = "with_mask"
            elif old_lbl == "face_with_mask_incorrect":
                lbl = "mask_weared_incorrect"
            else:
                continue

            # object
            object = ET.SubElement(root, "object")
                # name
            name = ET.SubElement(object, "name")

            name.text = lbl
                #bnbbox
            bnbbox = ET.SubElement(object, "bndbox")
                    #xmin
            xmin = ET.SubElement(bnbbox, "xmin")
            xmin.text = str(min(data["Annotations"][i]["BoundingBox"][0], data["Annotations"][i]["BoundingBox"][2]))
                    #ymin
            ymin = ET.SubElement(bnbbox, "ymin")
            ymin.text = str(min(data["Annotations"][i]["BoundingBox"][1], data["Annotations"][i]["BoundingBox"][3]))
                    #xmax
            xmax = ET.SubElement(bnbbox, "xmax")
            xmax.text = str(max(data["Annotations"][i]["BoundingBox"][0], data["Annotations"][i]["BoundingBox"][2]))
                    #ymax
            ymax = ET.SubElement(bnbbox, "ymax")
            ymax.text = str(max(data["Annotations"][i]["BoundingBox"][1], data["Annotations"][i]["BoundingBox"][3]))
            # gli indici del database sono sfasati, nella form x1,y1,x2,y2, abbiamo dovuto modificare tutto
        tree = ET.ElementTree(root)
        json_file.close()

        tree.write("Database_2/Medical mask/Medical mask/Medical Mask/annot_xml/" + str(index) + ".xml")
    index = index+1