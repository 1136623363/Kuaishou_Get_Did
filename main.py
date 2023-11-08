import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

option = Options()

mobile_emulation = {"deviceName": "iPhone 6/7/8"}
option.add_experimental_option("mobileEmulation", mobile_emulation)

option.add_argument('headless') # 无界面
option.add_argument("--disable-gpu")
option.add_argument('no-sandbox')

# 设置 set_capability  desired_capabil 在4版本中取消了 替代的是 set_capability
option.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

driver = webdriver.Chrome(options=option)

# 访问网页
driver.get(
    "https://livev.m.chenzhongtech.com/fw/live/KPL704668133?fid=0&cc=share_wxms&followRefer=151&shareMethod=CARD&kpn=GAME_ZONE&subBiz=LIVE_STEARM_OUTSIDE&shareId=17006290026928&shareToken=X-5EcwumOXxng1uv&shareMode=APP&originShareId=17006290026928&shareObjectId=web_pc&shareUrlOpened=0&timestamp=1655866833281")

# 等待网络请求加载完毕（你可以根据需要调整等待时间）
time.sleep(3)

driver.get(
    "https://livev.m.chenzhongtech.com/fw/live/KPL704668133?fid=0&cc=share_wxms&followRefer=151&shareMethod=CARD&kpn=GAME_ZONE&subBiz=LIVE_STEARM_OUTSIDE&shareId=17006290026928&shareToken=X-5EcwumOXxng1uv&shareMode=APP&originShareId=17006290026928&shareObjectId=web_pc&shareUrlOpened=0&timestamp=1655866833281")

# 获取所有网络请求
logs = driver.get_log("performance")

request_list = []
for item in logs:
    log = json.loads(item["message"])["message"]
    if "Network.requestWillBeSentExtraInfo" in log["method"]:
        if log["params"]["headers"].get("Cookie"):
            if "did=" in log["params"]["headers"]["Cookie"]:
                request_list.append(log)
# 关闭浏览器
driver.quit()
print(request_list[-1]["params"]["headers"]["Cookie"])
