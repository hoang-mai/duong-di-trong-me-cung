import pygame
import sys
from constants import *
import classes
from ui.setup import *
def reset_maze():
    # Khai báo biến toàn cục để có thể thay đổi giá trị từ hàm
    global growingTree, start, show_path

    # Tạo một đối tượng lưới mới
    growingTree = classes.GrowingTree(classes.Grid(height, width, cell_size), "GREEN")

    # Đặt lại trạng thái bắt đầu và hiển thị đường
    start = False
    show_path = True
def get_user_input(screen):
    input_box_width = pygame.Rect(screen.get_width() // 2 - 70, screen.get_height() // 2 - 16, 140, 32)
    input_box_height = pygame.Rect(screen.get_width() // 2 - 70, screen.get_height() // 2 + 50, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active_box = None
    text_width = ''
    text_height = ''
    instruction_text = "Enter the number of cells of 1 edge"
    instruction_width = "Width"
    instruction_height = "Height"
    warning_message = ''
    font_size = 30
    font = pygame.font.Font(None, font_size)

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
                            if width <= 0 or height <= 0:
                                warning_message = "Sai roi nhe"
                            else:
                                return width, height
                        except ValueError:
                            warning_message = "Sai roi nhe"
                            text_width = ''
                            text_height = ''
                    elif event.key == pygame.K_BACKSPACE:
                        if active_box == input_box_width:
                            text_width = text_width[:-1]
                        elif active_box == input_box_height:
                            text_height = text_height[:-1]
                        warning_message = ''
                    elif event.key == pygame.K_TAB:
                        if active_box == input_box_width:
                            active_box = input_box_height
                            color = color_inactive
                        elif active_box == input_box_height:
                            active_box = input_box_width
                            color = color_inactive
                        warning_message = ''
                    else:
                        char = event.unicode
                        if char.isdigit():
                            if active_box == input_box_width:
                                text_width += char
                            elif active_box == input_box_height:
                                text_height += char
                        warning_message = ''

        screen.fill(white)

        # Hiển thị hướng dẫn
        instruction_surface = font.render(instruction_text, True, (0, 0, 0))
        screen.blit(instruction_surface, (screen.get_width() // 2 - instruction_surface.get_width() // 2, screen.get_height() // 2 - 60))

        instruction_surface_width = font.render(instruction_width, True, (0, 0, 0))
        screen.blit(instruction_surface_width, (screen.get_width() // 2 - 160, screen.get_height() // 2 - 30))

        instruction_surface_height = font.render(instruction_height, True, (0, 0, 0))
        screen.blit(instruction_surface_height, (screen.get_width() // 2 - 160, screen.get_height() // 2 + 26))

        # Hiển thị cảnh báo
        warning_surface = font.render(warning_message, True, (255, 0, 0))
        screen.blit(warning_surface, (screen.get_width() // 2 - warning_surface.get_width() // 2, screen.get_height() // 2 + 100))

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

    # lay dai ,rong
    width, height = get_user_input(screen)

    # resize cai me cung
    cell_size = min(screen.get_width() // width, screen.get_height() // height)
    maze_width = width * cell_size
    maze_height = height * cell_size

    # resize man hinh
    screen = pygame.display.set_mode((maze_width, maze_height))

    # ve me cung
    growingTree = classes.GrowingTree(classes.Grid(height, width, cell_size), "GREEN")

    margin = 5  # Số lượng pixel khoảng trắng giữa các ô

    show_text = False
    color_mode = False
    show_path = True
    start = False
    run = True

    clock = pygame.time.Clock()
    fps = 120


    def update_press_enter():
        current_width, current_height = pygame.display.get_surface().get_size()
        PressEnter.position = (current_width // 2, current_height // 2)
    while run:
        clock.tick(fps)
        frame_rate = int(clock.get_fps())
        pygame.display.set_caption(f"Maze Generator - FPS: {frame_rate}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_maze()
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

    pygame.image.save(screen, "./images/path.png")
    pygame.quit()
