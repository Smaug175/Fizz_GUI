from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from Audio import Ui_Form
from aip import AipSpeech
import os,uuid,time

class Audio(QMainWindow, Ui_Form):

    APP_ID = '11079594'  # 设置自己创建百度云应用时的ID
    API_KEY = 'fMA2S0U0dGPHbdbn3EmtRGfZ'  # 设置自己创建百度云应用时的APIKey
    SECRET_KEY = '2d9bbfc2a45bde1056d0c1fd272fd5f2'  # 设置自己创建百度云应用时的SECRETKey
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)  # 创建语音识别对象

    def __init__(self):
        super(Audio, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 关联“语音合成”按钮的方法
        self.pushButton.clicked.connect(self.txtToAudio)
        # 关联“选择”按钮的方法,进行语音识别
        self.pushButton_2.clicked.connect(self.recAudio)

    def txtToAudio(self):
        voice = 0
        if self.radioButton.isChecked():
            voice = 0  # 女声
        elif self.radioButton_2.isChecked():
            voice = 1  # 男声
        elif self.radioButton_3.isChecked():
            voice = 3  # 度逍遥
        elif self.radioButton_4.isChecked():
            voice = 4  # 度丫丫
        # 语音合成
        result = self.client.synthesis(self.textEdit.toPlainText(), 'zh', 3, {
            'vol': 5,
            'per': voice,
        })
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).replace('-', '').replace(':', '').replace(' ','')  # 获取当前日期时间
        # 识别正确返回语音二进制，错误则返回dict
        if not isinstance(result, dict):
            with open(str(now) + '.mp3', 'wb') as f:
                f.write(result)
            QMessageBox.information(None, '提示', '文字已经转换为相应的MP3文件，请在当前项目路径中查看！', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, '警告', '转换失败，请确认转换的文本长度不超过1024字节（342个汉字）！', QMessageBox.Ok)

    def recAudio(self):
        # 记录用户选择的音频文件地址
        filepath,filetype=QFileDialog.getOpenFileName(None,'选择语音文件','C:\\',"音频(*.mp3;*.wav)")
        if filepath != "": # 判断是否选择了文件
            self.lineEdit.setText(filepath)
            path = os.path.splitdrive(filepath)[0]  # 得到原音频的路径
            if not path.endswith('\\'):  # 判断路径是否以\结尾
                path = path + '\\'  # 为路径结尾增加\
            newaudio = uuid.uuid1()  # 随机生成临时文件名
            newfile = os.path.join(path, str(newaudio) + ".wav")  # 新的文件（包含路径和扩展名）
            # 定义使用ffmpeg转换视频的命令，将mp3格式转换为采用16K采样率的wav文件
            cmd = "ffmpeg -i " + str(filepath) + " -ar 16000 -ac 1  -f wav " + newfile
            os.popen(cmd)  # 执行格式转换命令
            time.sleep(0.2)  # 休眠0.2秒，这里主要是为了执行上面的转换操作
            if os.path.exists(newfile):  # 判断是否存在新转换的文件
                with open(newfile, 'rb') as f:  # 以二进制形式打开文件
                    # 识别音频文件内容
                    result = self.client.asr(f.read(), 'wav', 16000, {'dev_pid': 1536, })
                    self.textEdit_2.setText(result['result'][0])# 显示识别结果
            else:
                QMessageBox.warning(None, '警告', '没有该文件！', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, '警告', '请选择一个有效文件……', QMessageBox.Ok)

if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    audio=Audio()
    audio.show()
    sys.exit(app.exec_())
