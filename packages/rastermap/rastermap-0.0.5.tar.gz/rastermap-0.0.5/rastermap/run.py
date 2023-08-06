import numpy as np
import os
from PyQt5 import QtGui, QtCore

### custom QDialog which allows user to fill in ops and run suite2p!
class RunWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(RunWindow, self).__init__(parent)
        self.setGeometry(50,50,600,600)
        self.setWindowTitle('Choose rastermap run options')
        self.win = QtGui.QWidget(self)
        self.layout = QtGui.QGridLayout()
        self.layout.setHorizontalSpacing(25)
        self.win.setLayout(self.layout)

        # default ops
        self.ops = {'n_components': 2, 'n_X': 40, 'n_Y': 0, 'alpha': 1., 'K': 1.,
                    'nPC': 200, 'sig_Y': 2, 'init': 'pca'}

        keys = ['n_components','n_X','n_Y','alpha','K','nPC','sig_Y','init']
        tooltips = ['each tiff has this many planes in sequence',
                    'each tiff has this many channels per plane',
                    'this channel is used to extract functional ROIs (1-based)',
                    'approximate diameter of ROIs in pixels (can input two numbers separated by a comma for elongated ROIs)',
                    'timescale of sensor in deconvolution (in seconds)',
                    'sampling rate (per plane)',
                    'if 1, binary file is deleted after processing is complete',
                    'save output also as mat file "Fall.mat"',
                    'combine results across planes in separate folder "combined" at end of processing',
                    '0 to select num_cores, -1 to disable parallelism, N to enforce value',
                    'ROI detection parallelism: 0 to select number of planes, -1 to disable parallelism, N to enforce value',
                    'if 1, registration is performed',
                    'when multi-channel, you can align by non-functional channel (1-based)',
                    '# of subsampled frames for finding reference image',
                    'number of frames per batch',
                    'max allowed registration shift, as a fraction of frame max(width and height)',
                    '1.15 good for 2P recordings, recommend >5 for 1P recordings',
                    'if 1, unregistered binary is kept in a separate file data_raw.bin',
                    'if 1, registered tiffs are saved',
                    'if 1, registered tiffs of channel 2 (non-functional channel) are saved',
                    'whether to use nonrigid registration (splits FOV into blocks of size block_size)',
                    'block size in number of pixels in Y and X (two numbers separated by a comma)',
                    'if any nonrigid block is below this threshold, it gets smoothed until above this threshold. 1.0 results in no smoothing',
                    'maximum *pixel* shift allowed for nonrigid, relative to rigid',
                    'whether or not to require ROIs to be fully connected (set to 0 for dendrites/boutons)',
                    'ROIs with greater than this overlap as a fraction of total pixels will be discarded',
                    'adjust the automatically determined threshold by this scalar multiplier',
                    'whether to smooth masks in final pass of cell detection',
                    'maximum number of iterations for ROI detection',
                    'max number of binned frames for the SVD',
                    'max number of SVD components to keep for ROI detection',
                    'ratio between neuropil basis size and cell radius',
                    'running mean subtraction with window of size "high_pass" (use low values for 1P)',
                    'allow shared pixels to be used for fluorescence extraction from overlapping ROIs (otherwise excluded from both ROIs)',
                    'number of pixels between ROI and neuropil donut',
                    'minimum number of pixels in the neuropil',
                    'window for maximin',
                    'smoothing constant for gaussian filter',
                    'smoothing constant for gaussian filter',
                    'neuropil coefficient']

        bigfont = QtGui.QFont("Arial", 10, QtGui.QFont.Bold)
        l=0
        self.keylist = []
        self.editlist = []
        k=0
        for key in keys:
            qedit = LineEdit(k,key,self)
            qlabel = QtGui.QLabel(key)
            qlabel.setToolTip(tooltips[k])
            qedit.set_text(self.ops)
            qedit.setFixedWidth(90)
            self.layout.addWidget(qlabel,k,0,1,1)
            self.layout.addWidget(qedit,k,1,1,1)
            self.keylist.append(key)
            self.editlist.append(qedit)
            k+=1

        self.layout.addWidget(QtGui.QLabel("."),19,4,1,1)
        self.layout.addWidget(QtGui.QLabel("."),19,5,1,1)
        self.layout.addWidget(QtGui.QLabel("."),19,6,1,1)
        self.layout.addWidget(QtGui.QLabel("."),19,7,1,1)
        self.layout.addWidget(QtGui.QLabel("."),19,8,1,1)

        self.layout.setColumnStretch(4,10)
        self.runButton = QtGui.QPushButton('RUN')
        self.runButton.clicked.connect(lambda: self.run_RMAP(parent))
        self.layout.addWidget(self.runButton,19,0,1,1)
        #self.runButton.setEnabled(False)
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.layout.addWidget(self.textEdit, 20,0,30,9)
        self.process = QtCore.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.stdout_write)
        self.process.readyReadStandardError.connect(self.stderr_write)
        # disable the button when running the s2p process
        self.process.started.connect(self.started)
        self.process.finished.connect(lambda: self.finished(parent))
        # stop process
        self.stopButton = QtGui.QPushButton('STOP')
        self.stopButton.setEnabled(False)
        self.layout.addWidget(self.stopButton, 19,1,1,1)
        self.stopButton.clicked.connect(self.stop)

    def run_RMAP(self, parent):
        self.finish = True
        self.error = False
        self.save_text()
        np.save('ops.npy', self.ops)
        print('Running rastermap!')
        print('starting process')
        if parent.file_iscell is not None:
            self.process.start('python -u -W ignore -m rastermap --ops ops.npy --S %s --iscell %s'%(parent.filebase, parent.file_iscell))
        else:
            self.process.start('python -u -W ignore -m rastermap --ops ops.npy --S %s'%parent.filebase)


    def stop(self):
        self.finish = False
        self.process.kill()

    def started(self):
        self.runButton.setEnabled(False)
        self.stopButton.setEnabled(True)

    def finished(self, parent):
        self.runButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        if self.finish and not self.error:
            cursor = self.textEdit.textCursor()
            cursor.movePosition(cursor.End)
            cursor.insertText('Opening in GUI (can close this window)\n')
            basename,fname = os.path.split(parent.fname)
            parent.fname = os.path.join(basename, 'embedding.npy')
            parent.load_proc(parent.fname)
        elif not self.error:
            cursor = self.textEdit.textCursor()
            cursor.movePosition(cursor.End)
            cursor.insertText('Interrupted by user (not finished)\n')
        else:
            cursor = self.textEdit.textCursor()
            cursor.movePosition(cursor.End)
            cursor.insertText('Interrupted by error (not finished)\n')

    def save_text(self):
        for k in range(len(self.editlist)):
            key = self.keylist[k]
            self.ops[key] = self.editlist[k].get_text(self.ops[key])

    def stdout_write(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(str(self.process.readAllStandardOutput(), 'utf-8'))
        self.textEdit.ensureCursorVisible()

    def stderr_write(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText('>>>ERROR<<<\n')
        cursor.insertText(str(self.process.readAllStandardError(), 'utf-8'))
        self.textEdit.ensureCursorVisible()
        self.error = True

class LineEdit(QtGui.QLineEdit):
    def __init__(self,k,key,parent=None):
        super(LineEdit,self).__init__(parent)
        self.key = key
        #self.textEdited.connect(lambda: self.edit_changed(parent.ops, k))

    def get_text(self,okey):
        key = self.key
        if key=='diameter' or key=='block_size':
            diams = self.text().replace(' ','').split(',')
            if len(diams)>1:
                okey = [int(diams[0]), int(diams[1])]
            else:
                okey = int(diams[0])
        else:
            if type(okey) is float:
                okey = float(self.text())
            elif type(okey) is str:
                okey = self.text()
            elif type(okey) is int or bool:
                okey = int(self.text())

        return okey

    def set_text(self,ops):
        key = self.key
        if key=='diameter' or key=='block_size':
            if (type(ops[key]) is not int) and (len(ops[key])>1):
                dstr = str(int(ops[key][0])) + ', ' + str(int(ops[key][1]))
            else:
                dstr = str(int(ops[key]))
        else:
            if type(ops[key]) is bool:
                dstr = str(int(ops[key]))
            elif type(ops[key]) is str:
                dstr = ops[key]
            else:
                dstr = str(ops[key])
        self.setText(dstr)
