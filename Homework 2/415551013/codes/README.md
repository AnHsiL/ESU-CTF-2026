# 單向條件式通訊協定

`lossy_protocol.py` 從 `config.yaml` 讀取雙方的選擇與訊息，在本機模擬一次 sender → receiver 的通訊。
只有雙方皆選擇 `true`，接收者才能取得訊息；姓名可以自行更換。

## 環境與安裝

需要 Python 3.10 以上版本，以及 PyYAML

## 設定 config.yaml

以 UTF-8 儲存 YAML：

| 欄位 | 格式與用途 |
|---|---|
| `capacity` | 正整數，訊息容量上限，單位為 bytes |
| `sender` | `[傳送者姓名, 選擇, 訊息文字]` |
| `receiver` | `[接收者姓名, 選擇]` |

- 選擇使用不加引號的 `true` 或 `false`，不能寫成字串 `"true"`／`"false"`。
- 訊息以 UTF-8 編碼後的 bytes 數不得超過 `capacity`；例如 `"A"` 為 1 byte，`"你好"` 為 6 bytes。
- 目前設定載入器在 sender 選擇 `false` 時，也會檢查訊息大小。
- 訊息不足容量時會自動填充；容量越大，密文越大、執行通常越慢。
- YAML 頂層只接受 `capacity`、`sender`、`receiver` 三個欄位。

## 執行

```powershell
python lossy_protocol.py
```

程式預設讀取 `config.yaml`，也可指定其他設定檔：

```powershell
python lossy_protocol.py another_config.yaml
```

## 輸出結果

| Sender 選擇 | Receiver 選擇 | 結果 |
|---|---|---|
| `true` | `true` | `ACCEPT`，並顯示原訊息 |
| `true` | `false` | `NO_INFO`，不取得訊息與傳送者選擇 |
| `false` | `true` | `REJECT`，得知傳送者拒絕 |
| `false` | `false` | `NO_INFO`，不取得訊息與傳送者選擇 |

程式另顯示公鑰與密文大小，以及三個階段的耗時（秒）：

- `start time`：接收者產生金鑰與公開金鑰編碼。
- `send time`：傳送者封裝、加密與密文編碼。
- `receive time`：接收者解析密文；有正常私鑰時解密並解析明文。

這些時間不包含 YAML 讀取、列印或網路傳輸。
程式只在終端機顯示結果，不會自動寫入實驗 CSV。
