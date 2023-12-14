from PySide6 import QtCore


class LaunchPz(QtCore.QObject):
    def __init__(self, Ui, exePZ):
        super(LaunchPz, self).__init__()
        self.commande = exePZ
        self.Ui = Ui
        self.process = None
        self.argument = []
        self.initClass()

    def initClass(self):
        self.output = self.Ui.textEdit_Log
        self.process = QtCore.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.dataReady)

    def dataReady(self):
        # cursor.movePosition(cursor.End)
        data = str(self.process.readAllStandardOutput())
        self.output.insertHtml(self.parserdata(data))
        self.output.ensureCursorVisible()

    def parserdata(self, data):
        """
        Parcours les données renvoyés par PZ
        """
        listinfo = data.split("\n")
        returnData = ""
        for info in listinfo:
            info = info.replace("\\n", "<br>")\
                .replace("b'", "")\
                .replace('\\r', "")\
                .replace("'", "")\
                .replace('ERROR', "<strong>ERROR</strong>")\
                .replace('WARN', "<strong>WARN</strong>")\
                .replace('LOG', "<strong>LOG</strong>")\
                .replace('DEBUG', "<strong>DEBUG</strong>")
            if not self.Ui.checkBox_LOGWarn.isChecked() and ("<strong>WARN</strong>" in info or "<strong>ERROR</strong>" in info):
                info = ""
            elif not self.Ui.checkBox_LOGDebug.isChecked() and "<strong>DEBUG</strong>" in info:
                info = ""
            elif not self.Ui.checkBox_LOG.isChecked() and "<strong>LOG</strong>" in info:
                info = ""
            elif info != "":
                returnData += f"{info}"
        return returnData
    
    def parseArguments(self):
        
        if self.Ui.checkBox_DebugMode.isChecked():
            self.argument.append("-debug")
        
    
    def start(self):
        self.parseArguments()
        self.process.start(self.commande, self.argument)