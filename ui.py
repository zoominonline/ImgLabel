from PySide6.QtWidgets import (QWidget, QButtonGroup,
            QLabel, QVBoxLayout, QPushButton, QLineEdit,QFrame)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from models import WorkFolder
from models import classes,strlblstyle

class ClassifyImgLabel(QLabel):
    def __init__(self, workFolder: WorkFolder, width, height, parent=None):
        super().__init__(parent)
        self.width, self.height = width, height
        self.setStyleSheet("border: 1px inset grey;")
        self.setAlignment(Qt.AlignCenter)
        self.workFolder=workFolder
        self.refreshImg()

    def refreshImg(self):
        imgPath=self.workFolder.getCurrentImg()
        if imgPath:
            pix=QPixmap()
            pix.load(imgPath)
            if pix.width()>self.width or pix.height()>self.height:
                pix=pix.scaled(self.width, self.height, Qt.KeepAspectRatio)
            self.setPixmap(pix)
        else:
            self.setFont(QFont('Arial', 20))
            self.setText(f"""No Image left to be Labeled 
in {str(self.workFolder)}, 

'Exit' this App, 

Select another directory that 
CONTAINs IMAGEs to work!""")

class ClassifyActivityBtns(QFrame):
    def __init__(self, workFolder: WorkFolder, parent=None):
        super().__init__(parent)
        layout=QVBoxLayout()
        self.setLayout(layout)
        self.parent=parent
        self.workFolder=workFolder
        self.buttonRoll = QPushButton('Roll(back')
        self.buttonRoll.setShortcut('b')
        self.buttonRoll.clicked.connect(self.rollback)
        self.buttonRoll.setDisabled(True)
        layout.addWidget(self.buttonRoll)
        
        self.cls_group = QButtonGroup()
        self.keys=[]
        id=0
        for key,cl in classes.items():
            self.keys.append(key)
            classifiedBtn = QPushButton(cl+" ("+key)
            classifiedBtn.setShortcut(key)
            layout.addWidget(classifiedBtn)
            self.cls_group.addButton(classifiedBtn, id)
            id +=1            
        self.cls_group.buttonClicked.connect(self.classifiedTo)
        self.checkCurrentImg()
    
    def classifiedTo(self, object):
        clsId=self.cls_group.id(object)
        self.workFolder.labelCurrentImg(self.keys[clsId])
        self.parent.imgLabel.refreshImg()
        self.parent.infoPanel.refreshPanel()
        self.buttonRoll.setDisabled(False)
        self.checkCurrentImg()

    def checkCurrentImg(self):
        if self.workFolder.getCurrentImg():
            self._enableClassify()
        else:
            self._disableClassify()

    def _disableClassify(self):
        for b in self.cls_group.buttons():
            b.setDisabled(True)

    def _enableClassify(self):
        for b in self.cls_group.buttons():
            b.setDisabled(False)

    def rollback(self):
        try:
            self.workFolder.rollback()
            self.parent.imgLabel.refreshImg()
            self.parent.infoPanel.refreshPanel()
        except:
            print('No Classification History to rollback')

        if len(self.workFolder.history)==0:    
            self.buttonRoll.setDisabled(True)
        self._enableClassify()

class InfoPanel(QWidget):
    def __init__(self, workFolder: WorkFolder, parent=None):
        super().__init__()
        layout=QVBoxLayout()
        self.setLayout(layout)
        self.parent=parent
        self.workFolder=workFolder
    
        currentLabel=QLabel('Current Img:')
        self.current=QLineEdit('-')
        self.current.setReadOnly(True)
        self.imgSize=QLabel('-')
        historyLabel=QLabel('Label History:')
        self.history=QLabel('-')
        remainsLabel=QLabel('Remain Imgs:')
        self.remains=QLabel('-')
        labeledLabel=QLabel('Total Labeled Imgs:')
        self.labeled=QLabel('-')
        remainsLabel.setStyleSheet(strlblstyle)
        labeledLabel.setStyleSheet(strlblstyle)
        currentLabel.setStyleSheet(strlblstyle)
        historyLabel.setStyleSheet(strlblstyle)
        layout.addWidget(currentLabel)
        layout.addWidget(self.current)
        layout.addWidget(self.imgSize)
        layout.addWidget(historyLabel)
        layout.addWidget(self.history)
        layout.addWidget(remainsLabel)
        layout.addWidget(self.remains)
        layout.addWidget(labeledLabel)
        layout.addWidget(self.labeled)
        self.refreshPanel()
    
    def refreshPanel(self):
        self.current.setText(self.workFolder.getCurrentName())
        self.imgSize.setText(self.workFolder.getCurrentSize())
        self.history.setText(str(len(self.workFolder.history)))
        self.remains.setText(str(len(self.workFolder.remains)))
        self.labeled.setText(self.workFolder.getLabeledCountStr())