import pygame

height, width = 800, 600
win = pygame.display.set_mode((height, width))
pygame.display.set_caption("brick breaker")

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit
    quit()

if __name__ == "_main_":
    main()
# if __name__ == '__main__':
#     print_hi('PyCharm')
