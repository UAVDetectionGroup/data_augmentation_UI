from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QAction
from main_win.win import Ui_mainWindow
from PyQt5.QtCore import Qt, QPoint, QTimer, QThread, pyqtSignal
from PyQt5 import QtWidgets,QtGui
import sys
from models.noise.jiaoyan import jiao_yan
from models.noise.gao_si import gao_si_noise
from models.noise.bo_song import bo_song_noise
from models.mixup.mix_up import mix_up
from models.small_object.small_object import Samll_object_Augmentation
from models.cutmix.cutmix import  CutmixAugmentation
from models.cyclegan.predict import cycleGANAugmentaion
from models.all_code.Augment import Augment
import os

class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.m_flag = False
        #打开文件设置
        self.image_path=None
        self.image_save_path=None
        self.xml_path=None
        self.xml_save_path= None

        # # # 样式1：窗口可以拉伸
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint |
        #                     Qt.WindowSystemMenuHint )
        self.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint |
                            Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(1500,1000)


        # 样式2：窗口不能拉伸
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint
        #                     | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        # self.setFixedSize(1500, 1000)
        # self.setWindowOpacity(0.85)  # 窗口的透明度

        self.minButton.clicked.connect(self.showMinimized)
        self.maxButton.clicked.connect(self.max_or_restore)
        # show minButton window
        self.minButton.animateClick(10)
        self.closeButton.clicked.connect(self.close)

        self.qtimer = QTimer(self)              #首先初始化一个定时器，把定时器的timeout信号与showTime()槽函数连接起来
        self.qtimer.setSingleShot(True)         #实现单次定时器
        self.qtimer.timeout.connect(lambda: self.statistic_label.clear())   #当定时器超时时发射此信号

        #打开图片文件夹
        self.fileButton.clicked.connect(self.image_dir)

        #打开xml文件夹
        self.pushButton.clicked.connect(self.xml_dir)
        #保存图片路径
        self.fileButton_2.clicked.connect(self.image_save)
        #保存xml文件路径
        self.pushButton_6.clicked.connect(self.xml_save)





        # 噪声增强模型
        self.comboBox.clear()   #   删除 ComboBox 中的列表中的所有条目。
        self.pt_list = ['无噪声',"椒盐噪声","高斯噪声","泊松噪声"]
        # self.pt_list.sort(key=lambda x: os.path.getsize('./pt/'+x))
        self.comboBox.setCurrentIndex(0)
        self.comboBox.clear()
        self.comboBox.addItems(self.pt_list)
        self.comboBox.currentIndexChanged.connect(self.nosie_enduance)


        # mixup增强
        self.pushButton_2.clicked.connect(self.mix_up)


        #cutmix数据增强
        self.pushButton_4.clicked.connect(self.cut_mix)

        #小目标增强
        self.lineEdit.text()
        self.pushButton_3.clicked.connect(self.small_object)


        #cyclegan数据增强
        self.pushButton_5.clicked.connect(self.cyclegan)

        #生成所有
        self.pushButton_7.clicked.connect(self.all_augment)





    def all_augment(self):
        image_path=os.path.split(self.image_path[0])[0]
        Augment(img_path=image_path, xml_path=self.xml_path, img_save_path=self.image_save_path, xml_save_xml=self.xml_save_path,)







    def cyclegan(self):
        cyclegan_image=cycleGANAugmentaion(image_path=self.image_path[0], xml_path=self.xml_path, image_save_path=self.image_save_path, xml_save_path=self.xml_save_path, mode="dir_predict")
        self.out_video.clear()
        pix = QtGui.QPixmap(cyclegan_image)  # 注意修改Windows路径问题
        self.out_video.setPixmap(pix)
        # self.out_video.setScaledContents(True)



    def cut_mix(self):
        category = ['gtz', "others", "group", "connection"]
        cutmix_image=CutmixAugmentation(image_path=self.image_path[0],xml_path=self.xml_path,image_save_path=self.image_save_path,xml_save_path=self.xml_save_path,category=category)
        self.out_video.clear()
        pix = QtGui.QPixmap(cutmix_image)  # 注意修改Windows路径问题
        self.out_video.setPixmap(pix)
        # self.out_video.setScaledContents(True)

    def small_object(self):
        category = ['gtz', "others", "group", "connection"]
        objects = ['gtz', "others", "connection"]
        min_xml = self.lineEdit.text()
        max_xml = self.lineEdit_2.text()

        min_xmls = min_xml.split(sep='*', maxsplit=-1)
        max_xmls = max_xml.split(sep='*', maxsplit=-1)
        min_xml  = int(min_xmls[0])*int(min_xmls[1])
        max_xml  =int(max_xmls[0])*int(max_xmls[1])

        Small_image=Samll_object_Augmentation(image_path=self.image_path[0],xml_path=self.xml_path,image_save_path=self.image_save_path,xml_save_path=self.xml_save_path,
                                  SOA_THRESH=min_xml, SOA_PROB=1, SOA_COPY_TIMES=3, SOA_EPOCHS=30,Low_SOA_THRESH=max_xml,category=category,objects=objects)
        self.out_video.clear()
        pix = QtGui.QPixmap(Small_image)  # 注意修改Windows路径问题
        self.out_video.setPixmap(pix)
        # self.out_video.setScaledContents(True)


    def mix_up(self):
        mix_up_image=mix_up(image_path=self.image_path[0], xml_path=self.xml_path, save_image=self.image_save_path,save_xml=self.xml_save_path)
        self.out_video.clear()
        pix = QtGui.QPixmap(mix_up_image)  # 注意修改Windows路径问题
        self.out_video.setPixmap(pix)
        # self.out_video.setScaledContents(True)




    def nosie_enduance(self):
        self.nosie_type = self.comboBox.currentText()  # 返回选中选项的文本
        if self.nosie_type==self.pt_list[1]:
            image_jy=jiao_yan(image_path=self.image_path[0],image_save_path=self.image_save_path,xml_path=self.xml_path,xml_save_path=self.xml_save_path)
            self.out_video.clear()
            pix = QtGui.QPixmap(image_jy)  # 注意修改Windows路径问题
            self.out_video.setPixmap(pix)
            # self.out_video.setScaledContents(True)
        elif self.nosie_type==self.pt_list[2]:
            image_gs = gao_si_noise(image_path=self.image_path[0], image_save_path=self.image_save_path,
                                xml_path=self.xml_path, xml_save_path=self.xml_save_path,gs_var=0.01)
            self.out_video.clear()
            pix = QtGui.QPixmap(image_gs)  # 注意修改Windows路径问题
            self.out_video.setPixmap(pix)
            # self.out_video.setScaledContents(True)
        elif self.nosie_type==self.pt_list[3]:
            image_bo= bo_song_noise(image_path=self.image_path[0], image_save_path=self.image_save_path,
                                xml_path=self.xml_path, xml_save_path=self.xml_save_path)
            self.out_video.clear()
            pix = QtGui.QPixmap(image_bo)  # 注意修改Windows路径问题
            self.out_video.setPixmap(pix)
            # self.out_video.setScaledContents(True)

        else:
            self.out_video.clear()



    def image_dir(self, Filepath):
        self.image_path = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files (*);;Text Files (*.txt)")
        # 打开图片
        pix = QtGui.QPixmap(self.image_path[0])  # 注意修改Windows路径问题
        self.raw_video.setPixmap(pix)
        # self.raw_video.setScaledContents(True)
    def image_save(self, Filepath):
        self.image_save_path= QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件", "./")

    def xml_save(self, Filepath):
        self.xml_save_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件", "./")

    def xml_dir(self):
        self.xml_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件", "./")





    def max_or_restore(self):
        if self.maxButton.isChecked():
            self.showMaximized()
        else:
            self.showNormal()


if __name__ == "__main__":
    app = QApplication(sys.argv)                    #初始化       提供整个图像界面底层管理，例如：初始化，程序入口，参数处理，点击输入拖拽，
    myWin = MainWindow()                            # 创建主窗口

    myWin.show()
    myWin.showMinimized()
    sys.exit(app.exec_())
