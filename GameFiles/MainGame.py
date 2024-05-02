import pygame

# Importing Tools
from Tools.Image import Image
from Tools.GameStateManager import GameStateManager

# Importing States
from states.MainMenuState import MainMenuState
from states.SettingsState import SettingsState
from states.CreditsState import CreditsState
from states.LevelState import LevelState
from states.EndlessModState import EndlessModState


class FirstStageState:
    def __init__(self):
        pass


def main():
    pygame.init()
    WIDTH = 1200
    HEIGHT = 700
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The Silent Defender")

    FONT = pygame.font.Font("GameFiles/assets/fonts/font.otf", 40)
    FONT2 = pygame.font.Font("GameFiles/assets/fonts/font2.otf", 40)
    Click_sound = "GameFiles/assets/sounds/click_sound.mp3"
    btn_frame = "GameFiles/assets/images/btn_frame.png"
    LOGO = "GameFiles/assets/images/Logo.png"
    MBG = "GameFiles/assets/images/background_image.png"
    SNG = "GameFiles/assets/sounds/MenuMusic.mp3"
    pygame.mixer.music.load(SNG)
    pygame.mixer.music.play(-1)
    LOGO_WIDTH = WIDTH - (WIDTH // 4)
    logo_x = (WIDTH - LOGO_WIDTH) // 2
    logo_y = 30

    game_state_manager = GameStateManager()
    logo = Image(LOGO, logo_x, logo_y)
    logo.resize(LOGO_WIDTH, 200)
    mainBg = Image(MBG, 0, 0)

    main_menu_state = MainMenuState(
        WIDTH, HEIGHT, FONT, Click_sound, btn_frame, game_state_manager, logo, mainBg
    )
    settings_state = SettingsState(
        WIDTH,
        HEIGHT,
        FONT,
        SNG,
        Click_sound,
        btn_frame,
        game_state_manager,
        logo,
        mainBg,
    )
    credits_state = CreditsState(
        WIDTH, HEIGHT, FONT, Click_sound, btn_frame, game_state_manager, logo, mainBg
    )
    level_state = LevelState(
        WIDTH,
        HEIGHT,
        FONT,
        Click_sound,
        btn_frame,
        game_state_manager,
        logo,
        mainBg,
    )
    endlessmod_state = EndlessModState(
        WIDTH,
        HEIGHT,
        FONT2,
        game_state_manager,
    )

    game_state_manager.add_state("MainMenu", main_menu_state)
    game_state_manager.add_state("Settings", settings_state)
    game_state_manager.add_state("Credits", credits_state)
    game_state_manager.add_state("Levels", level_state)
    game_state_manager.add_state("Endless", endlessmod_state)
    game_state_manager.change_state("MainMenu")


    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60) / 1000  # Amount of seconds since last frame

        for event in pygame.event.get():
            game_state_manager.handle_events(event)

        game_state_manager.update(dt)  # Pass delta time to your update function

        WIN.fill((255, 255, 255))
        game_state_manager.draw(WIN)
        # Draw image_cursor to the mouse position
        mouse_pos = pygame.mouse.get_pos()
        image_cursor = Image("GameFiles/assets/images/Jeff.png", mouse_pos[0], mouse_pos[1])
        image_cursor.draw(WIN)

        pygame.mouse.set_visible(False)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
