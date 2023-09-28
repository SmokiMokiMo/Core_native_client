import subprocess
from scapy.all import *
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import allure
from modules_for_test.video_record import VideoRec
import pytest

class NetWork(VideoRec):    

    def __init__(self):        
        
        self.ip_addr: dict = {
            "185.2.108.5": "185.2.108.6",
            "185.2.108.6": "185.2.108.5"
        }        
        self.target_ip:str = "192.168.20.48"
        self.network_interface: str = "eno2"
        self._counter: int = 0
        self.numbers_of_switches: int = 0
        self.stop_capture: bool = False
        self.protocol_type: str = 'TCP'
        self.switch_limit: int = 50
        self.token = "https://hooks.slack.com/services/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"  # Replace with your Slack API token
        self.channel = "C05H1FS7B1U"  # Replace with your channel or user ID


    def packet_handler(self, packet):
        if self.stop_capture:
            return

        if packet.haslayer(IP) and packet.haslayer(UDP):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            udp_srcport = packet[UDP].sport
            udp_dstport = packet[UDP].dport
            udp_payload = packet[UDP].payload

            # Check if the destination IP is in the blocked/unblocked IP list
            
            for hostname, unblocked in self.ip_addr.items():
                if ip_src == hostname:
                    self._counter += 1
                    print(f"Counter is: {self._counter}")
                    if self._counter == 20:
                        print("Reset counter")
                        # Try block
                        if not self.check_iptables_stdout(ip_src):
                            self.numbers_of_switches += 1
                            print(f"Try block on {ip_src}")
                            self.reset_all_iptable_rules()
                            self.block_ip(ip_src)  # Block IP using iptables
                        elif self.check_iptables_stdout(ip_src):
                            self.numbers_of_switches += 1
                            print(f"Try block: IP: {ip_src} exists in Iptables -> Reset rules for Blocked IP -> Block IP: {unblocked}")
                            self.reset_all_iptable_rules()
                            self.block_ip(unblocked)
                        self._counter = 0

                if self.numbers_of_switches == self.switch_limit + 1:
                    self.send_slack_message(f"The switch limit of {self.switch_limit} has been reached!")
                    print(f"The switch limit of {self.switch_limit} has been reached!")
                    self.reset_all_iptable_rules()
                    self.stop_capture = True
                    break
                           
            # Print packet details
            print(f"numbers of switches is: {self.numbers_of_switches}")
            print(f"Source IP: {ip_src}")
            print("----------------------------------------")
            time.sleep(1)

    def check_iptables_stdout(self, ip) -> bool:        
        command = ['sudo', 'iptables', '-n', '-L']
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout
        lines = output.splitlines()

        for line in lines:
            if ip in line:                
                return True
            
        return False

    def reset_all_iptable_rules(self):        
        command = ['iptables', '-F']
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout
        print(f"RESET ALL RULES {output}")        

    def block_ip(self, ip):
        ckeck: bool = self.check_iptables_stdout(ip)
        if ckeck is True:
            print(f"Method block_ip: ip-{ip} already exists in Iptables list")
        else:
            print(f"Method 'block_ip':{ip}")
            subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-p', self.protocol_type, '-j', 'DROP'], check=True)

    def unblock_ip(self, ip):
        ckeck: bool = self.check_iptables_stdout(ip)
        if ckeck is False:
            print(f"Method unblock_ip: rule for ip-{ip} does not exist")       
        else:
            print(f"Method 'unblock_ip':{ip}")
            try:
                subprocess.run(['iptables', '-D', 'INPUT', '-s', ip, '-p', self.protocol_type, '-j', 'DROP'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while unblocking IP: {ip}")
                print(f"Error message: {e}")

    def start_capture(self):        
        sniff(iface=self.network_interface, filter="udp", prn=self.packet_handler)

    def send_slack_message(self, message):
        try:
            payload = {"text": message}
            response = requests.post(self.token, json=payload)

            if response.status_code == 200:
                print("Message sent successfully to Slack!")
            else:
                print("Failed to send message to Slack.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending the message: {str(e)}")



@allure.feature("Switch between SG")
class TestSwitchBetweenSg:
    up = None

    @pytest.fixture(autouse=True)
    def init(self):

        if not TestSwitchBetweenSg.up:
            TestSwitchBetweenSg.up = NetWork()
        self.reg = TestSwitchBetweenSg.up

    @allure.story("Test:Run app 'Boosteroid', run session and switch between SG")
    @pytest.mark.run(order=1)
    def test_environment_preparation(self):
        self.reg.logger.info(
            "\tRunning Test -'Switch between SG': running app 'Boosteroid' -> start session -> switching between SG\n")
        try:           
            result = self.up.reset_all_iptable_rules() 
            result2 = self.up.start_capture()
            assert result is True
            assert result2 is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot(
                    "switch_sg.png")
                allure.attach.file(screenshot_path, name="switch_sg",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot(
                "switch_sg_failed.png")
            allure.attach.file(screenshot_path, name="switch_sg_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise
        allure.attach(f"Expected Result:",
                      f"Boosteroid application should be running, start sessinon should be successful, numbers of switches must be '{self.reg.switch_limit}'")
        allure.attach(
            "Summary:", "Test 'Switch between SG': running app 'Boosteroid' -> start session -> switching between SG")

"""

if __name__ == '__main__':
    start_time = time.time()

    up = UpdateApp()

    if not up.environment_preparation():
        up.get_screenshot('environment_preparation_boosteroid')
        up.logger.info("\033[31mEnvironment preparation failed\033[0m")           
    if not up.compare_app_ver():
        up.get_screenshot('failed_remove_boosteroid')
        up.logger.info("\033[31mApplication updating failed\033[0m") 

    else:
        up.logger.error("\033[32mApplication updating successful\033[0m") 
        up.get_screenshot('failed_remove_boosteroid')
                 

    
    end_time = time.time()
    execution_time = int(end_time - start_time)
    up.logger.info("Test execution time: '%s' sec.", execution_time)
    print(f"\033[32mTest execution time: \033[33m'{execution_time}'\033[0m\033[32msec.\033[0m")
"""
