import cv2
import os
import random
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom



def mix_up(image_path, xml_path, save_image,save_xml):
    img = cv2.imread(image_path)
    img_h, img_w = img.shape[0], img.shape[1]

    img_names = os.listdir(xml_path)
    img_num = len(img_names)

    image_name='mixup_'+ os.path.split(image_path)[-1]
    i = random.randint(0, img_num - 1)

    add_path = os.path.split(image_path)[0]+ r'/'+img_names[i][:-4]+os.path.split(image_path)[-1][-4:]
    addimg = cv2.imread(add_path)

    add_h, add_w = addimg.shape[0], addimg.shape[1]
    if add_h != img_h or add_w != img_w:
        addimg = cv2.resize(addimg, (img_w, img_h), interpolation=cv2.INTER_LINEAR)
    scale_h, scale_w = img_h / add_h, img_w / add_w

    lam = np.random.beta(1.5, 1.5)

    mixed_img = lam * img + (1 - lam) * addimg




    try:
        if os.path.split(image_path)[-1] != img_names[i]:
            xmlfile1 = xml_path +'/' +os.path.split(image_path)[-1][:-4] + '.xml'
            xmlfile2 = xml_path +"/"+os.path.split(add_path)[-1][:-4] + '.xml'

            tree1 = ET.parse(xmlfile1)
            tree2 = ET.parse(xmlfile2)

            doc = xml.dom.minidom.Document()
            root = doc.createElement("annotation")
            doc.appendChild(root)



            for folds in tree1.findall("folder"):
                folder = doc.createElement("folder")
                folder.appendChild(doc.createTextNode(os.path.split(save_image)[-1]))
                root.appendChild(folder)
            for filenames in tree1.findall("filename"):
                filename = doc.createElement("filename")
                filename.appendChild(doc.createTextNode(image_name ))
                root.appendChild(filename)
            for paths in tree1.findall("path"):
                path = doc.createElement("path")
                path.appendChild(doc.createTextNode(os.path.join(save_image,  image_name )))
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

            for obj in tree2.findall("object"):
                obj_struct = {}
                obj_struct["name"] = obj.find("name").text
                obj_struct["pose"] = obj.find("pose").text
                obj_struct["truncated"] = obj.find("truncated").text
                obj_struct["difficult"] = obj.find("difficult").text          # 有的版本的labelImg改参数为小写difficult
                bbox = obj.find("bndbox")
                obj_struct["bbox"] = [int(int(bbox.find("xmin").text) * scale_w),
                                      int(int(bbox.find("ymin").text) * scale_h),
                                      int(int(bbox.find("xmax").text) * scale_w),
                                      int(int(bbox.find("ymax").text) * scale_h)]
                objects.append(obj_struct)

            for obj in objects:
                nodeobject = doc.createElement("object")
                nodename = doc.createElement("name")
                nodepose = doc.createElement("pose")
                nodetruncated = doc.createElement("truncated")
                nodedifficult = doc.createElement("difficult")
                nodebndbox = doc.createElement("bndbox")
                nodexmin = doc.createElement("xmin")
                nodeymin = doc.createElement("ymin")
                nodexmax = doc.createElement("xmax")
                nodeymax = doc.createElement("ymax")
                nodename.appendChild(doc.createTextNode(obj["name"]))
                nodepose.appendChild(doc.createTextNode(obj["pose"]))
                nodepose.appendChild(doc.createTextNode(obj["truncated"]))
                nodedifficult.appendChild(doc.createTextNode(obj["difficult"]))
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
                nodeobject.appendChild(nodedifficult)
                nodeobject.appendChild(nodebndbox)

                root.appendChild(nodeobject)

            fp = open(save_xml +'/'+image_name[:-4] + ".xml", "w")
            doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
            fp.close()
            cv2.imwrite(os.path.join(save_image, image_name), mixed_img)
            return os.path.join(save_image, image_name)
    except:
        pass


#
# img_path = r"D:\xiangmu\ui\test\image\angle1_1.jpg"          # 原始图片文件夹路径
# save_path =  r"D:\xiangmu\ui\test\image_save"    # mixup的图片文件夹路径
# xml_path = r"D:\xiangmu\ui\test\xml"           # 原始图片对应的标注文件xml文件夹的路径
# save_xml = r"D:\xiangmu\ui\test\xml_save_patj"       # mixup的图片对应的标注文件xml的文件夹路径
# if __name__ == '__main__':
#     mix_up(image_path=img_path,xml_path=xml_path,save_image=save_path,save_xml=save_xml)