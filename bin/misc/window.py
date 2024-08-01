import pygame
from typing import final

# TODO: Zaimplementować mechanikę z wyświetlaniem okna z danymi na prawym boku ekranu

class Window(pygame.Surface):

    def __init__(self, abs_x: int, abs_y: int, w: int, h: int, **data) -> None:
        super().__init__((w, h))

        self.__font_color: final[tuple[int, int, int]] = (255, 255, 255)

        self.width: final[int] = w
        self.height: final[int] = h
        self.abs_x: int = abs_x
        self.abs_y: int = abs_y
        self.data: dict = data

        self.__font_head = pygame.font.SysFont('Arial', 28, True)
        self.__font_body = pygame.font.SysFont('Arial', 19, False)


    def __attempt_access(self, key: str):
        if key not in list(self.data.keys()):
            return '<unknown>'
        
        return self.data[key]
    
    def update_data(self) -> None:
        self.__header = self.__font_head.render(self.__attempt_access('name'), True, self.__font_color)

        self.__body: str = ""

        for key in self.data.keys()[1:]:
            self.__body += f"{key}: {self.__attempt_access(key)}\n"
        
        self.__body = self.__font_body.render(self.__body, True, self.__font_color)
    
    def update(self) -> None:
        self.fill((30, 30, 30, 255))

        self.blit(self.__header, ((self.width - self.__header.get_width()) // 4), 8)
        self.blit(self.__body, ((8, self.__header.get_height() + 16)))