import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()  # Sprite 초기화
        self.direction = direction
        self.speed = 600
        self.active = True

        self.image = pygame.image.load("assets/weapon/goldBullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 16)) 

        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.direction == "up":
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "down":
            self.image = pygame.transform.rotate(self.image, -90)

        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt, ground_group):
        if self.direction == "right":
            self.rect.x += self.speed * dt
        elif self.direction == "left":
            self.rect.x -= self.speed * dt
        elif self.direction == "up":
            self.rect.y -= self.speed * dt
        elif self.direction == "down":
            self.rect.y += self.speed * dt

        # 그룹 충돌
        for ground in ground_group:
            if self.rect.colliderect(ground.rect):
                #print("총알이 땅에 바로 부딪혀서 삭제됨!")
                self.active = False
                break

        if (self.rect.right < 0 or self.rect.left > 1280 or
            self.rect.bottom < 0 or self.rect.top > 1080):
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
