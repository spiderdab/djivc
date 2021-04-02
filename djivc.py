#!/usr/bin/python3

import sys
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QButtonGroup, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QAction, QApplication, QProgressBar, QPushButton, QRadioButton, QTextEdit, QVBoxLayout, QFileDialog
import subprocess, os


class djivc(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def selectInputFile(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self,"Select files to be converted:", "","MP4 (*.MP4 *mp4)", options=options)
        if files:
            #print(files)
            self.input_files = files
            for file in files:
                self.input_text.append(file)

    def selectOutputFolder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.DontResolveSymlinks
        folder = QFileDialog.getExistingDirectory(self, "Choose Folder", "/home", options=options)
        if folder:
            #print(folder)
            self.output_folder = folder
            self.folder_text.setText(folder)

    def startConverting(self):
        #print(self.input_files)
        self.output_text.clear()
            
        if self.input_files == []:
            self.status_label.setText("Choose some video to convert, please.")
            return
        if not os.path.isdir(self.output_folder):
            self.status_label.setText("Choose an output folder, please.")
            return
        line = 0
        for file in self.input_files:
            format = subprocess.getoutput("ffprobe -loglevel error -select_streams v -show_entries stream=codec_name -of default=nw=1:nk=1 "+file)
            if  format != "h264":
                #print("%s is %s encoded. It is not a valid h264 video. " % (file, format))
                self.output_text.append("ERROR: %s is %s encoded. It is not a valid h264 video." %(file, format))
                return
            else:
                #print("Format is h264! Ok to decode.")
                pass
            filename = os.path.basename(file)
            #print(filename)
            output_filename = filename.replace(".MP4", ".mov").replace(".mp4", ".mov")
            self.status_label.setText("Converting: " + filename)

            cmd = 'ffpb '+self.proc_code[self.proc_selected]+' -i '+file+' -c:v dnxhd -profile:v '+self.quality_code[self.quality_selected]+' -f mov '+self.output_folder+'/'+output_filename
            #print(cmd)
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                encoding='utf-8',
                errors='replace'
            )

            while True:
                realtime_output = self.process.stdout.readline()

                if realtime_output == '' and self.process.poll() is not None:
                    break

                if realtime_output:
                    try:
                        perc = int(realtime_output.strip()[14:17].strip())
                    except ValueError:
                        perc = 0
                    #print(perc, flush=True)
                    self.converting_progress.setValue(perc)

            self.output_text.append(filename)
            cursor = self.input_text.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor.select(QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()
            self.input_text.setTextCursor(cursor)

        self.status_label.setText("Job Done!")
        self.input_files = {}

    def proc_button_clicked(self, id):
        #print("Cliccato: ", id)
        self.proc_selected = id
        self.refresh_settings_label()

    def quality_button_clicked(self, id):
        #print("Cliccato: ", id)
        self.quality_selected = id
        self.refresh_settings_label()

    def refresh_settings_label(self):
        self.settings_label.setText("Selected Processor: %s - quality: %s" % (self.proc_text[self.proc_selected], self.quality_text[self.quality_selected]))    



    def initUI(self):
        self.setMaximumSize(720,860)
        # MENU:
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)
        
        fileMenu.addAction(exitAct)

        # STATUS BAR:
        self.statusBar().showMessage('Ciao!')

        # BODY:
        main_frame = QFrame()
        main_vbox = QVBoxLayout()
        #main_vbox.addStretch(1)

        input_button = QPushButton("Add Video to queue")
        input_button.setStatusTip("Click to select one or more videos to convert.")
        input_button.clicked.connect(self.selectInputFile)
        self.input_files = []
        main_vbox.addWidget(input_button)

        input_hbox = QHBoxLayout()
        input_label = QLabel("Input queue:")
        self.input_text = QTextEdit()
        input_hbox.addWidget(input_label)
        input_hbox.addWidget(self.input_text)
        main_vbox.addLayout(input_hbox)

        folder_button = QPushButton("Select Output Folder")
        folder_button.setStatusTip("Click to select the folder you want your convertions to be saved to.")
        folder_button.clicked.connect(self.selectOutputFolder)
        self.output_folder = ""
        main_vbox.addWidget(folder_button)

        folder_hbox = QHBoxLayout()
        folder_label = QLabel("Output Folder:")
        self.folder_text = QLineEdit()
        folder_hbox.addWidget(folder_label)
        folder_hbox.addWidget(self.folder_text)
        main_vbox.addLayout(folder_hbox)

        proc_hbox = QHBoxLayout()
        proc_button_group = QButtonGroup(self)
        proc_button_group.setExclusive(True)
        proc_button_group.buttonClicked[int].connect(self.proc_button_clicked)
        self.proc_text = ["CPU", "GPU"]
        self.proc_code = ["", "-c:v h264_cuvid"]
        cpu_button = QPushButton(self)
        cpu_button.setText("CPU")
        cpu_button.setStatusTip("Click to select CPU encoding.")
        cpu_button.setCheckable(True)
        cpu_button.setChecked(True)
        self.proc_selected = 0
        gpu_button = QPushButton(self)
        gpu_button.setText("GPU")
        gpu_button.setStatusTip("Click to select GPU encoding.")
        gpu_button.setCheckable(True)
        proc_button_group.addButton(cpu_button, 0)
        proc_button_group.addButton(gpu_button, 1)
        proc_hbox.addWidget(cpu_button)
        proc_hbox.addWidget(gpu_button)
        main_vbox.addLayout(proc_hbox)

        quality_hbox = QHBoxLayout()
        quality_button_group = QButtonGroup(self)
        quality_button_group.setExclusive(True)
        quality_button_group.buttonClicked[int].connect(self.quality_button_clicked)
        self.quality_text = ["LB", "SQ", "HQ"]
        self.quality_code = ["dnxhr_lb", "dnxhr_sq", "dnxhr_hq"]
        lb_button = QPushButton(self)
        lb_button.setText("LB")
        lb_button.setStatusTip("Click to select LB 180Mb/s quality.")
        lb_button.setCheckable(True)
        lb_button.setChecked(True)
        self.quality_selected = 0
        sq_button = QPushButton(self)
        sq_button.setText("SQ")
        sq_button.setStatusTip("Click to select SQ 577Mb/s quality.")
        sq_button.setCheckable(True)
        hq_button = QPushButton(self)
        hq_button.setText("HQ")
        hq_button.setStatusTip("Click to select HQ 873Mb/s quality.")
        hq_button.setCheckable(True)
        quality_button_group.addButton(lb_button, 0)
        quality_button_group.addButton(sq_button, 1)
        quality_button_group.addButton(hq_button, 2)
        quality_hbox.addWidget(lb_button)
        quality_hbox.addWidget(sq_button)
        quality_hbox.addWidget(hq_button)
        main_vbox.addLayout(quality_hbox)

        self.settings_label = QLabel()
        self.refresh_settings_label()
        main_vbox.addWidget(self.settings_label)

        start_stop_hbox = QHBoxLayout()
        start_button = QPushButton("Start Converting")
        start_button.setStatusTip("Click to start convertion. Videos are converted one after the other.")
        start_button.clicked.connect(self.startConverting)
        # Add a STOP button here..
        start_stop_hbox.addWidget(start_button)
        #start_stop_hbox.addWidget(stop_button)
        main_vbox.addLayout(start_stop_hbox)

        self.status_label = QLabel("Ready.")
        self.converting_progress = QProgressBar()
        self.converting_progress.setValue(0)
        main_vbox.addWidget(self.status_label)
        main_vbox.addWidget(self.converting_progress)

        output_hbox = QHBoxLayout()
        output_label = QLabel("Output:")
        self.output_text = QTextEdit()
        output_hbox.addWidget(output_label)
        output_hbox.addWidget(self.output_text)
        main_vbox.addLayout(output_hbox)

        main_frame.setLayout(main_vbox)
        self.setCentralWidget(main_frame)

        self.setWindowTitle('DJI 4K Video Converter - ( h264-MP4 -> DNxHR-MOV )')
        self.show()

def main():

    app = QApplication(sys.argv)
    App = djivc()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
