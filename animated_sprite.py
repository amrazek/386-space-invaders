import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    """Class that represents a sequence of images. Images must be square. """
    def __init__(self, sprite_sheet, animation_rate):
        super().__init__()

        self.sprite_sheet = sprite_sheet
        self.image = sprite_sheet

        rect = sprite_sheet.get_rect()

        self.width = rect.height
        self.height = rect.height

        num_frames = rect.width // self.width

        self.frames = [pygame.Rect(i * self.width, 0, self.width, self.height) for i in range(num_frames)]
        self.current_frame = 0
        self.last_tick = pygame.time.get_ticks()
        self.ticks_per_frame = round(1000 // num_frames * (1.0 / animation_rate))

    def update(self):
        this_tick = pygame.time.get_ticks()
        elapsed = this_tick - self.last_tick
        if elapsed > self.ticks_per_frame:
            self.last_tick = this_tick
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen, tl_coord):
        screen.blit(self.sprite_sheet, self.image.rect, area=self.frames[self.current_frame])