from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QMessageBox, QFileDialog, QCheckBox
from PyQt5.QtGui import QIcon
import webbrowser
import sys
import youtube_dl
from ydl import mp3_options, no_options


class App(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setWindowTitle("youtube video downloader")
		self.setFixedSize(430, 70)
		self.setWindowIcon(QIcon("icon.png"))

		self.textbox = QLineEdit(self)
		self.textbox.move(20, 10)
		self.textbox.resize(400, 20)

		self.playlist_button = QPushButton("download!", self)
		self.playlist_button.move(20, 35)

		self.github_button = QPushButton("", self)
		self.github_button.setFixedSize(32, 32)
		self.github_button.setIcon(QIcon("GitHub-Mark-32px.png"))
		self.github_button.move(390, 35)

		self.mp3_checkbox = QCheckBox("download as mp3", self)
		self.mp3_checkbox.setFixedWidth(110)
		self.mp3_checkbox.move(150, 35)

		self.playlist_button.clicked.connect(self.on_download_button_click)
		self.github_button.clicked.connect(self.on_github_button_click)
		self.mp3_checkbox.stateChanged.connect(self.on_mp3_checkbox_change)

		self.download_options = no_options

		self.show()

	@pyqtSlot(name="download_slot")
	def on_download_button_click(self):
		link = self.textbox.text()

		path = QFileDialog.getExistingDirectory(self, "where would you like to download the file(s)? - a folder will NOT be created", None)
		if path == "":
			exit()
		else:
			self.download_options["outtmpl"] = path + "\%(title)s.%(ext)s"

		with youtube_dl.YoutubeDL(self.download_options) as ydl:
			try:
				self.setWindowTitle("download in progress...")
				ydl.download([link])
			except youtube_dl.utils.DownloadError or youtube_dl.utils.ExtractorError:
				message_box = QMessageBox()
				message_box.setWindowTitle("error")
				message_box.setIcon(QMessageBox.Information)
				message_box.setText("Download failed. This can happen to due to a few reasons:\n1- The link is invalid\n2- There is a problem with your internet connection\n3- ffmpeg is not installed (if you wanted the file as mp3)")
				message_box.exec_()

				self.setWindowTitle("youtube video downloader")
			else:
				self.textbox.setText("")

				msg_box = QMessageBox()
				msg_box.setWindowTitle("success!")
				msg_box.setIcon(QMessageBox.Information)
				msg_box.setText("successfully downloaded the file(s)!")
				msg_box.exec_()

				self.setWindowTitle("youtube video downloader")

	@pyqtSlot(name="github_slot")
	def on_github_button_click(self):
		webbrowser.open("https://github.com/emredesu/youtube_video_downloader")

	@pyqtSlot(name="mp3_checkbox")
	def on_mp3_checkbox_change(self):
		if self.download_options == no_options:
			self.download_options = mp3_options
		elif self.download_options == mp3_options:
			self.download_options = no_options


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = App()
	sys.exit(app.exec())
