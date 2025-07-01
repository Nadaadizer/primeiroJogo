import pygame
import pygame as pg

print('Start game!')
pg.init()
window = pg.display.set_mode(size=(600, 460))

print('End start game!')

print('Start loop!')
while True:
    # Check for all events
    for event in pg.event.get():
        if event.type == pg.quit():
            pg.quit()  # Close window
            quit()#End pygame
            print('Finishing loop!')
