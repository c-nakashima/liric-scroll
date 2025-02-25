import re
import pygame

# LRCファイルを読み込む（コードも含める）
def load_lrc(file_path):
    lyrics = []
    title = None
    artist = None

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # 空白行の除去
            
            # タイトルとアーティスト情報を取得
            if line.startswith("[ti:"):
                title = line[4:-1]  # [ti: ] の部分を削除
                continue
            elif line.startswith("[ar:"):
                artist = line[4:-1]  # [ar: ] の部分を削除
                continue

            # LRCのフォーマット解析（タイムスタンプ付きの歌詞）
            match = re.match(r"\[(\d+):(\d+\.\d+)\](.*)", line)
            if match:
                minutes = int(match.group(1))
                seconds = float(match.group(2))
                text = match.group(3).strip()
                timestamp = minutes * 60 + seconds  # 秒単位

                # コードか歌詞を判定
                if text.startswith("(") and text.endswith(")"):
                    lyrics.append((timestamp, text, "chord"))  # コード
                else:
                    lyrics.append((timestamp, text, "lyric"))  # 歌詞

    print(f"Title: {title}, Artist: {artist}")
    return title, artist, lyrics

    