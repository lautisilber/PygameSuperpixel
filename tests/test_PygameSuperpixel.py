from PygameSuperpixel import Superpixel

def test_Superpixel():
    class MySuperpixel(Superpixel):
        def __init__(self, x: int, y: int, pixels_x: int, pixels_y: int=0, fps: int=15) -> None:
            from time import sleep
            super().__init__(x, y, pixels_x, pixels_y=pixels_y, fps=fps)
            self.draw_pixel(4, 3, (0, 255, 0), 1)
            self.draw_pixel(4, 3, (0, 0, 255), 0.75)
            self.draw_pixel(4, 3, (255, 0, 0), 0.5)
            self.draw_pixel(4, 3, (255, 255, 255), 0.25)
            self.update_screen()
            sleep(1)
            self.quit_pygame()

        def loop(self):
            print('loop')
            #return super().loop()

    mySuperpixel = MySuperpixel(827, 643, 10)