from PyQt6.QtCore import QDir, QUrl, Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication, QStyle, QVBoxLayout, QHBoxLayout, QSlider, QLabel)
import sys

from query import find_query_video

class VideoPlayer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("CS576 Final Project")

        self.media_player = QMediaPlayer()
        self.audio_player = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_player)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)

        video_widget = QVideoWidget()

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.slider_value_changed)

        self.duration_label = QLabel()
        self.duration_label.setText("xx:xx / xx:xx")
        self.duration_label.setFixedHeight(20)

        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.start_video)

        self.pause_button = QPushButton()
        self.pause_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        self.pause_button.clicked.connect(self.pause_video)

        self.reset_button = QPushButton()
        self.reset_button.setText("Reset to beginning")
        self.reset_button.clicked.connect(self.reset_video)

        self.reset_query_button = QPushButton()
        self.reset_query_button.setText("Reset to query")
        self.reset_query_button.clicked.connect(self.reset_query_video)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.reset_query_button)

        duration_layout = QHBoxLayout()
        duration_layout.addWidget(self.slider)
        duration_layout.addWidget(self.duration_label)

        layout = QVBoxLayout()
        layout.addWidget(video_widget)
        layout.addLayout(duration_layout)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        self.media_player.setVideoOutput(video_widget)

    def set_video_file(self, filename):
        file_path = QDir.currentPath()
        file_url = QUrl.fromLocalFile(file_path + "/" + filename)
        print(file_url)
        self.media_player.setSource(file_url)

    def set_query_position(self, query_position):
        self.query_position = query_position
        self.media_player.setPosition(query_position)
        self.slider.setValue(self.query_position)

    def start_video(self):
        self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def reset_video(self):
        self.media_player.setPosition(0)
        self.slider.setValue(0)

    def reset_query_video(self):
        self.media_player.setPosition(self.query_position)
        self.slider.setValue(self.query_position)

    def duration_changed(self, duration):
        self.duration = duration
        self.slider.setMinimum(0)
        self.slider.setMaximum(duration)

    def slider_value_changed(self, slider_value):
        self.media_player.setPosition(slider_value)

    def position_changed(self, position):
        duration_seconds = int(self.duration / 1000)

        duration_minutes = int(duration_seconds / 60)
        duration_seconds_text = duration_seconds % 60

        timestamp_seconds = int(position / 1000)
        timestamp_minutes = int(timestamp_seconds / 60)
        timestamp_seconds_text = timestamp_seconds % 60
        self.duration_label.setText(f"{timestamp_minutes:02d}:{timestamp_seconds_text:02d} / {duration_minutes:02d}:{duration_seconds_text:02d}")

if __name__ == "__main__":
    query_video_path = sys.argv[1]
    result = find_query_video(query_video_path)
    print(result)

    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.resize(640, 480)
    video_player.set_video_file(f"videos/{result['video_name']}")
    video_player.set_query_position(result['match_start_database'] // 30 * 1000)
    video_player.show()
    sys.exit(app.exec())
