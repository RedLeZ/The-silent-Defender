import pygame
from Tools.Button import Button
import json


class ShopState:
    def __init__(
        self,
        screen_width,
        screen_height,
        font,
        click_sound,
        btn_frame,
        game_state_manager,
        logo,
        background_image,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.click_sound = click_sound
        self.btn_frame = btn_frame
        self.game_state_manager = game_state_manager
        self.logo = logo
        self.background_image = background_image
        self.selected_item_index = 0
        self.showingConfirmPurchaseMenu = False
        with open("GameFiles/assets/data/private/playerstats.json") as f:
            self.playerState = json.load(f)
        self.coins = self.playerState["coins"]

        self.buttons = [
            Button(
                (self.screen_width - 150) / 2,
                self.screen_height - 80,
                150,
                50,
                "Back",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=self.back_button_clicked,
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
        ]
        self.cButtons = [
            Button(
                (self.screen_width - 100) / 2 - 100,
                self.screen_height / 2 - 50,
                150,
                50,
                "Yes",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=self.buy_item,
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
            Button(
                (self.screen_width - 100) / 2 + 100,
                self.screen_height / 2 - 50,
                150,
                50,
                "No",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=self.Cback_button_clicked,
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
        ]

    def Cback_button_clicked(self):
        self.showingConfirmPurchaseMenu = False
        self.game_state_manager.change_state("Shop")

    def buy_item(self):
        with open("GameFiles/assets/data/private/playerstats.json") as f:
            self.playerState = json.load(f)
        with open("GameFiles/assets/data/publicData.json") as f:
            self.PublicData = json.load(f)
        with open("GameFiles/assets/data/private/items.json") as f:
            self.items = json.load(f)
        self.coins = self.playerState["coins"]
        background_image = self.PublicData[0]["Background_Image"]
        projectile_image = self.PublicData[0]["Projectile_Image"]
        item = self.items[self.selected_item_index]
        item_name = item["name"]
        item_price = item["price"]
        item_image = item["image"]
        if self.coins >= item_price and item["item_is_bought"] == False:
            self.coins -= item_price
            self.playerState["coins"] = self.coins
            item["item_is_bought"] = True
            if item["image_type"] == 0:  # Background
                background_image = item_image
            elif item["image_type"] == 1:  # Projectile
                projectile_image = item_image

            with open("GameFiles/assets/data/private/playerstats.json", "w") as f:
                json.dump(self.playerState, f)
            with open("GameFiles/assets/data/private/items.json", "w") as f:
                json.dump(self.items, f)
            with open("GameFiles/assets/data/publicData.json", "w") as f:
                self.PublicData[0]["Background_Image"] = background_image
                self.PublicData[0]["Projectile_Image"] = projectile_image
                json.dump(self.PublicData, f)
            print(f"Item {item_name} bought for {item_price} coins!")
        elif item["item_is_bought"] == True:
            print(f"Item {item_name} is already bought!")
            if item["image_type"] == 0:
                background_image = item_image
            elif item["image_type"] == 1:
                projectile_image = item_image
        else:
            print("Not enough coins!")
        self.showingConfirmPurchaseMenu = False

    def start(self):
        self.showingConfirmPurchaseMenu = False
        pass

    def end(self):
        pass

    def draw_item_list(self, screen):
        with open("GameFiles/assets/data/private/items.json") as f:
            self.items = json.load(f)
        x = 50
        y = 50
        for i, item in enumerate(self.items):
            item_image = pygame.image.load(item["image"]).convert_alpha()
            item_image = pygame.transform.scale(item_image, (100, 100))
            item_price = item["price"]
            item_name = item["name"]
            item_box = pygame.Rect(x, y, 100, 100)
            pygame.draw.rect(screen, (255, 255, 255), item_box)
            font = pygame.font.Font(None, 36)
            text = font.render(item_name, True, (0, 0, 0))
            screen.blit(text, (x, y + 100))
            text = font.render(str(item_price), True, (0, 0, 0))
            screen.blit(text, (x, y + 120))
            screen.blit(item_image, (x, y))

            if i == self.selected_item_index:
                pygame.draw.rect(screen, (255, 0, 0), (x, y, 100, 100), 5)  # Red border
            x += 200
            if x >= self.screen_width - 150:
                x = 50

    def update(self, dt):
        for cButton in self.cButtons:
            cButton.update(pygame.mouse.get_pos())
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for cButton in self.cButtons:
                if cButton.rect.collidepoint(event.pos):
                    cButton.click()
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.click()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_item_index -= 1
            elif event.key == pygame.K_RIGHT:
                self.selected_item_index += 1
            elif event.key == pygame.K_RETURN:
                self.showingConfirmPurchaseMenu = True
            self.selected_item_index = max(
                0, min(self.selected_item_index, len(self.items) - 1)
            )

    def confirmPurchase_menu(self, item_index):
        item = self.items[item_index]
        item_name = item["name"]
        item_price = item["price"]
        text = f"Are you sure you want to buy {item_name} for {item_price} coins?"
        return text

    def DrawConfirmPurchaseMenu(self, screen, text):
        font = pygame.font.Font(None, 36)
        backgroundRect = pygame.Rect(
            self.screen_width / 4 - 10,
            self.screen_height / 3,
            self.screen_width / 2 + 50,
            self.screen_height / 5,
        )
        pygame.draw.rect(screen, (255, 0, 255), backgroundRect)
        text = font.render(text, True, (0, 0, 0))
        screen.blit(text, (self.screen_width / 4, self.screen_height / 3))
        for cButtons in self.cButtons:
            cButtons.draw(screen)

    def draw(self, screen):
        self.background_image.draw(screen)

        for button in self.buttons:
            button.draw(screen)
        self.draw_item_list(screen)
        # draw the coins
        font = pygame.font.Font(None, 36)
        text = font.render(f"Coins: {self.coins}", True, (0, 0, 0))
        screen.blit(text, (self.screen_width - 150, 20))
        if self.showingConfirmPurchaseMenu:
            self.DrawConfirmPurchaseMenu(
                screen, self.confirmPurchase_menu(self.selected_item_index)
            )

    def back_button_clicked(self):
        self.game_state_manager.change_state("MainMenu")
