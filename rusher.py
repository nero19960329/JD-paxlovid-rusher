import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import time
import winsound


def beep(event):
    while not event.is_set():
        winsound.Beep(600, 500)
        time.sleep(0.5)


parser = argparse.ArgumentParser()
parser.add_argument("--id", type=str)
args = parser.parse_args()


mobile_emulation = {
    "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
}

chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(
    options=chrome_options,
)
driver.get(f"https://m.healthjd.com/s/my/prescribe/detail?rxId={args.id}")

input("waiting for login...")

while True:
    while True:
        try:
            buy_btn = driver.find_element(By.XPATH, "//span[text()='立即购买']")
            buy_btn.click()
            break
        except Exception as e:
            time.sleep(0.5)
    retry_count = 10
    while retry_count >= 0:
        try:
            driver.find_element(By.XPATH, "//div[contains(text(), '抱歉，您本次购买的部分商品因无货')]")
            ret_btn = driver.find_element(
                By.XPATH, "//span[contains(text(), '我知道了')]"
            ).find_element(By.XPATH, "..")
            ret_btn.click()
            break
        except Exception as e:
            time.sleep(0.5)
        retry_count -= 1
    if retry_count < 0:
        print("Needs manual intervention!")
        stop_event = threading.Event()
        thread = threading.Thread(
            target=beep, args=(stop_event,), daemon=True, name="bgm"
        )
        thread.start()
        input("waiting for any key...")
        stop_event.set()
        thread.join()
