from PySide2.QtWidgets import  *
from PySide2.QtUiTools import *
from PySide2.QtCore import *
from PySide2 import QtGui,QtCore,QtWidgets
from PySide2.QtGui import *
from moviepy.editor import VideoFileClip
import threading
import cv2
import sys, os
import PySide2
import datetime
import matplotlib
import matplotlib.pyplot as plt
from PySide2.QtGui import QMovie
import sys
matplotlib.use('agg')
sys.path.append('deploy')

from ui_tools.MyControl import *

from PIL import Image

from PySide2.QtCore import QEventLoop, QTimer
from PySide2 import QtCore

# 重定向信号
class EmittingStr(QtCore.QObject):
        textWritten = QtCore.Signal(str)  # 定义一个发送str的信号，这里用的方法名与PyQt5不一样

        def write(self, text):
            self.textWritten.emit(str(text))
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()




class Status():
    def __init__(self):
        self.id_num = 0
        self.handleCalc()

    def show_ui(self,location):
        qfile = QFile(location)
        qfile.open(QFile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)
        self.ui.setWindowTitle('this is a test process')

    def switchType(self,type):
        '''
        type: 1==>图片，0==>视频
        '''
        if type == 1:
            return "图片类型 (*.png *.jpg)"
        else:
            return "视频类型 (*.mp4 *.avi)"

    def open_one_file_dialog(self,title,type):
        type = self.switchType(type)
        file_path,_ = QFileDialog.getOpenFileNames(
            self.ui, #父窗口对象
            title,  #显示标题
            r"/home/once", #起始目录
            type  #选择类型过滤项，过滤内容在括号中
        )
        return file_path

    def open_video(self):
        self.have_show_time=0

        self.ui.label_3.setFixedSize\
            (self.ui.label_3.width(), self.ui.label_3.height())

        self.frame_count = 0
        self.timer_camera1 = QTimer()
        # self.load_video_controller()

    # def load_video_controller(self):
    #     self.ui.pu


    # def load_video(self,control_hide,control_label):
    def load_video(self):

        file_path = self.open_one_file_dialog('选择视频需要检测的视频',0)
        # print(file_path,'------1')

        file_name = file_path[0]
        # print(file_name,'------2')
        self.file_name = file_name.split('.')[0] + '.mp4'
        if file_path == " ":
            return

        self.open_video()

    def handleCalc(self):
        self.show_ui('mainwindow.ui')

        self.ui.show()
        # self.ui.pushButton_3.clicked.connect(self.load_video(self.ui.pushButton_3,self.ui.label_3))
        self.ui.pushButton_3.clicked.connect(self.load_video)

        self.ui.pushButton_4.clicked.connect(self.video_pause)
        self.ui.pushButton_5.clicked.connect(self.video_stop)
        self.ui.pushButton_6.clicked.connect(self.result_show)
        #
        # import sys
        # sys.stdout = EmittingStr()
        # self.ui.textBrowser.connect(sys.stdout, QtCore.SIGNAL("textWritten(QString)"), self.outputWritten)
        # sys.stderr = EmittingStr()
        # self.ui.textBrowser.connect(sys.stderr, QtCore.SIGNAL("textWritten(QString)"), self.outputWritten)


        # self.ui.show()


    def outputWritten(self, text):
        # self.edt_log.clear()
        cursor = self.ui.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textBrowser.setTextCursor(cursor)
        self.ui.textBrowser.ensureCursorVisible()










    def video_stop(self):
        self.timer_camera1.stop()
        self.cap.release()

    def load_model(self):
        print(self.file_name)
        starttime = datetime.datetime.now()
        print('***'*50)
        # python_exe = os.environ['PYTHON']
        val = os.system('%s /home/onco/ProjectCodes/object_tracking/yolov7-object-tracking/detect_and_track.py --weights=yolov7.pt --source=%s' \
                % ('python', self.file_name))
        end_time = datetime.datetime.now()




    def video_pause(self):

        self.t1 = threading.Thread(target=self.load_model)
        self.t1.start()

    def result_show(self):
        self.frame_count = 0

        self.cap = cv2.VideoCapture(self.file_name)
        self.ui.label_3.setText(str(round(self.cap.get(cv2.CAP_PROP_FPS))))
        self.timer_camera1.start(120)
        self.timer_camera1.timeout.connect(self.openFrame)

    def openFrame(self):
        ret,frame = self.cap.read()
        if ret:
            self.Display_Image(frame, self.ui.label_3)
            self.frame_count = self.frame_count + 1
            self.ui.label_frames.setText(str( self.frame_count))
        else:
            print("播放结束")
            self.cap.release()
            self.timer_camera1.stop()

    def Display_Image(self,image,controller):
        self.have_show_time = self.have_show_time + 1
        if (len(image.shape) == 3):
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            Q_img = QImage(image.data,
                           image.shape[1],
                           image.shape[0],
                           QImage.Format_RGB888)
        elif (len(image.shape) == 1):
            Q_img = QImage(image.data,
                           image.shape[1],
                           image.shape[0],
                           QImage.Format_Indexed8)
        else:
            Q_img = QImage(image.data,
                           image.shape[1],
                           image.shape[0],
                           QImage.Format_RGB888)

        controller.setPixmap(QtGui.QPixmap(Q_img))
        controller.setScaledContents(True)

        if (self.have_show_time / self.have_show_video) % 50 == 0 and self.have_show_video == 2:
            # 这里只针对多镜头检测
            item = QListWidgetItem()
            self.listWidget.addItem(item)
            item.setSizeHint(QSize(330, 70))
            widget = QWidget()
            widget.resize(330, 70)
            # f = open('test.txt', 'r')
            first_info = "source/second/menu_car.PNG"
            second_info = "source/second/menu_car.PNG"
            id_num = self.id_num
            self.id_num = self.id_num + 1
            """
            !!!!!!!!!!!!!!!!!!!!
            这里的注释必看！！！！！
            如果是随着视频播放，检测数据进行更新的话，这里将会进行更新
            first_info是跨境头检测的，检测数据的，第一张图片
            second_info是第二章图片
            id_num是第几个也就是id
            """
            label1 = double_photo_show_label(widget, 0, first_info
                                             , 10, 0, 100, 70)
            label2 = double_photo_show_label(widget, 0, second_info
                                             , 126, 0, 100, 70)
            label3 = double_photo_show_label(widget, 1, id_num
                                             , 242, 17, 98, 36)
            self.listWidget.setItemWidget(item, widget)

if __name__ == '__main__':
    app = QApplication([])
    MainWindow=QMainWindow()
    statu = Status()
    statu.ui.show()
    app.exec_()
