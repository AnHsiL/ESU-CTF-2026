#Web 


給了一個網址，點開來：
![[W4-4_web.png|366]]

---
# SSTI-waf1
## 題目

**SSTI-waf1**
source

```js
from flask import (
    Flask,
    request,
    render_template,
    render_template_string,
    Response
)

app = Flask(__name__)
app.secret_key = open("/flag").read()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        rawtext = request.form.get("rawtext")
        rawtext = "😺 " + rawtext + " 😺"
        return render_template_string(rawtext)

    return render_template("index.html")

@app.route('/source')
def get_main_py():
    with open('/app/main.py', 'r', encoding='utf-8') as file:
        content = file.read()
    return Response(content, mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
```


## 解題
1. 題目 SSTI，且使用 Flask -> 輸入 `{{config}}`
   ![[W4-4_conf.png]]
2. flag = `CTF{SSTI_can_use_without__}`


