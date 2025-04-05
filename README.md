# python-mc-protocol
A Python-based command generator for Mitsubishi PLC using MC Protocol (ASCII mode), supporting batch &amp; random write for M/D devices

# MC Protocol Command Generator for Mitsubishi PLC (Python)

This project provides a Python-based command generator for Mitsubishi PLC using the **MC Protocol (ASCII mode, 3C frame)**.  
It supports **Batch Write** and **Random Write** for bit/word devices such as `M`, `D`, `Y`, and `W`.

## 🔧 Features

- Support for batch and random write commands
- Compatible with bit-level (`M`, `Y`) and word-level (`D`, `W`) devices
- Generates MC Protocol-compliant frame headers, device addressing, and CRC checksum
- Easy to integrate into IPC-based automation systems or Python control interfaces

## 📦 Files

| File | Description |
|------|-------------|
| `mc_protocol_rw.py` | Main module that generates command frames according to MC Protocol |
| `example_usage.py`  | Sample usage showing how to send write commands to Mitsubishi PLC |

## 🚀 Usage Example

```python
from mc_protocol_rw import McProtocolRW

mc = McProtocolRW()

# Batch write M0~M3 to [1, 0, 1, 1]
cmd = mc.commant_batch('M0', [1, 0, 1, 1])

# Random write D100, D101 to 10, 20 (in ASCII)
cmd = mc.commant_random(['D100', 'D101'], ['31 30', '32 30'])  # ASCII for 10, 20
