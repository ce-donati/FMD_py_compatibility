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
        save_img = False

        img_path = IMAGE_DIR + "/" + data["FileName"]
        for i in range(data["NumOfAnno"]):
            old_lbl = data["Annotations"][i]["classname"]
            if old_lbl == "face_no_mask":
                save_img = True
                break;
            elif old_lbl == "face_with_mask":
                save_img = True
                break;
            elif old_lbl == "face_with_mask_incorrect":
                save_img = True
                break;
            else:
                continue

        json_file.close()

        if save_img==False:
            remove(img_path)
            remove(file)