# utils.py
"""
Utility functions for Mitsubishi PLC data handling
Author: bh.hong
Date: 2025-April
"""

from mc_protocol_rw import McProtocolRW

# 建立共用實體
mc = McProtocolRW()

def dec_to_ascii_hex_list(values, length=4):
    """將十進位整數轉為 ASCII 格式 hex 字串（不拆段）"""
    ascii_list = []
    for v in values:
        hex_str = f"{v:X}"
        ascii_list.append(mc.str_to_ascii(hex_str, length))
    return ascii_list

def dec32_to_Dword_ascii(dec_values):
    """
    將 32-bit 十進位數轉為兩段 16-bit（高低位）ASCII Hex字串。
    傳回格式為 [D_Low, D_High]
    """
    split_ascii = []
    for val in dec_values:
        hex32 = f"{val:08X}"  # 保留8位16進位
        low_word = hex32[4:]  # 後4位 → D_Low
        high_word = hex32[:4] # 前4位 → D_High
        split_ascii.append(mc.str_to_ascii(low_word, 4))  # 低位
        split_ascii.append(mc.str_to_ascii(high_word, 4)) # 高位
    return split_ascii
