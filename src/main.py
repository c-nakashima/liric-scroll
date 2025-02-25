import pygame
import time
from lrc_parser import load_lrc  # 歌詞の読み込み関数
from spotify import get_current_track, get_current_playback_time, get_current_track  # Spotifyの現在の曲を取得
import os


# == Getting Lyrics ====================
# -- Gettig the base directry
# `main.py` のあるディレクトリを取得
base_dir = os.path.dirname(os.path.abspath(__file__))
# assets フォルダのLRCファイルを指定
lrc_file_path = os.path.join(base_dir, "assets", "shape_of_you.lrc")
# load title, artist, lyrics, timestamp
title, artist, lyrics = load_lrc(lrc_file_path)

# Pygame の初期化
# 画面設定
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 36)  # フォントサイズ36
clock = pygame.time.Clock()

# 背景色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 歌詞のスクロール用変数
current_line = 0
start_time = time.time()  # 再生開始時間

running = True
while running:
    screen.fill((0, 0, 0))  # 背景を黒にする
    
    # 🎵 **Spotifyの現在の再生時間を取得**
    current_time = get_current_playback_time()
    
    if current_time is not None:
        # 🎵 **現在の時間に一番近いインデックスを取得**
        current_index = 0
        for i, (timestamp, text, ltype) in enumerate(lyrics):
            if timestamp > current_time - 1.8:  # ⏳ **2秒前に歌詞を表示**
                current_index = max(0, i)  # 少し前の行を選択
                break

        # 🎵 **最初の歌詞が始まるまでは、すべてグレーで表示**
        if current_index == 0 and current_time < lyrics[0][0]:
            display_lyrics = lyrics[:4]  # 🎶 最初の4行を表示
        else:
            display_lyrics = lyrics[max(0, current_index - 2) : current_index + 4]  # 📜 前後2行 + 現在の行

        # 🎵 **画面に表示**
        y_pos = 200  # 最初の行のY座標
        for i, (_, text, ltype) in enumerate(display_lyrics):
            # 🎶 **最初の歌詞が始まるまで白**
            if current_index == 0:
                color = (255, 255, 255)  # 🔥 すべて白
            elif i == 2:  # 🔥 **現在の歌詞**
                color = (255, 255, 255)  # 白
            elif ltype == "chord":  # 🎸 **コード**
                color = (100, 200, 255)  # 水色
            else:  # 🔘 **前後の歌詞**
                color = (150, 150, 150)  # グレー

            text_surface = font.render(text, True, color)
            screen.blit(text_surface, (100, y_pos))
            y_pos += 50  # 50ピクセル下にずらす

    # Pygameイベント処理
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False

    pygame.display.flip()  # 画面を更新
    clock.tick(30)  # 30FPS
