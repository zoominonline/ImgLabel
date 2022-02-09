import sys, os, subprocess
from PySide6.QtCore import QSize
from PySide6.QtWidgets import ( QApplication, QWidget, 
             QVBoxLayout, QHBoxLayout, QPushButton,QFrame
)
from ui import ClassifyImgLabel, InfoPanel, ClassifyActivityBtns
from models import WorkFolder
from models import winH, winW, imgH, imgW, strbtnstylesys

class MainWindow(QWidget):
    def __init__(self, workFolder: WorkFolder):
        super().__init__()
        self.setMaximumSize(QSize(winW, winH))
        self.workFolder=workFolder
        layout=QHBoxLayout()
        panelsLayout=QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle(str(workFolder))
        self.imgLabel=ClassifyImgLabel(workFolder,self)
        self.imgLabel.setFixedSize(QSize(imgW, imgH))
        self.activityPanel=ClassifyActivityBtns(workFolder,self)
        self.infoPanel=InfoPanel(workFolder,self)
        layout.addWidget(self.imgLabel)
        layout.addLayout(panelsLayout)
        panelsLayout.addWidget(self.infoPanel)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        #panelsLayout.addStretch()
        panelsLayout.addWidget(line)
        panelsLayout.addWidget(self.activityPanel)
        openBtn = QPushButton('Open Work Folder')
        panelsLayout.addWidget(openBtn)
        openBtn.setStyleSheet(strbtnstylesys)
        openBtn.clicked.connect(self.openDir)
        
        exitBtn=QPushButton('Exit')
        panelsLayout.addWidget(exitBtn)
        exitBtn.setStyleSheet(strbtnstylesys)
        exitBtn.clicked.connect(app.exit)
    
    def openDir(self):
        if sys.platform.startswith('win'):
            os.startfile(str(self.workFolder))
        elif sys.platform.startswith('darwin'):
            subprocess.call(["open", str(self.workFolder)])
        elif sys.platform.startswith('linux'):
            subprocess.call(["xdg-open", str(self.workFolder)])
        
if __name__ == "__main__":
    app = QApplication([])
    if len(sys.argv)==2:
        wf=WorkFolder(sys.argv[1])
        if wf:
            win=MainWindow(wf)
            win.show()
            app.exec()
        else:
            print("""Please select a Directory containing at least one image to be labled!""")
    else:
        print(r"""Usage:
    python main.py 'C:\YOUR IMAGES\DIR'""")