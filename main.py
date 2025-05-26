import pygame
from player import Player
from tile import Tile
from map_loader import load_map, check_collision

# 초기화
pygame.init()

# 픽셀 게임 해상도
screen_width, screen_height = 1024, 1024
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)



# FPS 설정
clock = pygame.time.Clock()

# 현재 맵 인덱스
current_map = 0
background, tiles, tile_group, collision_rects, player_start_pos, next_map_rects, map_w, map_h = load_map(current_map)
player = Player(*player_start_pos)
# print("플레이어 시작 위치:", player_start_pos) # 디버그용


# 메인 루프 시작
running = True

while running:
    dt = clock.tick(144) / 1000
    pygame.display.set_caption(f"FPS: {clock.get_fps():.1f}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            print(f"창 크기 변경됨: {screen_width}x{screen_height}")

    keys = pygame.key.get_pressed()
    player.update(keys, dt, collision_rects)

    # 맵 전환 충돌 감지
    for trigger in next_map_rects:
        if player.rect.colliderect(trigger["rect"]):
            if trigger["name"] in ["NextMap", "PrevMap"]:
                target = trigger["target"]
                if target.startswith("map"):
                    new_map_index = int(target[3:]) - 1
                    if new_map_index == current_map:
                        continue  # 이미 그 맵이면 스킵

                    current_map = new_map_index
                    background, tiles, tile_group, collision_rects, player_start_pos, next_map_rects, map_w, map_h = load_map(current_map)

                    if trigger["name"] == "NextMap":
                        player.pos_x = 0
                    elif trigger["name"] == "PrevMap":
                        player.pos_x = map_w - player.rect.width

                    player.rect.x = int(player.pos_x)
                    
                    break

    # 배경 그리기
    screen.blit(background, (0, 0))

    # 타일과 플레이어 그리기
    for tile in tiles:
        tile.draw(screen)
    player.draw(screen)
    
    pygame.display.flip()

pygame.quit()

