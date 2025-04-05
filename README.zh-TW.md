# MC Protocol 通訊模組（Python版）

本模組使用 Python 實作 Mitsubishi PLC 的 MC Protocol 通訊格式（ASCII 3C Frame），支援 Bit/Word 裝置的 Batch 與 Random 寫入，適用於透過串口或網路與 PLC 建立通訊的應用情境。

## ✨ 特色功能

- 支援 Batch / Random 寫入（M、D、Y、W點）
- 自動產生 Frame Header、Command Code、CRC 校驗碼
- 可應用於 IPC + PLC 控制架構，實現 Python 控制伺服馬達動作

## 📦 檔案說明

| 檔案名稱        | 功能說明 |
|----------------|----------|
| `mc_protocol_rw.py` | 通訊指令封裝模組，提供產生 MC Protocol 封包功能 |
| `example_usage.py` | 示範如何使用模組與 PLC 進行 Batch 或 Random 寫入 |

## 🚀 使用方式

```python
from mc_protocol_rw import McProtocolRW

mc = McProtocolRW()

# Batch 寫入 M0~M3 = [1,0,1,1]
cmd = mc.commant_batch('M0', [1,0,1,1])

# Random 寫入 D100, D101 = [10, 20]
cmd = mc.commant_random(['D100','D101'], ['31 30', '32 30'])  # ASCII for 10, 20
