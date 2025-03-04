from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QImage
import pygame

# Embed Pygame onto PyQt6's QWidget
class PygameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lyrics_screen = pygame.Surface((600, 400))
        pygame.init() # Initialize pygame
        pygame.font.init()  # Initialize font before using

    def paintEvent(self, event):
        painter = QPainter(self)
        image = QImage(
            self.lyrics_screen.get_buffer(), 
            600, 400, 
            QImage.Format.Format_RGB32
        )
        painter.drawImage(0, 0, image)
    
    # Pygame の Surface に歌詞を描画
    def render_lyrics(self, screen, lyrics):
        font = pygame.font.Font(None, 36)
        # screen.fill((0, 0, 0))  # 背景を黒に
        text_surface = font.render(str(lyrics), True, (0, 0, 0))  # 白い文字
        screen.blit(text_surface, (50, 50))
        self.update()  # ここで PyQt の更新を要求


    def update_lyrics(self, lyrics):
        """歌詞を描画して更新"""
        self.render_lyrics(self.lyrics_screen, lyrics)
        self.update()
        
