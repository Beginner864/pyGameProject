import pygame
from player import Player
from tile import Tile
from map_loader import load_map, check_collision

pygame.init()

# 고정 논리 해상도
LOGICAL_WIDTH = 1024
LOGICAL_HEIGHT = 1024
game_surface = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))

# 초기 실제 화면 크기
screen_width = 1024
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

clock = pygame.time.Clock()

# 맵 로딩
current_map = 0
background, tiles, tile_group, collision_rects, player_start_pos, next_map_rects, map_w, map_h = load_map(current_map)
player = Player(*player_start_pos)

running = True
while running:
    dt = clock.tick(144) / 1000
    pygame.display.set_caption(f"FPS: {clock.get_fps():.1f}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    keys = pygame.key.get_pressed()
    player.update(keys, dt, collision_rects)

    # 화면 밖으로 나가지 않도록 제한
    if player.rect.left < 0:
        player.rect.left = 0
        player.pos_x = player.rect.x
    if player.rect.right > LOGICAL_WIDTH:
        player.rect.right = LOGICAL_WIDTH
        player.pos_x = player.rect.x
    if player.rect.top < 0:
        player.rect.top = 0
        player.pos_y = player.rect.y
    if player.rect.bottom > LOGICAL_HEIGHT:
        player.rect.bottom = LOGICAL_HEIGHT
        player.pos_y = player.rect.y

    # 맵 전환 감지
    for trigger in next_map_rects:
        if player.rect.colliderect(trigger["rect"]):
            if trigger["name"] in ["NextMap", "PrevMap"]:
                target = trigger["target"]
                if target.startswith("map"):
                    new_map_index = int(target[3:]) - 1
                    if new_map_index == current_map:
                        continue
                    current_map = new_map_index
                    player.bullets.empty() # 모든 총알 제거
                    background, tiles, tile_group, collision_rects, player_start_pos, next_map_rects, map_w, map_h = load_map(current_map)
                    if trigger["name"] == "NextMap":
                        player.pos_x = 0
                    elif trigger["name"] == "PrevMap":
                        player.pos_x = map_w - player.rect.width
                    player.rect.x = int(player.pos_x)
                    break

    # 모든 그리기는 game_surface에
    game_surface.fill((0, 0, 0))  # 화면을 지운다 (배경을 채운 후)
    game_surface.blit(background, (0, 0))
    for tile in tiles:
        tile.draw(game_surface)
    player.draw(game_surface)

    # === 레터박스 방식 비율 유지 출력 ===
    scale_x = screen_width / LOGICAL_WIDTH
    scale_y = screen_height / LOGICAL_HEIGHT
    scale = min(scale_x, scale_y)

    scaled_width = int(LOGICAL_WIDTH * scale)
    scaled_height = int(LOGICAL_HEIGHT * scale)

    offset_x = (screen_width - scaled_width) // 2
    offset_y = (screen_height - scaled_height) // 2

    # 검은 배경 + 중앙 배치
    screen.fill((0, 0, 0))
    scaled_surface = pygame.transform.scale(game_surface, (scaled_width, scaled_height))
    screen.blit(scaled_surface, (offset_x, offset_y))

    pygame.display.flip()

pygame.quit()

