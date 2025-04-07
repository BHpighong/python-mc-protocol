# 🧠 Mitsubishi PLC 指令產生器（Python + MC Protocol）

這個專案是一個用 Python 撰寫的 Mitsubishi PLC 通訊模組，  
透過 **MC Protocol（ASCII 3C frame 模式）** 來產生對 PLC 的 Batch / Random 寫入指令。

此專案特別設計給以下兩類使用者：
- 想用 **Python 控制 Mitsubishi PLC** 的開發者
- 需要在 **PC-based 自動化專案中進行馬達或硬體控制** 的工程師

---

## 🔧 主要特色

- ✅ 支援 MC Protocol 的 ASCII 3C frame 格式
- ✅ 可針對 M（位元）、D（字）裝置做 Batch 或 Random 寫入
- ✅ 接受 **十進位輸入**，自動轉換成 PLC 可讀的 ASCII hex 格式
- ✅ 可透過 **串列埠或 TCP 通訊** 傳送指令
- ✅ 附加工具函式：可將 32-bit 整數自動拆成高低 16-bit（對應 D10/D11）
- ✅ 適合用在 **PC 控制、AC伺服驅動、智慧工站整合等應用場景**

---

## 💬 為什麼會做這個？

現在許多自動化專案已經開始使用 Python 進行資料擷取、上位機介面甚至簡單邏輯控制。  
但實際要「用 Python 去寫入 PLC」卻常常卡關，因為 Mitsubishi 官方幾乎沒有提供 Python 的通訊函式，  
網路上也幾乎找不到 MC Protocol 的範例。

我們希望透過這個模組，提供一種不需使用昂貴 I/O 卡、只靠通訊就能實現控制的解法。  
透過串列或 TCP 連接，就能把 Python 的彈性與開發效率，延伸到實際硬體層面。

---

## 📁 專案檔案簡介

| 檔案名稱              | 說明 |
|-----------------------|------|
| `mc_protocol_rw.py`   | 封包產生核心，負責建立符合 MC Protocol 的 ASCII 指令 |
| `utils.py`            | 實用轉換工具：十進位轉 ASCII、32bit 拆段處理 |
| `example_usage.py`    | 各種用法示範（M點、D點、32bit 寫入） |
| `README.md`           | 英文版說明 |
| `README.zh-TW.md`     | 繁體中文版說明（本檔） |

---

## 🚀 快速範例

```python
from mc_protocol_rw import McProtocolRW
from utils import dec_to_ascii_hex_list, dec32_to_Dword_ascii

mc = McProtocolRW()

# 寫入 M0 ~ M3（對應接點開關）
cmd1 = mc.commant_batch('M0', [1, 0, 1, 1])

# 寫入 D100 = 10、D101 = 20（整數 → ASCII HEX）
cmd2 = mc.commant_random(['D100', 'D101'], dec_to_ascii_hex_list([10, 20]))

# 寫入 32bit 整數：30000000 → D11（低位）+ D10（高位）
cmd3 = mc.commant_random(['D11', 'D10'], dec32_to_Dword_ascii([30000000]))
