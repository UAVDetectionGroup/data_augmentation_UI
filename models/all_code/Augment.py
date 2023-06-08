from models.all_code.jiaoyan import  NoiseAugmentation
from models.all_code.cutmix import CutmixAugmentation
from models.all_code.small_object import Samll_object_Augmentation
from models.all_code.Cycle.predict import cycleGANAugmentaion



def Augment(img_path,xml_path,img_save_path,xml_save_xml):
    #-----------------------------------#
    #   Part1路径修改：
    #       输入图片、XML路径应为数据集路径
    #       输出图片、XML路径应为新路径
    #       未防止混淆，建议提前备份原路径
    #-----------------------------------#
    # img_path = r"D:\yolo v7 data processing\mixupkuocong\gui tiao zai picture"  # 原始图片文件夹路径
    # xml_path = r"D:\yolo v7 data processing\mixupkuocong\guitiaozai_xml" # 原始图片对应的标注文件xml文件夹的路径
    # img_save_path = r"D:\yolo v7 data processing\mixupkuocong\gs_sa" # 增强的图片文件夹路径
    # xml_save_xml = r"D:\yolo v7 data processing\mixupkuocong\gs_xml"  # 增强的图片对应的标注文件xml的文件夹路径
    category = ['gtz', "others", "group", "connection"]  # 一定要输对,不对会报错
    # # -----------------------------------#
    # #   Part2参数设定
    # # -----------------------------------#
    gs_mean = 0  # 高斯噪声均值
    gs_var = 0.01  # 高斯噪声var？
    # # -----------------------------------#
    # #   噪声增强方法调用
    # #       （即插即用）
    # # -----------------------------------#
    NoiseAugmentation(img_path, xml_path, img_save_path, xml_save_xml, gs_mean, gs_var)
    #
    # # -----------------------------------#
    # #   cutmix增强方法调用
    # #       （即插即用）
    # # -----------------------------------#
    CutmixAugmentation(img_path,xml_path,img_save_path,xml_save_xml,category)


    # -----------------------------------#
    #   小目标增强方法调用
    #       （即插即用）
    # part1参数设定
    # -----------------------------------#
    Low_SOA_THRESH = 256*256
    SOA_THRESH = 0 * 0#复制最大尺寸(如果尺寸小于64*64就不复制)
    SOA_PROB = 1#百分之百复制
    SOA_COPY_TIMES = 3#复制的个数。(如果小于64*64就会复制3个)
    SOA_EPOCHS = 30#轮次(没用)
    objects = ['gtz', "others", "connection"]
    # -----------------------------------#
    #  小目标增强方法调用
    #       （即插即用）
    # -----------------------------------#
    Samll_object_Augmentation(img_path, xml_path, img_save_path,xml_save_xml, SOA_THRESH, SOA_PROB,
                              SOA_COPY_TIMES, SOA_EPOCHS,Low_SOA_THRESH,category,objects)
    # -----------------------------------#
    # cyclegan增强方法调用
    #       （即插即用）
    # -----------------------------------#
    cycleGANAugmentaion(img_path, xml_path, img_save_path, xml_save_xml)