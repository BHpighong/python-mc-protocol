"""
目的 : 產出MC_Protocol 的指令
file name : mc_protocol_rw.py
Author: bh.hong
"""

class McProtocolRW:
    """ 產生McProtocol所需要的資訊 """
    def __init__(self):
        super().__init__()

        #Contol Code
        self.enq_code ='05' #ENQ Code // Contol Code
        self.cr = '0D' #CR
        self.lf = '0A' #LF
        self.end_code = f"{self.cr} {self.lf}" #self.cr+' '+self.lf

        #Frame ID No. as below
        self.frame_id = '46 39' #F9(3C frame)
        self.station_no= '30 30'
        self.network_no= '30 30'
        self.pc_no='46 46'
        self.self_station_no= '30 30'

        self.frame_code = ' '.join([
            self.frame_id,
            self.station_no,
            self.network_no,
            self.pc_no,
            self.self_station_no
        ])

        #指令代碼
        # self.batch_read = '0401'
        # self.batch_write = '1401'

    def device_code_define (self, device_code):
        """ 取得裝置代碼（例：'M', 'D'） """
        return f"{format(ord(device_code), 'X')} {format(ord('*'), 'X')}"

    def to_ascii_hex_string (self, address_int, length):
        """定義from int to hex(Ascii),給定int,格子數"""
        str_hex_ascii = str(address_int).zfill(length) #int >>str >>補0
        #將字串轉為ascii
        return ' '.join([format(ord(code), 'X') for code in str_hex_ascii])

    def point_status_qty (self, point_status):
        """點位輸狀態；配合點位數量(實際輸出為先數量再狀態)"""
        qty_in_ascii = self.to_ascii_hex_string(len(point_status), 4)
        point_status_ascii = ' '.join([format(ord(str(s)), 'X') for s in point_status])

        return f"{qty_in_ascii} {point_status_ascii}"

    def data_qty_unit (self, words):
        """ 當點位是D記存器且傳送內容為word時，傳入矩陣元素個數，自動生出點位數量 """
        point_qty_ascii = self.to_ascii_hex_string(len(words), 4)
        data_ascii = ' '.join([self.to_ascii_hex_string(f"{w:X}"[2:], 4) for w in words])

        return f"{point_qty_ascii} {data_ascii}"

    def check_sum(self, data):
        """ 求CRC校驗碼 """
        sum_check_code = sum(int(x, 16) for x in data.split(' ')) # 將list的int加總
        code = f"{sum_check_code:X}"[-2:]
        # print(' '.join([format(ord(c), "x") for c in code]))
        return ' '.join([format(ord(c), "x") for c in code])

    def build_command_payload(self, headdevice, values, command_code):
        """ pay load building """
        dev_type = headdevice[0]
        device_code = self.device_code_define(dev_type)
        device_address = self.to_ascii_hex_string(headdevice[1:], 6)
        data_payload = self.pay_load_style(dev_type, values, command_code)

        payload = ' '.join([
            self.frame_code,
            self.to_ascii_hex_string(command_code, 8),
            device_code,
            device_address,
            data_payload
        ])

        return payload, device_code, device_address, data_payload

    def pay_load_style(self, dev_type, values, command_code):
        """" pay load style """
        if str(command_code) == '04010001':
            return self.to_ascii_hex_string(values, 4)

        elif str(command_code) == '14010001':
            if dev_type == 'M':
                return self.point_status_qty(values)
            elif dev_type == 'D':
                return self.data_qty_unit(values)
        else:
            raise ValueError("Unsupported device type")

    def format_packet(self, payload, device_code, device_address, data_payload, command_code):
        """ formate fine tuning """
        crc = self.check_sum(payload)
        packet = ' '.join([
            self.enq_code,
            self.frame_code,
            self.to_ascii_hex_string(command_code, 8),
            device_code,
            device_address,
            data_payload,
            crc,
            f"{self.cr} {self.lf}"
        ])
        return bytes.fromhex(packet)

    def command_batch(self, headdevice, values):
        """ batch 命令 """
        command_code = 14010001
        payload, device_code, device_address, data_payload = self.build_command_payload(headdevice,
                                                                                    values,
                                                                                    command_code
                                                                                    )
        return self.format_packet(payload, device_code, device_address, data_payload, command_code)

    def build_random_write_payload(self, headdevices, values, is_bit=True):
        """ Build payload for random write command """
        if len(headdevices) != len(values):
            raise ValueError("Number of headdevices and values must match")

        if is_bit:
            command_code = '14020001'
            qty = self.to_ascii_hex_string(len(headdevices), 2)
            word_pack = ''
            for i, device in enumerate(headdevices):
                device_code = self.device_code_define(device[0])
                device_address = self.to_ascii_hex_string(device[1:], 6)
                status_ascii = self.to_ascii_hex_string(values[i], 2)
                word_pack += f" {device_code} {device_address} {status_ascii}"
            crc_components = ' '.join([self.frame_code,
                                       self.to_ascii_hex_string(command_code, 8),
                                       qty]) + word_pack
        else:
            command_code = '14020000'
            qty_words = self.to_ascii_hex_string(len(headdevices), 2)
            qty_dwords = self.to_ascii_hex_string(0, 2)
            word_pack = ''
            for i, device in enumerate(headdevices):
                device_code = self.device_code_define(device[0])
                device_address = self.to_ascii_hex_string(device[1:], 6)
                word_pack += f" {device_code} {device_address} {values[i]}"
            crc_components = ' '.join([self.frame_code,
                                       self.to_ascii_hex_string(command_code, 8),
                                       qty_words, qty_dwords]) + word_pack

        crc = self.check_sum(crc_components)
        packet = f"{self.enq_code} {crc_components} {crc} {self.end_code}"
        return bytes.fromhex(packet)

    def command_random(self, headdevices, values):
        """ Random_write """
        is_bit = headdevices[0][0] == 'M'
        return self.build_random_write_payload(headdevices, values, is_bit)

    def command_batch_read (self, headdevice, values):
        """ batch 讀取命令"""
        command_code = '04010001' #0401, 0001
        cmd_result= self.build_command_payload(headdevice,
                                               values,
                                               command_code)

        payload, device_code, device_address, data_payload = cmd_result
        return self.format_packet(payload, device_code, device_address, data_payload, command_code)
