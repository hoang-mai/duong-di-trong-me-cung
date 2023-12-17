import pygame
import sys
from constants import *
import classes
from ui.setup import *

def get_user_input(screen):
    input_box_width = pygame.Rect(300, 200, 140, 32)
    input_box_height = pygame.Rect(300, 250, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active_box = None
    text_width = ''
    text_height = ''
    instruction_text = "May` nhap. ho. bo. may` cai'"

    # Tạo font cho văn bản
    font = pygame.font.Font(None, 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_width.collidepoint(event.pos):
                    active_box = input_box_width
                    color = color_active
                elif input_box_height.collidepoint(event.pos):
                    active_box = input_box_height
                    color = color_active
                else:
                    active_box = None
                    color = color_inactive
            if event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_RETURN:
                        try:
                            width = int(text_width)
                            height = int(text_height)
                            return width, height
                        except ValueError:
                            print("Vui lòng nhập số nguyên hợp lệ.")
                            text_width = ''
                            text_height = ''
                    elif event.key == pygame.K_BACKSPACE:
                        if active_box == input_box_width:
                            text_width = text_width[:-1]
                        elif active_box == input_box_height:
                            text_height = text_height[:-1]
                    else:
                        char = event.unicode
                        if char.isdigit():
                            if active_box == input_box_width:
                                text_width += char
                            elif active_box == input_box_height:
                                text_height += char

        screen.fill(white)

        # Hiển thị hướng dẫn
        instruction_surface = font.render(instruction_text, True, (0, 0, 0))
        screen.blit(instruction_surface, (input_box_width.x, input_box_width.y - 30))

        # Vẽ ô text box cho chiều rộng
        txt_surface_width = font.render(text_width, True, color)
        width_width = max(200, txt_surface_width.get_width() + 10)
        input_box_width.w = width_width
        screen.blit(txt_surface_width, (input_box_width.x + 5, input_box_width.y + 5))
        pygame.draw.rect(screen, color, input_box_width, 2)

        # Vẽ ô text box cho chiều dài
        txt_surface_height = font.render(text_height, True, color)
        width_height = max(200, txt_surface_height.get_width() + 10)
        input_box_height.w = width_height
        screen.blit(txt_surface_height, (input_box_height.x + 5, input_box_height.y + 5))
        pygame.draw.rect(screen, color, input_box_height, 2)

        pygame.display.flip()

# Initialize pygame
pygame.init()

if __name__ == "__main__":
    # Initialize pygame screen
    screen = pygame.display.set_mode(size)

    # Nhận thông tin từ người dùng
    width, height = get_user_input(screen)

    # Tính toán kích thước của từng ô trong mê cung
    cell_size = min(screen.get_width() // width, screen.get_height() // height)

    # Tính toán lại kích thước mê cung
    maze_width = width * cell_size
    maze_height = height * cell_size

    # Điều chỉnh kích thước màn hình hiển thị mê cung
    screen = pygame.display.set_mode((maze_width, maze_height))

    # Khởi tạo mê cung với chiều dài và chiều rộng từ người dùng
    growingTree = classes.GrowingTree(classes.Grid(height, width, cell_size), "GREEN")

    margin = 5  # Số lượng pixel khoảng trắng giữa các ô

    # Các biến khác giữ nguyên
    show_text = False
    color_mode = False
    show_path = True
    start = False
    run = True

    clock = pygame.time.Clock()
    fps = 60

    while run:
        clock.tick(fps)
        frame_rate = int(clock.get_fps())
        pygame.display.set_caption(f"Maze Generator - FPS: {frame_rate}")

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

        screen.fill(black)

        if start:
            growingTree.Generate(screen, show_text, color_mode, show_path)
        else:
            PressEnter.Render(screen)

        pygame.display.flip()

    pygame.image.save(screen, "./images/path.png")
    pygame.quit()
