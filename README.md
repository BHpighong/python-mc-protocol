# python-mc-protocol
A Python-based command generator for Mitsubishi PLC using MC Protocol (ASCII mode), supporting batch &amp; random write for M/D devices

# 🧠 Mitsubishi PLC Command Generator (Python + MC Protocol)

This project provides a Python-based command generator for **Mitsubishi PLC communication via MC Protocol (ASCII mode)**.

It is designed specifically for **Python developers working with PLCs**, as well as **automation engineers looking to script control sequences in Python**.

---

## 🔧 Features

- ✅ Generate MC Protocol-compliant command frames (ASCII 3C frame)
- ✅ Supports **Batch Write** and **Random Write** for both Bit (M/Y) and Word (D/W) devices
- ✅ Accepts **decimal inputs** and auto-converts to ASCII-encoded hex
- ✅ Compatible with **serial or TCP communication**
- ✅ Utility functions for **32-bit word splitting** (D10/D11, D20/D21, etc.)
- ✅ Easy to integrate into **PC-based automation / servo control systems**

---

## 📁 File Structure

| File               | Description |
|--------------------|-------------|
| `mc_protocol_rw.py` | Core class for command generation using MC Protocol |
| `utils.py`          | Helper functions for converting decimal values into PLC-compatible formats |
| `example_usage.py`  | Demonstrates batch and random write with decimal and 32-bit data |
| `README.zh-TW.md`   | Traditional Chinese version of this README |

---

## 🚀 Quick Example

```python
from mc_protocol_rw import McProtocolRW
from utils import dec_to_ascii_hex_list, dec32_to_Dword_ascii

mc = McProtocolRW()

# Batch write to M0 ~ M3
cmd1 = mc.commant_batch('M0', [1, 0, 1, 1])

# Random write to D100 = 10, D101 = 20
cmd2 = mc.commant_random(['D100', 'D101'], dec_to_ascii_hex_list([10, 20]))

# Write 32-bit value (30000000) into D10 (high), D11 (low)
cmd3 = mc.commant_random(['D10', 'D11'], dec32_to_Dword_ascii([30000000]))

