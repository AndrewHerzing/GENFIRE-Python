import VolumeSlicer_MainWindow
from PyQt4 import QtCore, QtGui
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from functools import partial

class VolumeSlicer(QtGui.QMainWindow):
    def __init__(self, volume):
        super(VolumeSlicer, self).__init__()
        self.volume = volume
        self.ui = VolumeSlicer_MainWindow.Ui_VolumeSlicer()
        self.ui.setupUi(self)
        self.ui.checkBox_lockcmap.toggled.connect(self.toggleLockCmap)
        self.lockColormap = False
        self.ui.checkBox_lockcmap.setChecked(False)

        self.fig1 = plt.figure()
        self.fig2 = plt.figure()
        self.fig3 = plt.figure()

        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas3 = FigureCanvas(self.fig3)

        self.slice1 = self.fig1.add_subplot(111)
        self.slice2 = self.fig2.add_subplot(111)
        self.slice3 = self.fig3.add_subplot(111)

        self.slice1.hold(False)
        self.slice2.hold(False)
        self.slice3.hold(False)

        self.navigationToolbar1 = NavigationToolbar(self.canvas1, self)
        self.navigationToolbar2 = NavigationToolbar(self.canvas2, self)
        self.navigationToolbar3 = NavigationToolbar(self.canvas3, self)

        self.ui.vt_lyt_fig1.addWidget(self.navigationToolbar1)
        self.ui.vt_lyt_fig1.addWidget(self.canvas1)
        self.ui.vt_lyt_fig2.addWidget(self.navigationToolbar2)
        self.ui.vt_lyt_fig2.addWidget(self.canvas2)
        self.ui.vt_lyt_fig3.addWidget(self.navigationToolbar3)
        self.ui.vt_lyt_fig3.addWidget(self.canvas3)

        dimx, dimy, dimz = np.shape(volume)
        ncx,  ncy,  ncz  = dimx//2., dimy//2, dimz//2
        ncx,  ncy,  ncz  = int(ncx), int(ncy), int(ncz)

        self.ui.scrlbr_fig1.valueChanged.connect(partial(self.setTextFromSlider,self.ui.lineEdit_scrlbr1))
        self.ui.scrlbr_fig2.valueChanged.connect(partial(self.setTextFromSlider,self.ui.lineEdit_scrlbr2))
        self.ui.scrlbr_fig3.valueChanged.connect(partial(self.setTextFromSlider,self.ui.lineEdit_scrlbr3))

        self.ui.scrlbr_fig1.setValue(ncx)
        self.ui.scrlbr_fig1.setMinimum(0)
        self.ui.scrlbr_fig1.setMaximum(dimx-1)

        self.ui.scrlbr_fig2.setValue(ncy)
        self.ui.scrlbr_fig2.setMinimum(0)
        self.ui.scrlbr_fig2.setMaximum(dimy-1)

        self.ui.scrlbr_fig3.setValue(ncz)
        self.ui.scrlbr_fig3.setMinimum(0)
        self.ui.scrlbr_fig3.setMaximum(dimz-1)

        self.ui.lineEdit_scrlbr1.textChanged.connect(partial(self.setSliderFromText,self.ui.scrlbr_fig1))
        self.ui.lineEdit_scrlbr2.textChanged.connect(partial(self.setSliderFromText,self.ui.scrlbr_fig2))
        self.ui.lineEdit_scrlbr3.textChanged.connect(partial(self.setSliderFromText,self.ui.scrlbr_fig3))

        self.currentSliceX = ncx
        self.currentSliceY = ncy
        self.currentSliceZ = ncz
        self.updateAll()

        self.ui.scrlbr_fig1.valueChanged[int].connect(self.updateSliceX)
        self.ui.scrlbr_fig2.valueChanged[int].connect(self.updateSliceY)
        self.ui.scrlbr_fig3.valueChanged[int].connect(self.updateSliceZ)

        self.clim1 = plt.getp(plt.getp(self.slice1,'images')[0],'clim')
        self.clim2 = plt.getp(plt.getp(self.slice2,'images')[0],'clim')
        self.clim3 = plt.getp(plt.getp(self.slice3,'images')[0],'clim')

        self.lockColormap = True
        self.ui.checkBox_lockcmap.setChecked(True)


    def updateSliceX(self, nx):
        self.slice1.imshow(np.squeeze(self.volume[nx, :, :]))
        if self.lockColormap:
            plt.setp(plt.getp(self.slice1,'images')[0],'clim',self.clim1)
        self.canvas1.draw()

    def updateSliceY(self, ny):
        self.slice2.imshow(np.squeeze(self.volume[:, ny, :]))
        if self.lockColormap:
            plt.setp(plt.getp(self.slice2,'images')[0],'clim',self.clim2)
        self.canvas2.draw()

    def updateSliceZ(self, nz):
        self.slice3.imshow(np.squeeze(self.volume[:, :, nz]))
        if self.lockColormap:
            plt.setp(plt.getp(self.slice3,'images')[0],'clim',self.clim3)
        self.canvas3.draw()

    def updateAll(self):
        self.updateSliceX(self.currentSliceX)
        self.updateSliceY(self.currentSliceY)
        self.updateSliceZ(self.currentSliceZ)

    def toggleLockCmap(self):
        if self.ui.checkBox_lockcmap.isChecked():
            self.lockColormap = True
        else:
            self.lockColormap = False

    def setSliderFromText(self, slider, text):
        slider.setValue(text.toInt()[0])

    def setTextFromSlider(self, lineedit, value):
        lineedit.setText(QtCore.QString(str(value)))