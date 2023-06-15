import re
import time
import pyautogui
import pytest
from modules_for_test.video_record import VideoRec
import allure


class CardsGames(VideoRec):

    def __init__(self) -> None:
        super().__init__()

    # RED = "\033[31m"
    # GREEN = "\033[32m"
    # RESET = "\033[0m"


        self.card_check_text: tuple[str, str] = (
            "click", "search_line_click.png"
        )

        self.path_to_images: str = "/home/user/Test_Native_Client/images/games_cards"

        self.credentials_app: dict[str, str] = {
            "email": "i.zayats@boosteroid.com",
            "passw": "123123123"
        }
        self.auth_app_images: tuple[str, str] = (
            "3_email_click.png", "4_pass_click.png", "remember_my_click.png", "sing_in_click.png", "whats_new.png"
        )
        self.run_app: tuple[str, str] = (
            "start_app.png"
        )
        self.prepare_for_the_test: tuple[str, str] = (
            "whats_new_ok_click.png", "edudc_firs_img.png", "edudc_firs_img.png", "educ_first_img_skip_click.png",
            "your_free_time.png", "allrighs_your_free_time_click.png"
        )
        """Check the games in order: Dota, CS, Fortnite, Crossout"""
        self.find_and_check_games: tuple[str, str] = (
            "whats_new_ok_click.png", "edudc_firs_img.png", "edudc_firs_img.png", "educ_first_img_skip_click.png",
            "your_free_time.png", "allrighs_your_free_time_click.png",
            "search_line_click.png", "dota_click.png", "dota_card.png", "dota_card_inside.png", "search_line_click.png",
            "counter_strike_click.png", "counter_strike_card.png", "counter_strike_card_inside.png", "search_line_click.png",
            "fortnite_click.png", "fortnite_card.png", "fortnite_card_inside.png", "search_line_click.png",
            "crossout_click.png", "crossout_card.png", "crossout_card_inside.png", "full_screen_click.png", "search_line_click.png",
            "dota_click.png", "dota_card_full.png", "dota_card_inside_full.png", "search_line_click.png", "counter_strike_click.png",
            "counter_strike_card_full.png", "counter_strike_inside_full.png", "search_line_click.png", "fortnite_click.png",
            "fortnite_card_full.png", "fortnite_card__inside_full.png", "search_line_click.png", "crossout_click.png",
            "crossout_card_full.png", "crossout_card_inside_full.png", "return_back_click.png", "prod_accaun_settings_click.png",
            "log_out_click.png", "log_out_confirm.png", "log_out_botton_confirm_click.png", "close_app_click.png"
        )
        self.searching_field_test: tuple[str, str] = (
            "dota", "counter", "fortnite", "crossout", "dota", "counter", "fortnite", "crossout"
        )
        self._counter: int = 0


@allure.feature("Test cards of games")
class TestCardsGames:
    cg = None

    @pytest.fixture(autouse=True)
    def init(self):
        if not TestCardsGames.cg:
            TestCardsGames.cg = CardsGames()
        self.cg = TestCardsGames.cg

    @allure.story("Test 1: Run application")
    @pytest.mark.run(order=1)
    def test_startProcess(self):
        self.cg.logger.info(
            "\tRunning Test1 - 'test_startProcess': launching application\n")
        try:
            result = self.cg.startProcess(self.cg.run_app)
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.cg.get_screenshot(
                    "1_test_startProcess.png")
                allure.attach.file(screenshot_path, name="test_start_application",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.cg.get_screenshot(
                "test_startProcess_failed.png")
            allure.attach.file(screenshot_path, name="test_startProcess_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise

        allure.attach("Expected Result:",
                      "The apppicetion will be running successful")
        allure.attach(
            "Summary:", "Test the start process of the application and check gema cards")

    @allure.story("Test 2:Login in application")
    @pytest.mark.run(order=2)
    def test_boosteroidAuth(self):
        self.cg.logger.info("\tRunning Test2 -'setup': application login\n")
        try:
            result = self.cg.boosteroidAuth(
                self.cg.auth_app_images, self.cg.credentials_app)
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.cg.get_screenshot(
                    "2_boosteroidAuth.png")
                allure.attach.file(screenshot_path, name="test_boosteroid_auth",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.cg.get_screenshot(
                "boosteroidAuth_failed.png")
            allure.attach.file(screenshot_path, name="test_boosteroidAuth_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise

    @allure.story("Test 3:Chech cards in application")
    @pytest.mark.run(order=3)
    def test_card_check(self):
        self.cg.logger.info("\tRunning Test3 -'card_check': google login\n")
        try:
            result = self.cg.click_write_or_findAndWait(
                self.cg.find_and_check_games, self.cg.searching_field_test, self.cg.card_check_text)
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.cg.get_screenshot("3_card_check.png")
                allure.attach.file(screenshot_path, name="card_check",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.cg.get_screenshot("card_check_failed.png")
            allure.attach.file(screenshot_path, name="test_card_check_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise
"""

if __name__ == '__main__':
    start_time = time.time()
    
    cg = CardsGames()

    if not cg.startProcess(cg.run_app):
        cg.logger.error("Failed to start process")
        cg.get_screenshot("Not started.png")    

    if not cg.boosteroidAuth(cg.auth_app_images, cg.credentials_app):
        cg.logger.error("Failed to authenticate")
        cg.get_screenshot("auth_error.png")
    
    if not cg.click_write_or_findAndWait(
        cg.find_and_check_games, cg.searching_field_test, cg.card_check_text):
        cg.logger.error("Failed check card")
        cg.get_screenshot("check card.png")
        
    else:
        cg.logger.info("Success start and auth")
        print('\033[32mSuccess start\033[0m')
        print('\033[32mSuccess auth\033[0m')
        print('\033[32mSuccess check card\033[0m')
        
    end_time = time.time()
    execution_time = int(end_time - start_time)
    cg.logger.info("Test execution time: '%s' sec.", execution_time)
    print(f"\033[32mTest execution time: \033[33m'{execution_time}'\033[0m\033[32msec.\033[0m")

"""