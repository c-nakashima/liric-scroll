from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget
from PyQt6.QtCore import QTimer
from src.pygame_widget import PygameWidget
import os
from src.lrc_parser import load_lrc

# 🎵 **PyQt6 + Pygame の統合**
class LyricScrollApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LyricScroll")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # 🎵 Pygame 埋め込みウィジェット
        self.pygame_widget = PygameWidget(self)
        layout.addWidget(self.pygame_widget)

        # 🎵 曲の選択リスト
        self.song_list = QListWidget()
        self.song_list.addItem("Time After Time")
        self.song_list.addItem("Other Song")
        self.song_list.itemClicked.connect(self.load_selected_song)
        layout.addWidget(self.song_list)

        # 🎵 再生ボタン
        self.play_button = QPushButton("Play")
        layout.addWidget(self.play_button)
        # 🎵 再生ボタンのクリック時に play_song() を呼び出す
        self.play_button.clicked.connect(self.play_song)

        # 🎵 歌詞更新用タイマー
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_lyrics)
        self.timer.start(30)

        self.setLayout(layout)

        # 🎵 初期の LRC ロード
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.lrc_file_path = os.path.join(base_dir, "assets", "time_after_time.lrc")
        self.lyrics = load_lrc(self.lrc_file_path)

        print("🎯 LyricScrollApp initialized")


    def load_selected_song(self, item):
        print("load_selected_song")
        # """選択した曲の LRC ファイルを読み込む"""
        song_name = item.text()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.lrc_file_path = os.path.join(base_dir, "assets", f"{song_name.lower().replace(' ', '_')}.lrc")
        self.lyrics = load_lrc(self.lrc_file_path)
    
    def play_song(self):
        # """曲の再生処理を開始"""
        print(f"🎶 {self.song_list.currentItem().text()} を再生開始")
        
        # 歌詞の再生を開始
        self.update_lyrics()

    def update_lyrics(self):
        # """歌詞を更新"""
        self.pygame_widget.update_lyrics(self.lyrics)
