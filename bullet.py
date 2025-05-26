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

    def update(self, dt, ground_group):  # 여기서 ground_group이 실제로는 collision_rects를 의미
        if self.direction == "right":
            self.rect.x += self.speed * dt
        elif self.direction == "left":
            self.rect.x -= self.speed * dt
        elif self.direction == "up":
            self.rect.y -= self.speed * dt
        elif self.direction == "down":
            self.rect.y += self.speed * dt

        # 충돌 판정
        for rect in ground_group:
            if self.rect.colliderect(rect):
                self.active = False
                break

        # 화면 밖으로 나가면 비활성화
        if (self.rect.right < 0 or self.rect.left > 2000 or
            self.rect.bottom < 0 or self.rect.top > 2000):
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
