from mc_protocol_rw import McProtocolRW
from utils import dec_to_ascii_hex_list, dec32_to_Dword_ascii

# 建立實體
mc = McProtocolRW()

# === 1. Batch Write (M點) ===
batch_cmd = mc.commant_batch('M0', [1, 0, 1, 1])
print("Batch Write to M0~M3:", batch_cmd)

# === 2. Random Write (D點，不拆段，直接轉ascii) ===
dec_values = [10, 20]
ascii_values = dec_to_ascii_hex_list(dec_values)
cmd_random = mc.commant_random(['D100', 'D101'], ascii_values)
print("Random Write to D100, D101:", cmd_random)

# === 3. Write 32-bit 整數到 PLC D記憶體（拆成高低位）===
# 寫入 30000000 → D11（low）、D10（high）
ascii_split = dec32_to_Dword_ascii([30000000]) #30000000
cmd_dword = mc.commant_random(['D10','D11'], ascii_split)
print("Write 32-bit to D10, D11:\n", cmd_dword)


###
def dec_to_ascii_hex(dec_val, total_len=8):
    return mc.str_to_ascii(f"{abs(dec_val):X}", total_len)

def create_move_command(value, cmd_tags):
    dsp_ascii = dec_to_ascii_hex(value)
    print(dsp_ascii)

    # spd_ascii = mc.str_to_ascii(spd_value, 8)
    # print(spd_ascii)
    return mc.commant_random(cmd_tags, [
        dsp_ascii[12:24], dsp_ascii[0:11]#,
        # spd_ascii[0:11], spd_ascii[12:24]
    ])

cmd_dword = create_move_command(30000000, ['D10','D11'])
print(cmd_dword)