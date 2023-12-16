import pygame
from constants import *
from ui.colors import *
import classes

from ui.setup import *
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

growingTree = classes.GrowingTree(classes.Grid(rows, cols, cell_size), "GREEN")


show_text = False
color_mode = False
show_path = False
start = False
run = True
while run:
    #screen.fill(black)
    # Set Caption and fps
    clock.tick(fps)
    frame_rate = int(clock.get_fps())
    pygame.display.set_caption(f"Maze Generator - FPS: {frame_rate}")

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_RETURN:
                start = not start
            elif event.key == pygame.K_h:
                show_text = not show_text
            elif event.key == pygame.K_SPACE:
                color_mode = not color_mode
            elif event.key == pygame.K_s:
                show_path = not show_path
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rightMouseClicked = True

    if start:
        growingTree.Generate(screen, show_text, color_mode, show_path)
    else:
        PressEnter.Render(screen)

    pygame.display.flip()

pygame.image.save(screen, "C:\\Users\\Administrator\\Desktop\\HUST\\AI\\duong-di-trong-me-cung\\images\\path.png")
pygame.quit()