#Web 

## 題目

**dig-argument**
給了一個網址，點開來
![[W1-19_web.png|center|441]]
可以點擊 `main.py` 進入 `http://chals1:20018/?debug=1`：
```python
from flask import Flask, render_template, request, send_file
import subprocess

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def dig():
    dig_result = None
    if request.args.get("debug"):
        return send_file(__name__ + ".py")
    if request.method == "POST":
        hostname1 = request.form["hostname1"]
        hostname2 = request.form["hostname2"]
        process = subprocess.Popen(
            ["dig", hostname1, hostname2],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, _ = process.communicate()
        dig_result = output.decode()

    return render_template("index.html", request=request, dig_result=dig_result)


if __name__ == "__main__":
    app.run(debug=True)
```


### Argument Injection
應用程式將未經過濾的外部輸入作為命令列參數（arguments）傳遞給作業系統或執行檔，攻擊者可藉由注入特殊字元或參數開關（如 `-`、`--`），使資料被誤解析為控制選項，進而改變原本的執行行為

##### 例子
搜尋關鍵字 "aaa"
```bash
grep "aaa" data.txt
```
會輸出 `data.txt` 中的 "aaa"
*若* 輸入為 "--help"
```bash
grep --help data.txt
```
輸出 "--help"，`--` 的作用是選項到此結束，後面全部視為資料，因此忽視 `data.txt`


---
## 解題
1. 題目為 *Dig-argument* -> 可能是 Argument Injection
   網頁顯示 "flag is in /flag" -> 目標：讀取 "/flag"
2. 觀察程式碼
   ```python
   process = subprocess.Popen(
		["dig", hostname1, hostname2],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
	)
   ```
   -> 實際執行的指令是 `dig hostname1 hostname2`，並且不是用 shell 字串執行，而是將 `hostname1 hostname2` 視為兩個 `dig` 的參數傳給程式 
   -> 沒辦法利用前端規則繞過
   -> 用 Argument Injection
3. 輸入 `man dig` 找 `dig` 指令中可能可以利用的參數
   ![[W1-19_dig-options.png]]
   --> 發現 `-f` 可以讀檔
4. 讀取 "/flag"
   ![[W1-19_flag.png|569]]
5. flag = `CTF{dig_argument_14e7d03bb3a5340c53ba9cd0}`













