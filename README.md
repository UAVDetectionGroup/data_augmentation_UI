# data_augmentation_UI
## 数据增强的ui界面
### 文件夹说明
1.icon 用于存放各种界面图片
2.main_win 是ui界面以及生成的py文件（可使用QTdesger打开）
3.model存放数据增强的模型（mixup，cutmix，小目标，噪声，cyclegan）
4.test用于|--image （存放测试图片）
          |--xml（存放标注文件（voc格式））
          |--image_save（生成数据增强测试图片保存路径）
          |--xml_save_patj（生成数据增强的xml文件）
### 数据增强使用说明
1.在main.py里面修改  
   def cut_mix(self):   117行
        category = ['gtz', "others", "group", "connection"] #改
 使得category为数据集标注的种类
     def small_object(self):   125行
        category = ['gtz', "others", "group", "connection"]
        objects = ['gtz', "others", "connection"]
  使得category为数据集标注的种类
  使得objects为小目标要增强的种类
 2.直接运行main.py即可
 3.<img width="754" alt="image" src="https://github.com/UAVDetectionGroup/data_augmentation_UI/assets/107593840/de78d49f-af1d-4fd0-9592-b4a293393bf5">
