"""
File: example_usage.py
Author: bh.hong
"""

from mc_protocol_rw import McProtocolRW
from utils import dec_to_ascii_hex_list, dec32_to_Dword_ascii

# 建立實體
mc = McProtocolRW()

# === 1. Batch Write (M點) ===
batch_cmd = mc.command_batch('M100', [1, 1, 0, 0, 1, 1, 0, 0])
print("Batch Write to M100~M107\n:", batch_cmd)

# === 2. Batch Write (D點) ===
batch_cmd = mc.command_batch('D100', [6549, 4610, 4400])
print("Batch Write to M100~M107\n:", batch_cmd)

# === 2. Random Write (D點，不拆段，直接轉ascii) ===
dec_values = [550, 575]
ascii_values = dec_to_ascii_hex_list(dec_values)
cmd_random = mc.command_random(['D00', 'D01'], ascii_values)
print("Random Write to D100, D101:", cmd_random)

# === 3. Write 32-bit 整數到 PLC D記憶體（拆成高低位）===
# 寫入 30000000 → D11（low）、D10（high）
ascii_split = dec32_to_Dword_ascii([30000000]) #30000000
cmd_dword = mc.command_random(['D10','D11'], ascii_split)
print("Write 32-bit to D10, D11:\n", cmd_dword)
