from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QTimer, QObject, pyqtSlot
import json
import sys # - deal with command line argument(sys.argv)。 Terminate program with sys.exit().
import os
from src.spotify import get_current_playback_time


# Send data from Python to JavaScript
class LyricsBridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lyrics = []

    @pyqtSlot(str)
    # Method that can be called from JavaScript
    def set_lyrics(self, lyrics_json):
        print("Received lyrics from JS:", lyrics_json)

    @pyqtSlot(result=str)
    # Pass lyric data to JavaScript
    def get_lyrics(self):
        lyrics_json = json.dumps(self.lyrics)
        return lyrics_json


# Sync displaying liric with playing with spotify
class LyricsSync(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Lyrics Sync")
        self.setGeometry(100, 100, 600, 400)

        # WebEngineView config
        self.browser = QWebEngineView(self)
        self.channel = QWebChannel()
        self.bridge = LyricsBridge()
        self.channel.registerObject("lyricsBridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)

        # UI layout
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        # load HTML
        self.browser.setHtml(self.generate_html())

        # full path to `time_after_time.lrc`
        lrc_file_path = os.path.join(os.path.dirname(__file__), "assets", "time_after_time.lrc")

        # load LRC file
        self.bridge.lyrics = [line for line in self.load_lrc(lrc_file_path) if line["time"] is not None]
        self.current_index = 0  # current lyric index

        # reload each 1 sec
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_lyrics)
        self.timer.start(1000)

    # HTML displayed in QWebEngineView 
    def generate_html(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <style>
                body { background-color: black; color: white; font-size: 20px; padding: 20px; }
                #lyrics { transition: transform 0.5s ease-in-out; }
                .highlight { color: yellow; font-weight: bold; }
            </style>
            <script>
                console.log("Script Loaded");
                var lyrics = [];
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    console.log("QWebChannel initialized");
                    channel.objects.lyricsBridge.get_lyrics().then(function(lyricsJson) {
                        console.log("Received Lyrics:", lyricsJson);
                        lyrics = JSON.parse(lyricsJson);  // ✅ Promise の結果を受け取ってパース
                        updateLyrics();
                    }).catch(function(error) {
                        console.error("Error fetching lyrics:", error);
                    });
                });

                function updateLyrics() {
                    console.log("Updating lyrics in HTML");  // 🔍 デバッグ出力
                    let html = "";
                    lyrics.forEach((line, index) => {
                        html += `<p id="line-${index}">${line.text}</p>`;
                    });
                    document.getElementById("lyrics").innerHTML = html;
                }

                function scrollToLine(index) {
                    let element = document.getElementById("line-" + index);
                    if (element) {
                        window.scrollTo({ top: element.offsetTop - 100, behavior: 'smooth' });
                        element.classList.add("highlight");
                    }
                }
            </script>
        </head>
        <body>
            <div id="lyrics"></div>
        </body>
        </html>
        """

    # load lrc file
    # Create timestamp and lyric list
    def load_lrc(self, file_path):
        lyrics = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line.startswith("[") or ":" not in line:
                    continue  # skip metadata

                parts = line.split("]", 1)
                if len(parts) < 2:
                    continue  # skip incorrect data

                timestamp = parts[0][1:]  # [00:14.59] → 00:14.59
                lyrics_text = parts[1].strip()

                # parce time data
                try:
                    minutes, seconds = map(float, timestamp.split(":"))
                    time_in_seconds = minutes * 60 + seconds
                    lyrics.append({"time": time_in_seconds, "text": lyrics_text})
                except (ValueError, IndexError):
                    continue  # skip incorrect time data

        return lyrics


    # load current timestamp from Spotify API
    def get_spotify_playback_time(self):
        return 90  # example：90secs #TODO example data


    def find_next_lyrics_index(self):
        current_time = get_current_playback_time()
        # current_time = self.get_spotify_playback_time()
        print('current_time',current_time)

        for i, line in enumerate(self.bridge.lyrics):
            time_value = line.get("time")
            if time_value is not None and time_value > current_time:
                return i

        return len(self.bridge.lyrics) - 1


    # Highlight lyric aligning Spotify's timestamp
    def update_lyrics(self):
        index = self.find_next_lyrics_index()
        print(f"Scrolling to line {index}")  # デバッグ用
        self.browser.page().runJavaScript(f"scrollToLine({index})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LyricsSync()
    window.show()
    app.exec()
