try:
    import pygame
except:
    raise Exception('Pygame is not installed! Run \'pip install pygame\'')
try:
    import numpy as np
except:
    raise Exception('Numpy is not installed! Run \'pip install numpy\'')

from typing import Tuple
from abc import ABCMeta, abstractmethod

Colour = Tuple[int, int, int]

class Superpixel(metaclass=ABCMeta):
    def __init__(self, x: int, y: int, pixels_x: int, pixels_y: int=0, fps: int=30) -> None:
        '''
            Pygame wrapper that allows easy use of pygame to create graphical grids of pixels. Each square
            in the grid is a 'superpixel'. It should be inhereted by a class and the method 'loop()' needs
            to be implemented by the child class. The loop is initiated by callong the begin() method.
            Superpixels can be drawn by calling draw_pixel()

            :param x: width in pixels of the window
            :param y: height in pixels of the window
            :param pixels_x: how many superpixels per row
            :param pixels_y: how many superpixels per column (if 0 it means that superpixels are squared)
            :param fps: is the fps cap
        '''

        # bad input checking
        if x < 0 or y < 0 or pixels_x < 0 or pixels_y < 0:
            msg = 'Argument '
            if x <= 0:
                msg + f'x is {x}. It should be grater or equal to 1'
            elif y <= 0:
                msg + f'y is {y}. It should be grater or equal to 1'
            elif pixels_x <= 0:
                msg + f'pixels_x is {pixels_x}. It should be grater or equal to 1'
            elif pixels_y < 0:
                msg + f'pixels_y is {pixels_y}. It should be grater or equal to 0 (0 is equal to pixels_x)'
            raise Exception(msg)
        
        #self.buffer = np.array((x, y, 3), dtype=np.uint8) # pixel buffer

        #window title
        self.window_title = 'Superpixel'

        # size in pixels of each superpixel
        square_x_size = x // pixels_x
        square_y_size = x // pixels_x
        if pixels_y:
            square_y_size = y // pixels_y
        self.square_size = (square_x_size, square_y_size) # width and height of each 'superpixel'

        # create grid and assign to each grid coordinate a pixel space coordinate
        squares_in_x = x // self.square_size[0]
        squares_in_y = y // self.square_size[1]
        x_poss = [p*self.square_size[0] for p in range(squares_in_x)]
        y_poss = [p*self.square_size[1] for p in range(squares_in_y)]
        self.square_pos = np.zeros((squares_in_x, squares_in_y, 2), dtype=np.uint16) # pixel position for 'superpixels'. it creates a grid with square size equal to a superpixel and for a position in the grid it return the pixel position
        for xi, xpos in enumerate(x_poss):
            for yi, ypos in enumerate(y_poss):
                self.square_pos[xi, yi] = (xpos, ypos)
        self.superpixel_grid_shape = np.array((squares_in_x, squares_in_y))

        # pygame init
        self.fps = fps
        self.running = False
        pygame.init()
        self.screen = pygame.display.set_mode((x, y))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.window_title)

    def get_grid_shape(self):
        '''
            :return: shape of the grid of superpixels
        '''
        return self.superpixel_grid_shape

    def draw_pixel(self, x: int, y: int, colour: Colour, size: float=1) -> None: #draws a superpixel of colour colour and position (x, y)
        '''
            Draw a superpixel

            :param x: x position in superpixel grid
            :param y: y position in superpixel grid
            :param colour: (r, g, b) tuple with rgb pixel colour values
            :param size: float between 0 - 1 that determines the percentage of the grid square the superpixel will fill
        '''

        rect = pygame.Rect(self.square_pos[x, y][0], self.square_pos[x, y][1], self.square_size[0], self.square_size[1])
        if size != 1:
            size = np.interp(np.clip(size, 0, 1), (0, 1), (-self.square_size[0], 0))
            rect.inflate_ip(size, size)
        pygame.draw.rect(self.screen, colour, rect)

    def draw_region(self, up_left: Tuple[int, int], width_height: Tuple[int, int], colour: Colour, size: float=1) -> None:
        '''
            Draw a rectangular region that fits in multiple grid squares

            :param up_left: (x, y) grid coordinates of up left corner
            :param width_height: (x, y) width and height in superpixels the region will occupy
            :param colour: (r, g, b) tuple with rgb pixel colour values
            :param size: float between 0 - 1 that determines the percentage of the space the region will fill
        '''

        rect = pygame.Rect(self.square_pos[up_left[0], up_left[1]][0], self.square_pos[up_left[0], up_left[1]][1], width_height[0]*self.square_size[0], width_height[1]*self.square_size[1])
        if size != 1:
            size = np.interp(np.clip(size, 0, 1), (0, 1), (-self.square_size[0], 0))
            rect.inflate_ip(size, size)
        pygame.draw.rect(self.screen, colour, rect)

    def fill(self, colour: Colour=(0, 0, 0)):
        '''
            Fills entire screen with one colour

            :param colour: (r, g, b) tuple with rgb pixel colour values
        '''
        self.screen.fill(colour)

    def get_events(self):
        '''
            :return: pygame.eventsl list
        '''
        return pygame.event.get()

    def update_screen(self):
        '''
            Manually update the screen
        '''
        pygame.display.update()

    def quit_pygame(self):
        '''
            Manually quit pygame
        '''
        pygame.quit()

    def set_window_title(self, show_fps=True):
        if show_fps:
            pygame.display.set_caption(self.window_title + f' - {self.clock.get_fps():.{2}f}')
        else:
            pygame.display.set_caption(self.window_title)

    def begin(self, end_and_quit=True) -> None:
        '''
            Begins main loop at the set fps rate. Calls the implemented loop() method every frame and
            the the screen is refreshed. The loop is closed if the window close button is pressed. If param end_and_quit
            is True, pygame is also quit. If the internal variable self.running is set to false, the loop is also broken
        '''
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.loop()

            self.set_window_title()
            self.clock.tick(self.fps)
            pygame.display.update()

        if end_and_quit:
            pygame.quit()

    @abstractmethod
    def loop(self):
        ''' implement in child class '''
        pass


if __name__ == '__main__':
    class MyClass(Superpixel):
        def __init__(self, x: int, y: int, pixels_x: int, pixels_y: int=0, fps: int=15) -> None:
            super().__init__(x, y, pixels_x, pixels_y=pixels_y, fps=fps)
            self.draw_pixel(3, 3, (0, 255, 0), 1)
            self.draw_pixel(3, 3, (0, 0, 255), 0.75)
            self.draw_pixel(3, 3, (255, 0, 0), 0.5)
            self.draw_pixel(3, 3, (255, 255, 255), 0.25)

            self.draw_region((5, 4), (3, 2), (255, 0, 255))
            self.draw_region((5, 4), (3, 2), (0, 255, 255), 0.8)
            self.draw_pixel(5, 4, (255, 255, 255), 0.65)
            self.draw_pixel(6, 4, (255, 255, 255), 0.65)
            self.draw_pixel(7, 4, (255, 255, 255), 0.65)
            self.draw_pixel(5, 5, (255, 255, 255), 0.65)
            self.draw_pixel(6, 5, (255, 255, 255), 0.65)
            self.draw_pixel(7, 5, (255, 255, 255), 0.65)
            

        def loop(self):
            pass
            #return super().loop()

    g = MyClass(827, 643, 10)
    g.begin()