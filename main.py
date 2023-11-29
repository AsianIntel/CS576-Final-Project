from PyQt6.QtCore import QDir, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication, QStyle, QVBoxLayout, QHBoxLayout)
import sys

from query import find_query_video

class VideoPlayer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("CS576 Final Project")

        self.media_player = QMediaPlayer()
        self.audio_player = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_player)

        video_widget = QVideoWidget()

        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.start_video)

        self.pause_button = QPushButton()
        self.pause_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        self.pause_button.clicked.connect(self.pause_video)

        self.reset_button = QPushButton()
        self.reset_button.setText("Reset")
        self.reset_button.clicked.connect(self.reset_video)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)

        layout = QVBoxLayout()
        layout.addWidget(video_widget)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        self.media_player.setVideoOutput(video_widget)

    def set_video_file(self, filename):
        file_path = QDir.currentPath()
        file_url = QUrl.fromLocalFile(file_path + "/" + filename)
        print(file_url)
        self.media_player.setSource(file_url)

    def set_video_position(self, position):
        self.media_player.setPosition(position)

    def start_video(self):
        self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def reset_video(self):
        self.media_player.setPosition(0)

if __name__ == "__main__":
    query_video_path = sys.argv[1]
    result = find_query_video(query_video_path)
    print(result)

    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.resize(640, 480)
    video_player.set_video_file(f"videos/{result['video_name']}")
    video_player.set_video_position(result['match_start_database'] * 1000)
    video_player.show()
    sys.exit(app.exec())
