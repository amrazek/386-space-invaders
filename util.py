import pygame


def create_dialog(text, text_color, fill_color, border_color, font_size, width, height):
    # create game over text
    font = pygame.font.SysFont("", font_size)
    font_surf = font.render(text, True, text_color)

    # create a square 1/4 screen dimensions
    dialog_rect = pygame.Rect(0, 0, width, height)
    dialog = pygame.Surface((dialog_rect.width, dialog_rect.height))

    # fill with dialog color
    dialog.fill(fill_color)

    # create black border to set dialog apart more
    border_rect = dialog.get_rect()
    border_rect.left = border_rect.top = 5
    border_rect.width, border_rect.height = border_rect.width - 10, border_rect.height - 10

    pygame.draw.rect(dialog, border_color, border_rect, 5)

    # blit game over text, centered, onto dialog
    blit_rect = font_surf.get_rect()
    blit_rect.center = (dialog_rect.width // 2, dialog_rect.height // 2)

    dialog.blit(font_surf, dest=blit_rect)

    return dialog
