import pygame
import pytmx
from tile import Tile

# 게임 기본 해상도 (픽셀 아트 기준)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360

# 맵 불러오기 함수
def load_map(index):
    # map1.tmx, map2.tmx ... 순서대로 로드
    tmx_data = pytmx.load_pygame(f"maps/map{index + 1}.tmx")

    # 전체 맵 해상도 계산
    map_pixel_width = tmx_data.width * tmx_data.tilewidth
    map_pixel_height = tmx_data.height * tmx_data.tileheight

    # 배경 Surface (기본 해상도 기준)
    bg = pygame.Surface((map_pixel_width, map_pixel_height))

    tile_group = pygame.sprite.Group()
    tiles = []
    collision_rects = []
    player_start_pos = (0, 0)
    next_map_rects = []

    # 타일 레이어 처리
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_img = tmx_data.get_tile_image_by_gid(gid)
                if tile_img:
                    px = x * tmx_data.tilewidth
                    py = y * tmx_data.tileheight

                    bg.blit(tile_img, (px, py))

                    tile = Tile(tile_img, px, py)
                    if layer.name.lower() in ["ground", "collision"]:
                        collision_rects.append(tile.rect)
                    else:
                        tile_group.add(tile)
                    tiles.append(tile)

    # 이미지 레이어 처리 (배경 이미지 자동 포함)
    for layer in tmx_data.layers:
        if hasattr(layer, 'image') and layer.image:
            bg.blit(layer.image, (0, 0))

    # 오브젝트 레이어 처리: 시작 위치 및 맵 전환
    for obj in tmx_data.objects:
        if obj.name == "PlayerStart":
            player_start_pos = (obj.x, obj.y)
        elif obj.name in ["NextMap", "PrevMap"]:
            next_map_rects.append({
                "name": obj.name,  # 예: "NextMap" or "PrevMap"
                "rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                "target": obj.properties.get("target", "")  # 예: "map2"
            })

    return bg, tiles, tile_group, collision_rects, player_start_pos, next_map_rects, map_pixel_width, map_pixel_height

# 충돌 감지 함수
def check_collision(rect, rect_list):
    for target in rect_list:
        if rect.colliderect(target):
            return True
    return False
