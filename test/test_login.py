import pyautogui
from typing import Tuple, Dict
from Base import Base
import time
import pytest
import allure


class Auth(Base):

    def __init__(self, file_name: Tuple[str, ...]="auth.png") -> None:
        super().__init__()

        """Data for the test"""
        self.credentials: Dict[str, str] = {
            "email": "i.zayats@boosteroid.com",
            "passw": "123123123"
            }
        self.clickable_images: Tuple[str, ...] = (
                "auth.png", "email.png", "password.png", "remember.png", "log_in.png", "change_log.png",
                "change_log_ok.png", "edu.png", "next.png", "edu1.png", "next.png", "edu2.png",
                "next.png", "edu3.png", "next.png", "edu4.png", "next.png", "edu5.png",
                "next.png", "edu6.png", "finish.png", "free_time.png", "alright.png",
                "main_menu.png", "user_sett_PROD.png", "menu_user.png", "log_out.png",
                "logout_confirm.png", "out_confirm_ok.png", "boost_start.png", "close_prog.png"
            )
        self.unlockable_images: Tuple[str, ...] = (
                "auth.png", "change_log.png", "edu.png", "edu1.png", "edu2.png", "edu3.png", "edu4.png",
                "edu5.png", "edu6.png", "free_time.png", "main_menu.png", "logout_confirm.png", "boost_start.png", "menu_user.png"
            )
        self.path_to_images: str = "/home/user/PycharmProjects/Test_Native_Client/images/login"
    
    def boosteroidAuth(self) -> bool:
            if not self.click_image(self.clickable_images[1]):
                return False
            pyautogui.write(self.credentials["email"])
            if not self.click_image(self.clickable_images[2]):
                return False
            pyautogui.write(self.credentials["passw"])
            if not self.click_image(self.clickable_images[3]):
                return False
            if not self.click_image(self.clickable_images[4]):
                return False
            time.sleep(2)
            return self.test_auth(self.clickable_images, self.unlockable_images, 5)




@allure.feature("Runong application, authorization and close application")
class TestAuth:
    reg = None



    @pytest.fixture(autouse=True)
    def init(self):
        if not TestAuth.reg:
            TestAuth.reg = Auth()
        self.reg = TestAuth.reg
    

    @allure.story("launch the application and check if it has started")
    @pytest.mark.run(order=1)
    def test_startProcess(self):
        self.reg.logger.info("\tRunning Test1 - 'test_startProcess': run application\n")
        recording = None
        try:
            recording = self.reg.start_video_recording("test_auth")            
            result1 = self.reg.startProcess(self.reg.clickable_images[0])
            result2 = self.reg.boosteroidAuth()
            assert result1 is True
            assert result2 is True
            with allure.step("Attach screenshot"):
                if recording is not None:
                    self.reg.stop_video_recording(recording)
                    self.reg.stop_threads()
                screenshot_path = self.reg.get_screenshot("test_startProcess.png")
                allure.attach.file(screenshot_path, name="Start_application", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            #self.reg.logger(f"Error is: {e}")
            #screenshot_path = self.reg.get_screenshot("test_startProcess_failed.png")
            allure.attach("Screenshot", self.reg.get_screenshot("test_startProcess_failed.png"),
                          allure.attachment_type.PNG)
            raise
        #finally:
        #    if recording is not None:               
        #        self.reg.stop_video_recording(recording)
        #    self.reg.stop_threads()
            
    """
    @allure.story("authorization and familiarization with the application")
    @pytest.mark.run(order=2)
    def test_boosteroidAuth(self):
        self.reg.logger.info("\tRunning Test2 -'test_boosteroidAuth': authorization and education check\n")
        try:
            result = self.reg.boosteroidAuth()
            assert result is True
            with allure.step("Attach screenshot"):
                 screenshot_path = self.reg.get_screenshot("test_boosteroidAuth.png")
                 allure.attach.file(screenshot_path, name="Auth_and_chech_training",
                               attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot("test_boosteroidAuth_failed.png")
            allure.attach.file(screenshot_path, name="Auth_and_chech_training",
                               attachment_type=allure.attachment_type.PNG)
            raise
        
        
        



    
if __name__ == '__main__':
    start_time = time.time()
    
    auth = Auth()    

    if not auth.startProcess(auth.clickable_images[0]):
        auth.logger.error("Failed to start process")
        auth.get_screenshot("Not started.png")
    elif not auth.boosteroidAuth():
        auth.logger.error("Failed to authenticate")
        auth.get_screenshot("auth_error.png")
    else:
        auth.logger.info("Success start and auth")
        print('\033[32mSuccess start\033[0m')
        print('\033[32mSuccess auth\033[0m')
        
    end_time = time.time()
    execution_time = int(end_time - start_time)
    auth.logger.info("Test execution time: '%s' sec.", execution_time)
    print(f"\033[32mTest execution time: \033[33m'{execution_time}'\033[0m\033[32msec.\033[0m")
"""