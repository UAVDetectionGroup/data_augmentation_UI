import os
import cv2
import random
import numpy as np
from tqdm import tqdm
import xml.etree.ElementTree as ET
import xml.dom.minidom


def bosong_img(image, lam):#添加泊松噪声
    """
     :param imaege:cv2所读取的图片
     :param lam:泊松噪声出现的期望
     :return:处理后的泊松噪声图片
     """
    noise_type = np.random.poisson(lam=lam, size=(image.shape[0],image.shape[1] , 1)).astype(dtype='uint8')  # lam>=0 值越小，噪声频率就越少，size为图像尺寸
    noise_image = noise_type + image
    return noise_image

def bo_song_noise(image_path, xml_path, image_save_path, xml_save_path,
                 ):
    bs_lam = random.uniform(0, 0.5)  # 泊松噪声lam？

    img = cv2.imread(image_path)
    image_name = os.path.basename(image_path)
    img_h, img_w = img.shape[0], img.shape[1]
    img4 = bosong_img(img, bs_lam)
    bs_image_name = 'bs_' + image_name
    try:
        # ——————————————保存高斯噪声xml文件---------------------------#
        xmlfile1 = xml_path + r'/' + image_name[:-4] + '.xml'
        tree1 = ET.parse(xmlfile1)
        doc = xml.dom.minidom.Document()
        root = doc.createElement("annotation")
        doc.appendChild(root)

        for folds in tree1.findall("folder"):
            folder = doc.createElement("folder")
            folder.appendChild(doc.createTextNode(os.path.split(image_save_path)[-1]))
            root.appendChild(folder)
        for filenames in tree1.findall("filename"):
            filename = doc.createElement("filename")
            filename.appendChild(doc.createTextNode( bs_image_name ))
            root.appendChild(filename)
        for paths in tree1.findall("path"):
            path = doc.createElement("path")
            path.appendChild(doc.createTextNode(os.path.join(image_save_path,  bs_image_name )))
            root.appendChild(path)
        for sources in tree1.findall("source"):
            source = doc.createElement("source")
            database = doc.createElement("database")
            database.appendChild(doc.createTextNode(str("Unknow")))
            source.appendChild(database)
            root.appendChild(source)
        for sizes in tree1.findall("size"):
            size = doc.createElement("size")
            width = doc.createElement("width")
            height = doc.createElement("height")
            depth = doc.createElement("depth")
            width.appendChild(doc.createTextNode(str(img_w)))
            height.appendChild(doc.createTextNode(str(img_h)))
            depth.appendChild(doc.createTextNode(str(3)))
            size.appendChild(width)
            size.appendChild(height)
            size.appendChild(depth)
            root.appendChild(size)

        nodeframe = doc.createElement("frame")
        nodeframe.appendChild(doc.createTextNode(image_name[:-4] + '_3'))

        objects = []

        for obj in tree1.findall("object"):
            obj_struct = {}
            obj_struct["name"] = obj.find("name").text
            obj_struct["pose"] = obj.find("pose").text
            obj_struct["truncated"] = obj.find("truncated").text
            obj_struct["difficult"] = obj.find("difficult").text
            bbox = obj.find("bndbox")
            obj_struct["bbox"] = [int(bbox.find("xmin").text),
                                  int(bbox.find("ymin").text),
                                  int(bbox.find("xmax").text),
                                  int(bbox.find("ymax").text)]
            objects.append(obj_struct)

        for obj in objects:
            nodeobject = doc.createElement("object")
            nodename = doc.createElement("name")
            nodepose = doc.createElement("pose")
            nodetruncated = doc.createElement("truncated")
            nodeDifficult = doc.createElement("Difficult")
            nodebndbox = doc.createElement("bndbox")
            nodexmin = doc.createElement("xmin")
            nodeymin = doc.createElement("ymin")
            nodexmax = doc.createElement("xmax")
            nodeymax = doc.createElement("ymax")
            nodename.appendChild(doc.createTextNode(obj["name"]))
            nodepose.appendChild(doc.createTextNode(obj["pose"]))
            nodetruncated.appendChild(doc.createTextNode(obj["truncated"]))
            nodeDifficult.appendChild(doc.createTextNode(obj["difficult"]))
            nodexmin.appendChild(doc.createTextNode(str(obj["bbox"][0])))
            nodeymin.appendChild(doc.createTextNode(str(obj["bbox"][1])))
            nodexmax.appendChild(doc.createTextNode(str(obj["bbox"][2])))
            nodeymax.appendChild(doc.createTextNode(str(obj["bbox"][3])))

            nodebndbox.appendChild(nodexmin)
            nodebndbox.appendChild(nodeymin)
            nodebndbox.appendChild(nodexmax)
            nodebndbox.appendChild(nodeymax)

            nodeobject.appendChild(nodename)
            nodeobject.appendChild(nodepose)
            nodeobject.appendChild(nodetruncated)
            nodeobject.appendChild(nodeDifficult)
            nodeobject.appendChild(nodebndbox)

            root.appendChild(nodeobject)
        fp = open(xml_save_path + '/' + "bs_" + image_name[:-4] + ".xml", "w")
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
        fp.close()

        if not os.path.exists(image_save_path):
            os.makedirs(image_save_path)
        cv2.imwrite(os.path.join(image_save_path, bs_image_name), img4)

        if not os.path.exists(xml_save_path):
            os.makedirs(xml_save_path)
        return os.path.join(image_save_path, bs_image_name)
    except:
        pass
