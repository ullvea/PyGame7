import pygame
import os
import sys

size = WIDTH, HEIGHT = 501, 501
running = True
clock = pygame.time.Clock()

FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.tyle_type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, state):
        last_pos = self.rect.copy()
        if state == 'up' and self.rect.y - 55 >= 0:
            self.rect.y -= tile_height
        if state == 'down' and self.rect.y + 95 <= level_y * tile_height:
            self.rect.y += tile_height
        if state == 'right' and self.rect.x + 55 <= level_x * tile_height:
            self.rect.x += tile_width
        if state == 'left' and self.rect.x - 55 >= 0:
            self.rect.x -= tile_width
        for i in tiles_group:
            if i.rect.colliderect(self.rect) and i.tyle_type == 'wall':
                self.rect = last_pos


if __name__ == '__main__':
    try:
        new_map = input('Введите название желаемой карты либо напишите default для открытия стандартной карты: ')
        if new_map == 'default':
            new_map = 'map1.txt'
        player, level_x, level_y = generate_level(load_level(new_map))
    except Exception:
        print('Ошибка !')
    pygame.init()
    pygame.display.set_caption('Перемещение героя')
    screen = pygame.display.set_mode(size)
    running2 = True
    while running2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move('up')
                if event.key == pygame.K_DOWN:
                    player.move('down')
                if event.key == pygame.K_RIGHT:
                    player.move('right')
                if event.key == pygame.K_LEFT:
                    player.move('left')
        screen.fill((255, 255, 255))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
