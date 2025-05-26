# Update -> Draw 불문률
import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    # 생성자 메소드 (self는 자기 자신을 뜻함)
    def __init__(self, x, y, speed = 5):
        super().__init__()
        self.rect = pygame.Rect(x, y, 32, 32)

        # 실수 위치 추적용
        self.pos_x = float(x)
        self.pos_y = float(y)
        
        self.velocity_y = 0 # y축 방향의 속도
        # self.speed = 5 # 좌우 이동 속도
        # 아래는 60fps 기준 이동 속도 5 * 60 = 300 (144fps 에서도 60fps의 물체 속도를 보여주기 위해서)
        self.speed = 300
        
        # self. gravity = 0.5 # 중력 가속도
        # 가속도 개념이기 때문에 단순히 60을 곱한다고 되는게 아니다 점프힘도 마찬가지
        self.gravity = 1200

        # 점프할 때 위로 튕겨 나가는 힘 (음수인 이유는 화면에서는 y축이 아래로 증가하기 때문)
        # self.jump_strength = - 10
        self.jump_strength = -500
        
        self.jump_count = 2 # 남은 점프 횟수
        self.on_ground = False # 지금 플레이어가 바닥에 닿아있는지를 표시
        self.space_pressed_last = False # 스페이스 키를 누르고 있는 동안 중복 점프 방지


        self.direction = "right" # 애니메이션 방향
        self.state = "idle"

        # 슬라이딩 관련
        self.is_sliding = False
        self.slide_timer = 0
        self.max_slide_time = 0.3 # 슬라이드 지속 시간
        self.slide_cooldown = 0 # 슬라이드 쿨타임
        self.slide_end_time = 0.2 # 슬라이드 모션 전환 위해
    

        # 총 발사 관련
        self.bullets = pygame.sprite.Group()
        self.shoot_cooldown = 0


        # 애니메이션 관련
        self.spritesheet = pygame.image.load("assets/character/JusticeGuy.png").convert_alpha()
        self.animations = self.load_animations()
        self.current_frame = 0
        self.animation_timer = 0



    def load_animations(self):
        animations = {}
        
        
        # 직접 측정한 프레임 좌표
        frame_rects = {
            "jump_down": [
                pygame.Rect(1, 1, 32, 32),
                #pygame.Rect(34, 1, 32, 32),
                #pygame.Rect(67, 1, 32, 32),
                #pygame.Rect(100, 1, 32, 32),
            ],
            "jump_down_fall": [
                pygame.Rect(34, 1, 32, 32),
                pygame.Rect(67, 1, 32, 32),
                pygame.Rect(100, 1, 32, 32),
            ],
            "idle": [
                pygame.Rect(1, 34, 32, 32),
                pygame.Rect(34, 34, 32, 32),
                pygame.Rect(67, 34, 32, 32),
                pygame.Rect(100, 34, 32, 32),
                pygame.Rect(133, 34, 32, 32),
            ],
            "jump": [
                #pygame.Rect(1, 67, 32, 32),
                pygame.Rect(34, 67, 32, 32),
                #pygame.Rect(67, 67, 32, 32),
                #pygame.Rect(100, 67, 32, 32),
                #pygame.Rect(133, 67, 32, 32),
            ],
            "fall": [ 
                pygame.Rect(67, 67, 32, 32),
                pygame.Rect(100, 67, 32, 32),
            ],
            "land": [
                pygame.Rect(133, 67, 32, 32),
                pygame.Rect(1, 67, 32, 32),
            ],
            "walk": [
                pygame.Rect(1, 100, 32, 32),
                pygame.Rect(34, 100, 32, 32),
                pygame.Rect(67, 100, 32, 32),
                pygame.Rect(100, 100, 32, 32),
                pygame.Rect(133, 100, 32, 32),
            ],
            "crouch": [
                pygame.Rect(1, 133, 32, 32),
                pygame.Rect(34, 133, 32, 32),
                pygame.Rect(67, 133, 32, 32),
                pygame.Rect(100, 133, 32, 32),
                pygame.Rect(133, 133, 32, 32),
                pygame.Rect(166, 133, 32, 32),
            ],
            "look_up": [
                #pygame.Rect(1, 166, 32, 32),
                pygame.Rect(34, 166, 32, 32),
                pygame.Rect(67, 166, 32, 32),
                pygame.Rect(100, 166, 32, 32),
                pygame.Rect(133, 166, 32, 32),
                pygame.Rect(166, 166, 32, 32),
                pygame.Rect(199, 166, 32, 32),
            ],
            "walk_look_up": [
                pygame.Rect(1, 199, 32, 32),
                pygame.Rect(34, 199, 32, 32),
                pygame.Rect(67, 199, 32, 32),
                pygame.Rect(100, 199, 32, 32),
                pygame.Rect(133, 199, 32, 32),
            ],
            "slide": [
                pygame.Rect(1, 232, 32, 32),
            ],
            "slide_end": [
                pygame.Rect(1, 232, 32, 32),
            ]
        }

        for state, rects in frame_rects.items():
            animations[state] = [self.spritesheet.subsurface(rect) for rect in rects]
    
        return animations


    def handle_input(self,keys):
        moving = False


        # 총 발사
        if keys[pygame.K_z] and self.shoot_cooldown == 0:
            #print("총 발사 조건 만족 (z 누름 + 쿨타임 OK)")
            dir = self.direction
            if self.on_ground:
                if keys[pygame.K_UP]:
                    dir = "up"
                    
            if keys[pygame.K_DOWN] and not self.on_ground:
                dir = "down"
            bullet_x = self.rect.centerx
            bullet_y = self.rect.centery

            if dir == "right":
                bullet_x += 0
            elif dir == "left":
                bullet_x -= 41
            elif dir == "up":
                bullet_x -= 5 if self.direction == "right" else 24
                bullet_y -= 20
            elif dir == "down":
                bullet_x -= 12 if self.direction == "right" else 20
                bullet_y += 20
            if self.state == "crouch":
                bullet_y += 5

            self.bullets.add(Bullet(bullet_x, bullet_y, dir))
            self.shoot_cooldown = 0.05

        
        # 슬라이드 중 아래 방향키 누르면 중지
        if self.is_sliding:
            if keys[pygame.K_DOWN]:
                self.is_sliding = False
                self.state = "crouch"
                return
            return


        # 슬라이딩
        if keys[pygame.K_x] and self.on_ground and not self.is_sliding and self.slide_cooldown <= 0 and not keys[pygame.K_DOWN]:
            self.is_sliding = True
            self.slide_timer = 0
            self.state = "slide"
            return


        # 숙이고 있지 않을 때 좌우로 움직임
        if self.state != "crouch":
            if keys[pygame.K_LEFT]:
                self.pos_x -= self.speed * self.dt
                self.direction = "left"
                moving = True
            elif keys[pygame.K_RIGHT]:
                self.pos_x += self.speed * self.dt
                self.direction = "right"
                moving = True
        

        # 상태 전환
        if self.on_ground:
            if keys[pygame.K_DOWN]:
                self.state = "crouch"
            elif keys[pygame.K_UP]:
                if moving:
                    self.state = "walk_look_up"
                else:
                    self.state  = "look_up"
            elif moving:
                self.state = "walk"
            else:
                self.state = "idle"
        

        # 점프
        if keys[pygame.K_SPACE] and not self.space_pressed_last:
            if self.jump_count > 0:
                self.velocity_y = self.jump_strength
                self.jump_count -= 1
        self.space_pressed_last = keys[pygame.K_SPACE] # 이번 프레임에 스페이스 키가 눌렸는지 기억

        # 점프하면서 아래
        if not self.on_ground:
            if keys[pygame.K_DOWN]:
                if self.velocity_y < 0:
                    self.state = "jump_down"
                else:
                    self.state = "jump_down_fall"
            elif self.velocity_y < 0:
                self.state = "jump"
            else:
                self.state = "fall"



    # 점프 중이거나 바닥이 아닐 때 중력을 적용해서 낙하하도록 하는 함수
    def apply_gravity(self, tile_group):

        # 바닥일때는 중력 가속도 x
        if self.on_ground and self.velocity_y == 0:
            return

        self.velocity_y += self.gravity * self.dt
        self.pos_y += self.velocity_y * self.dt
        self.rect.y = round(self.pos_y)

        # 충돌 체크
        hits = pygame.sprite.spritecollide(self, tile_group, False)
        for tile in hits:
            if self.velocity_y >= 0 and self.rect.colliderect(tile.rect):
                self.rect.bottom = tile.rect.top
                self.pos_y = self.rect.y

                #if abs(self.velocity_y) < 1: 
                self.velocity_y = 0

                self.jump_count = 2
                self.on_ground = True
                break
        else:
            self.on_ground = False
        

    def update(self, keys, dt, tile_group):
        self.dt = dt # 현재 프레임 시간 저장
        prev_state = self.state # 이전 상태 저장
        prev_on_ground = self.on_ground

        self.apply_gravity(tile_group)
        
        self.handle_input(keys)


 
        # 슬라이딩 처리
        if self.is_sliding:
            slide_speed = self.speed * 2.5
            direction = 1 if self.direction == "right" else -1
            self.pos_x += slide_speed * dt * direction
            self.slide_timer += dt
            
            if self.slide_timer >= self.max_slide_time:
                self.is_sliding = False
                self.slide_cooldown = 0.5
                self.state = "slide_end"
        elif self.state == "slide_end":
            self.slide_timer += dt
            if self.slide_timer >= self.slide_end_time:
                self.state = "idle"

        # 쿨타임 감소
        self.slide_cooldown = max(0, self.slide_cooldown - dt)
        self.shoot_cooldown = max(0, self.shoot_cooldown - dt)

        

        self.bullets.update(dt, tile_group)
        for bullet in list(self.bullets):
            if not bullet.active:
                self.bullets.remove(bullet)



        # 착지 모션
        if not prev_on_ground and self.on_ground:
            self.state = "land"

        if self.state == "land":
            frames = self.animations.get("land", [])
            if self.current_frame >= len(frames) - 1:
                self.state = "walk" if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] else "idle"
    
        

        if self.state != prev_state:
            self.current_frame = 0
            self.animation_timer = 0


        # rect 위치 반영
        self.rect.x = round(self.pos_x)
        self.rect.y = round(self.pos_y)


        # 애니메이션 프레임 업데이트
        self.animation_timer += dt
        if self.animation_timer > 0.1:
            frames = self.animations.get(self.state, [0])
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.animation_timer = 0

        #if self.rect.y > 1080:
            #print("주의 : 캐릭터 화면 아래로 사라짐!", self.rect.y)

    def draw(self,screen):
        frame_list = self.animations.get(self.state, self.animations["idle"])
        frame = frame_list[self.current_frame % len(frame_list)]


        frame_rect = frame.get_rect()

        # 좌우 반전 처리
        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)
              
        frame_x = self.rect.centerx - frame_rect.width
        frame_y = self.rect.bottom - frame_rect.height

        screen.blit(frame, (frame_x, frame_y))

        self.bullets.draw(screen)

