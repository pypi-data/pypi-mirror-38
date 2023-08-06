import sys, os.path, time, csv, io, queue

from qtpy import QtCore, QtWidgets, QtWidgets

import infupy.backends.fresenius as fresenius
from infupy.gui.syringorecueil_ui import Ui_wndMain

DEBUG = True

class Worker(QtCore.QObject):
    sigConnected      = QtCore.Signal()
    sigDisconnected   = QtCore.Signal()
    sigUpdateSyringes = QtCore.Signal(list)
    sigError          = QtCore.Signal(str)

    def __init__(self):
        super(Worker, self).__init__()
        self.oldconnstate = False
        self.destfolder = os.path.expanduser("~")
        self.port = ""
        self.conn = None
        self.base = None
        self.logger = None
        self.syringes = dict()
        self.csvfd = io.IOBase()
        self.csv = None
        self.shouldrun = False

        self.conntimer = QtCore.QTimer()
        self.conntimer.timeout.connect(self.connectionLoop)

        self.logtimer = QtCore.QTimer()
        self.logtimer.timeout.connect(self.logLoop)

        self.conntimer.start(5000) # 5 seconds

    @QtCore.Slot()
    def start(self):
        self.shouldrun = True

    @QtCore.Slot()
    def stop(self):
        self.shouldrun = False

    @QtCore.Slot(str)
    def setport(self, port):
        self.port = port

    @QtCore.Slot(str)
    def setfolder(self, folder):
        self.destfolder = folder

    def connectionLoop(self):
        if not self.shouldrun:
            self.onDisconnected()
            return

        if not self.checkSerial():
            if not self.connectSerial():
                return
        if not self.checkBase():
            if self.connectBase():
                self.onConnected()
            else:
                self.onDisconnected()
                return
        self.checkSyringes()
        self.attachNewSyringes()

    def logLoop(self):
        try: # Ensure file is open and writable.
            if self.csvfd.closed or not self.csvfd.writable():
                raise IOError("Not writable")
        except (IOError, ValueError) as e:
            if self.shouldrun:
                self.reportUI("File: {}".format(e))
            return

        while True: # Dump the whole queue to csv
            try:
                dt, origin, msg = self.conn.eventq.get_nowait()
            except queue.Empty:
                break

            try:
                volume = fresenius.extractVolume(msg)
            except ValueError:
                self.reportUI("Failed to decode volume value")
                continue

            if DEBUG: print("{}:{}:{}".format(dt, origin, volume), file=sys.stderr)

            timestamp = int(dt.timestamp() * 1e9)
            self.csv.writerow({'timestamp' : timestamp,
                               'syringe'   : origin,
                               'volume'    : volume})

    def onConnected(self):
        if self.oldconnstate == True:
            if DEBUG: print("Already connected", file=sys.stderr)
            return # already connected

        self.oldconnstate = True
        self.sigConnected.emit()
        self.csvfd.close()
        if self.csvfd.closed or not self.csvfd.writable():
            # We need to open a new file
            self.csvfd.close()
            filename = time.strftime('%Y%m%d-%H%M.csv')
            filepath = os.path.join(self.destfolder, filename)
            self.csvfd = open(filepath, 'w', newline='')
            self.reportUI("Opened file: {}".format(filepath))
            self.csv = csv.DictWriter(self.csvfd, fieldnames = ['timestamp', 'syringe', 'volume'])
            self.csv.writeheader()
        self.logtimer.start(1000) # 1 second

    def onDisconnected(self):
        if self.oldconnstate == False:
            if DEBUG: print("Already disconnected", file=sys.stderr)
            return # already disconnected

        self.oldconnstate = False
        self.sigDisconnected.emit()
        # Clean up
        self.syringes = dict()
        self.base = None
        self.sigUpdateSyringes.emit([])
        # Stop csv logging
        self.logtimer.stop()
        # Call once more to empty the queue
        self.logLoop()
        self.csvfd.close()
        if not self.shouldrun and self.conn is not None:
            self.conn.close()
            self.conn = None

    def checkSyringes(self):
        for i, s in self.syringes.copy().items():
            try:
                dtype = s.readDeviceType()
                if DEBUG: print("Device: {}".format(dtype), file=sys.stderr)
            except Exception as e:
                self.reportUI("Syringe {} lost: {}".format(i, e))
                del self.syringes[i]
            else:
                # Re-register volume event in case the syringe got reset.
                try:
                    s.registerEvent(fresenius.VarId.volume)
                except fresenius.CommandError as e:
                    self.reportUI("Register event error: {}".format(e))

    def attachNewSyringes(self):
        try:
            modids = self.base.listModules()
            self.sigUpdateSyringes.emit(modids)
            for modid in modids:
                if not modid in self.syringes.keys():
                    s = fresenius.FreseniusSyringe(self.conn, modid)
                    s.registerEvent(fresenius.VarId.volume)
                    self.syringes[modid] = s
        except (IOError, fresenius.CommandError) as e:
            self.reportUI("Attach syringe error: {}".format(e))

    def checkSerial(self):
        if self.conn is None:
            return False
        try:
            self.conn.name
        except Exception as e:
            self.reportUI("Serial port exception: {}".format(e))
            return False
        else:
            return True

    def connectSerial(self):
        try:
            self.conn = fresenius.FreseniusComm(self.port)
        except Exception as e:
            self.reportUI("Failed to open serial port: {}".format(e))
            return False
        else:
            return True

    def checkBase(self):
        if self.base is None:
            return False
        try:
            dtype = self.base.readDeviceType()
            if DEBUG: print("Device: {}".format(dtype), file=sys.stderr)
        except Exception as e:
            self.reportUI("Base error: {}".format(e))
            return False
        else:
            return True

    def connectBase(self):
        try:
            self.base = fresenius.FreseniusBase(self.conn)
        except Exception as e:
            self.reportUI("Failed to connect to base: {}".format(e))
            return False
        else:
            return True

    def reportUI(self, err):
        if DEBUG: print(err, file=sys.stderr)
        self.sigError.emit(str(err))

    @QtCore.Slot()
    def cleanup(self):
        self.logtimer.stop()
        self.conntimer.stop()
        for _, s in self.syringes.items():
            s.disconnect()
        if self.base is not None:
            self.base.disconnect()
        if self.conn is not None:
            self.conn.close()
        if self.csvfd is not None:
            self.csvfd.close()


class MainUi(QtWidgets.QMainWindow, Ui_wndMain):
    sigCleanup = QtCore.Signal()

    def __init__(self, parent = None):
        super(MainUi, self).__init__(parent = parent)
        self.setupUi(self)

        # Add Connection label to statusbar
        self.connStatusLabel = QtWidgets.QLabel()
        self.connStatusLabel.setMargin(2)
        self.statusBar.addPermanentWidget(self.connStatusLabel)

        # Init worker
        self.__workerthread = QtCore.QThread()
        self.__worker = Worker()

        # Worker callbacks and signals
        self.btnStart.clicked.connect(self.__worker.start)
        self.btnStop.clicked.connect(self.__worker.stop)
        self.sigCleanup.connect(self.__worker.cleanup)
        self.txtFolder.textChanged.connect(self.__worker.setfolder)
        self.comboCom.editTextChanged.connect(self.__worker.setport)
        self.__worker.setport(self.comboCom.currentText())

        self.__worker.sigConnected.connect(self.connected)
        self.__worker.sigDisconnected.connect(self.disconnected)
        self.__worker.sigUpdateSyringes.connect(self.updateSyringeList)
        self.__worker.sigError.connect(self.showStatusError)

        self.__worker.moveToThread(self.__workerthread)
        self.__workerthread.start()

        # Continue UI initialization
        self.btnBrowse.clicked.connect(self.browsefolder)

    def browsefolder(self):
        folderpreset = self.txtFolder.text()
        if not os.path.isdir(folderpreset):
            folderpreset = os.path.expanduser("~")
        destfolder = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose destination Folder", folderpreset)
        self.txtFolder.setText(destfolder)

    def showStatusError(self, errstr):
        # Show for 3 seconds
        self.statusBar.showMessage(errstr, 3000)

    def connected(self):
        self.connStatusLabel.setStyleSheet("QLabel{background : green;}")
        self.connStatusLabel.setText("Connected")

    def disconnected(self):
        self.lstSyringes.clear()
        self.connStatusLabel.setStyleSheet("QLabel{background : red;}")
        self.connStatusLabel.setText("Disconnected")

    def updateSyringeList(self, slist):
        self.lstSyringes.clear()
        for modid in slist:
            liststr = "Seringue {}".format(modid)
            self.lstSyringes.addItem(liststr)

    def closeEvent(self, event):
        # Wrap it all up
        if DEBUG: print("Cleaning up before exiting.", file=sys.stderr)
        self.sigCleanup.emit()
        self.__workerthread.quit()
        event.accept()


if __name__ == '__main__':
    qApp = QtWidgets.QApplication(sys.argv)

    wMain = MainUi()
    wMain.show()

    sys.exit(qApp.exec_())
