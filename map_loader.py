import pygame
import json
from tile import Tile

def load_map_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def load_map(index):
    data = load_map_from_file(f"maps/map{index+1}.json")

    bg = pygame.image.load(f"assets/background/{data['background']}").convert()
    bg = pygame.transform.scale(bg, (1280, 1080))


    # 타일 이미지 로딩 및 배치
    tile_path = f"assets/tiles/{data['tile_image']}"
    tile_image = pygame.image.load(tile_path).convert_alpha()

    tile_surface = pygame.Surface((314, 122), pygame.SRCALPHA)
    tile_surface.blit(tile_image, (0, 0), pygame.Rect(438, 597, 314, 122))

    # 타일 리스트 및 그룹 생성
    tiles = []
    tile_group = pygame.sprite.Group()


    for x, y in data["tile_positions"]:
        tile = Tile(tile_surface, x, y)
        tiles.append(tile)
        tile_group.add(tile)

    return bg, tiles, tile_group
