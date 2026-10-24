#Reverse

## 題目

**idb - corrupted main**
Fixing IDB, find hidden string

並提供了 `lab01.i64`

## 解題
1. 題目為 corrupted main，並且要求要修好 IDB -> `main` 有損壞
2. 用 IDA 打開 `lab01.i64`，找到 main 的位置
   ```armasm
   .text:0000000000001230 main:            ; DATA XREF: start+18↑o
	.text:0000000000001230 ; __unwind {
	.text:0000000000001230            endbr64
	.text:0000000000001234            push    rbp
	.text:0000000000001235            mov     rbp, rsp
	.text:0000000000001238            sub     rsp, 10h
	.text:000000000000123C            mov     [rbp-4], edi
	.text:000000000000123F            mov     [rbp-10h], rsi
	.text:0000000000001243            lea     rax, aHelloworld ; "HelloWorld!"
	.text:000000000000124A            mov     rdi, rax
	.text:000000000000124D            call    _puts
	.text:0000000000001252
	.text:0000000000001252 loc_1252:        ; CODE XREF: .text:loc_1252↑j
	.text:0000000000001252            jmp     short near ptr loc_1252+1
	.text:0000000000001254 
	; --------------------------------------------------------------------------
	.text:0000000000001254                 ror     byte ptr [rax-73h], 5
	.text:0000000000001258                 xor     al, 0Eh
	.text:0000000000001258 
	; --------------------------------------------------------------------------
	.text:000000000000125A            dq 0FE0CE8C789480000h
	.text:0000000000001262            dq 0E2D058D48FFFFh
	.text:000000000000126A            dq 0B8C7894800h
	.text:0000000000001272            dq 0B8FFFFFE18E800h
	.text:000000000000127A            dw 0
	.text:000000000000127C            db 0
	.text:000000000000127D 
	; --------------------------------------------------------------------------
	.text:000000000000127D            leave
	.text:000000000000127E            retn
	.text:000000000000127E ; } // starts at 1230
   ```
   發現 jump 的位置：
   ```armasm
   0000000000001252            jmp     short near ptr loc_1252+1
   ```
   跳回自己這條 instruction 的中間 `0x1253` -> 【overlapping instructions】有兩種解碼方式
   - 原本的解碼 -> 後面出現亂碼 (X)
   - 從 `jmp` 的目標開始解碼 
1. 把 `0x1252: jmp...` ~ `0x127C: db ...` 這段選取按 `u`(Undefine)，並選取 `0x1053` ~ `0x127C` 按 `c`(Make Code)
   ![[W3-2_fixed_main.png|561]]
2. 對 `main` 按 `p`(Create function)，將選取的程式碼區塊定義為一個函數
   ![[W3-2_func_main.png|585]]
   >[!abstract] Linux x86-64 System 
   >函式參數順序：
   >- 第 1 個參數 → `RDI`
   >- 第 2 個參數 → `RSI`
   >- 第 3 個參數 → `RDX`
   >- 第 4 個參數 → `RCX`
   
    程式把變數 的位址存到 `RDI` 後呼叫 function -> function 的參數很可疑
   - `_puts` 參數 `aD` ，雙擊`aD` 
     ![[W3-2_aD.png|215]]
     看起來不是
   - `_wprintf` 參數 `format`，雙擊 `format` 
     ![[W3-2_format.png|407]]
     非常可疑，每個字元都是 4 bytes + 註解寫的 `wchar_t` -> 是 string
1. 點選變數 `format`，用 `options`-> `string literals` -> `32 bits`
   ![[W3-2_flag.png]]
2. flag = `FLAG{fix_main_and_flag}`
