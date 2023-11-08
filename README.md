# Kuaishou_Get_Did
生成快手did
# 原理:
手机模式刷新两次网页就可以生成did了，但是其中发送了数十个请求，逆向破解难度过大，所以直接使用selenium模拟手机进入快手直播页面刷新两次网页，从而获取did

#  环境：
Ubuntu22.04

python > 3.8

selenium = 4.15.2

Google Chrome = 119.0.6045.105

ChromeDriver =119.0.6044.0

原理其实都不难，问题主要出现在Chrome和对应ChromeDriver的安装，还有selenium新版本的用法改动


Chrome安装
```
wget https://dl.google.com/linux/chrome/deb/pool/main/g/==google-chrome-stable==/==google-chrome-stable==_==119.0.6045.105==-1_amd64.deb

sudo dpkg -i google-chrome-stable_119.0.6045.105-1_amd64.deb
apt -f install
```

chromedriver安装
https://vikyd.github.io/download-chromium-history-version/#/
下载对应机器和版本的zip
```
unzip Linux_x64_1203869_chromedriver_linux64.zip #注意修改中间的版本号
cd chromedriver_linux64
sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

```

检查chrome和chromedriver是否安装成功
```
google-chrome-stable --version
chromedriver --version
```


selenium安装 (默认安装版本>4.10)
```
pip3 install selenium
```


# 代码：
main.py
```
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
  
# 设置 set_capability desired_capabil 在4版本中取消了 替代的是 set_capabilityoption.set_capability("goog:loggingPrefs", {'performance': 'ALL'})  
  
driver = webdriver.Chrome(options=option)  
  
# 访问网页  
driver.get("https://livev.m.chenzhongtech.com/fw/live/KPL704668133?fid=0&cc=share_wxms&followRefer=151&shareMethod=CARD&kpn=GAME_ZONE&subBiz=LIVE_STEARM_OUTSIDE&shareId=17006290026928&shareToken=X-5EcwumOXxng1uv&shareMode=APP&originShareId=17006290026928&shareObjectId=web_pc&shareUrlOpened=0&timestamp=1655866833281")  
  
# 等待网络请求加载完毕（你可以根据需要调整等待时间）  
time.sleep(3)  
  
driver.get("https://livev.m.chenzhongtech.com/fw/live/KPL704668133?fid=0&cc=share_wxms&followRefer=151&shareMethod=CARD&kpn=GAME_ZONE&subBiz=LIVE_STEARM_OUTSIDE&shareId=17006290026928&shareToken=X-5EcwumOXxng1uv&shareMode=APP&originShareId=17006290026928&shareObjectId=web_pc&shareUrlOpened=0&timestamp=1655866833281")  
  
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
```
