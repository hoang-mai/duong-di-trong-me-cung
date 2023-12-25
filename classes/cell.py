import sys
import pygame
from ui.colors import *
from classes.heuristic import Heuristic
from constants import *
import heapq
pygame.font.init()
text_font = pygame.font.SysFont("Arial", cell_size//3)
offset = 0


def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


class Cell:
    def __init__(self, x, y, size=40):
        self.x = x
        self.y = y

        self.cost = 0
        self.isgoalNode = False
        self.isStartingNode = False
        self.isCurrent = False
        self.isPath = False
        self.show_path = False
        self.highlight = white

        self.g = 0  # Chi phí từ điểm xuất phát đến nút hiện tại
        self.h = 0  # Chi phí ước lượng từ nút hiện tại đến điểm đích
        self.f = 0  # Tổng chi phí (f = g + h)
        self.parent=None

        self.show_highlight = False
        self.size = size
        self.color= white
        self.wall_color= black
        self.wall_thickness = 4
        self.visited = False
        self.connections = []
        self.neighbours = []
        self.isAvailable = True
        # Walls -- neighbours
        self.North = None
        self.South = None
        self.East = None
        self.West = None

        self.textColor = (0, 0, 0)
        self.show_text = True

    def __lt__(self, other):
        # Cài đặt so sánh dựa trên giá trị f
        return self.f < other.f
    def astar(self,screen, end_node):

        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (self.f, self))

        while open_set:
            current_node = heapq.heappop(open_set)[1]
            if current_node == end_node:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = current_node.parent
                return path[::-1]

            closed_set.add(current_node)

            for neighbor in current_node.connections:
                if neighbor in closed_set:
                    continue
                neighbor.parent = current_node
                neighbor.g = current_node.g + 1
                neighbor.h = heuristic(neighbor,end_node)
                neighbor.f = neighbor.g + neighbor.h
                start_pos = ((current_node.x+0.5)*self.size, (current_node.y+0.5)*self.size)
                end_pos = ((neighbor.x+0.5)*self.size, (neighbor.y+0.5)*self.size)

                pygame.draw.line(screen, orange, start_pos,end_pos, 2)
                pygame.draw.circle(screen, orange, start_pos, self.size// 6)
                pygame.display.flip()
                clock = pygame.time.Clock()  # Khởi tạo đối tượng Clock

                drawing_speed = 100  # Số frames mỗi giây bạn muốn vẽ
                clock.tick(drawing_speed)
                if (neighbor.f, neighbor) not in open_set:
                    heapq.heappush(open_set, (neighbor.f, neighbor))

    def ucs(self,screen, end_node):
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (self.g, self))

        clock = pygame.time.Clock()

        while open_set:
            current_node = heapq.heappop(open_set)[1]

            if current_node == end_node:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = current_node.parent
                return path[::-1]

            closed_set.add(current_node)

            for neighbor in current_node.connections:
                if neighbor in closed_set:
                    continue
                tentative_g = current_node.g + 1
                start_pos = ((current_node.x+0.5)*self.size, (current_node.y+0.5)*self.size)
                end_pos = ((neighbor.x+0.5)*self.size, (neighbor.y+0.5)*self.size)

                pygame.draw.line(screen, orange, start_pos,end_pos, 2)
                pygame.draw.circle(screen, orange, start_pos, self.size// 6)
                pygame.display.flip()
                clock = pygame.time.Clock()  # Khởi tạo đối tượng Clock

                drawing_speed = 100  # Số frames mỗi giây bạn muốn vẽ
                clock.tick(drawing_speed)
                if (heuristic(neighbor, end_node), neighbor) not in open_set:
                    neighbor.parent = current_node
                    neighbor.g = tentative_g
                    heapq.heappush(open_set, (heuristic(neighbor, end_node), neighbor))

        return None
    def IsConneted(self, cell):
        if cell != None:
            if cell in self.connections and self in cell.connections:
                return True
            else:
                return False

    def Draw(self, screen, rows, cols):
        x = self.x * self.size
        y = self.y * self.size

        if not self.visited or not self.isAvailable:
            pygame.draw.rect(screen, black, [x, y, self.size-offset, self.size-offset])
        else:
            color = self.color
            if self.isStartingNode:
                color = yellow
            if self.isCurrent:
                color = white
            elif self.isgoalNode:
                color = blue
            pygame.draw.rect(screen, color, [x, y, self.size-offset, self.size-offset])

            if self.show_highlight:
                pygame.draw.rect(screen, self.highlight, [x, y, self.size-offset, self.size-offset])

        if self.North != None or self.y - 1 < 0:
            A = (x, y)
            B = (x + self.size, y)
            pygame.draw.line(screen, self.wall_color, A, B, self.wall_thickness)
        if self.South != None or self.y + 1 >= rows:
            A = (x, y + self.size)
            B = (x + self.size, y + self.size)
            pygame.draw.line(screen, self.wall_color, A, B, self.wall_thickness)
        if self.East != None or self.x + 1 >= cols:
            A = (x + self.size, y)
            B = (x + self.size, y + self.size)
            pygame.draw.line(screen, self.wall_color, A, B, self.wall_thickness)
        if self.West != None or self.x - 1 < 0:
            A = (x, y)
            B = (x, y + self.size)
            pygame.draw.line(screen, self.wall_color, A, B, self.wall_thickness)

        if self.show_text:
            text_surface = text_font.render(str(int(self.cost)), True, self.textColor)
            text_rect = text_surface.get_rect(center=(x + self.size//2, y + self.size/2))
            screen.blit(text_surface, text_rect)

    def __repr__(self):
        # DEBUG
        return f"({self.x}, {self.y}, {id(self)})"
