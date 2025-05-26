import pygame
from player import Player
from tile import Tile
from map_loader import load_map

# 초기화
pygame.init() 
screen = pygame.display.set_mode((1280,1080)) # 1280x1080 크기의 창 생성
clock = pygame.time.Clock() # FPS를 조절하기 위한 Clock 객체 생성

# 배경 이미지
background = pygame.image.load("assets/background/nightCastle.png").convert()
background = pygame.transform.scale(background, (1280, 1080))

# 플레이어 100,100 에 생성
player = Player(100,800)


# 현재 맵 인덱스
current_map = 0
background, tiles, tile_group = load_map(current_map)



# 메인 루프 시작
running = True
while running:
    # FPS 설정 (초 단위 delta time)
    # dt를 설정하여 144, 60 프레임 등 게임에서의 속도는 일정하게 유지
    dt = clock.tick(144) / 1000

    pygame.display.set_caption(f"FPS: {clock.get_fps():.1f}")


    # 닫기 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() # 현재 눌린 키 상태들을 가져온다

    # Player 바닥 충돌 감지용
    ground_rects = [tile.rect for tile in tiles]
    player.update(keys, dt, tile_group)
   
    screen.blit(background, (0, 0)) # 배경 이미지 blit

    # 타일 화면에 그리기
    for tile in tiles:
        tile.draw(screen)
    
    player.draw(screen) # 현재 위치에 플레이어를 그림   
    pygame.display.flip() # 버퍼를 교체해서 실제로 화면에 반영


pygame.quit() # pygame을 종료하고 리소스를 정리
