import pygame
import random
import math
pygame.init()

class DrawInformation:
    Black = 0,0,0
    White = 255,255,255
    Green = 0, 255, 0
    Red = 255, 0, 0
    Grey = 128, 128, 128
    BackgroundColor = White

    Gradients = [
        Grey,
        (160,160,160),
        (192,192,192),
        (128,128,128)
    ]
    Font = pygame.font.SysFont('comicsans', 20)
    large_Font = pygame.font.SysFont('comicsans', 30)
    Side_Pad = 100
    Top_Pad = 150

    def __init__ (self,width,height,lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)
    
    def set_list (self,lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_Width = round((self.width - self.Side_Pad) / len(lst))
        self.block_Height = math.floor(self.height - self.Top_Pad) / (self.max_val - self.min_val)
        self.start_x = self.Side_Pad // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BackgroundColor)

    title = draw_info.large_Font.render((f"{algo_name} - {'Ascending' if ascending else 'Descending'}"), 1, draw_info.Green)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))
    
    controls = draw_info.Font.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.Black)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 35))

    sorting = draw_info.Font.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.Black)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 65))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst
    
    if clear_bg:
        clear_rect = (draw_info.Side_Pad//2, draw_info.Top_Pad, draw_info.width - draw_info.Side_Pad, draw_info.height - draw_info.Top_Pad)

        pygame.draw.rect(draw_info.window, draw_info.BackgroundColor, clear_rect)
    
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_Width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_Height

        color = draw_info.Gradients[i % 3] 

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_Width, draw_info.height))
    if clear_bg:
        pygame.display.update()

def generate_starting_list (n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
        
    return lst
def bubble_sort (draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst)- 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.Green, j + 1: draw_info.Red}, True)
                yield True
    return lst

def insertion_sort (draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            decending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not decending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.Green, i: draw_info.Red}, True)
            yield True

    return lst

def main():
    run = True 
    
    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list (n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    clock = pygame.time.Clock()
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(100)
        
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False 
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list (n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"


    pygame.quit()

if __name__ == "__main__":
    main()
