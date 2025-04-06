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
        self.end_code = self.cr+' '+self.lf
        #Frame ID No. as below
        self.frame_id = '46 39' #F9(3C frame)
        self.ststion_no= '30 30'
        self.network_no= '30 30'
        self.pc_no='46 46'
        self.self_ststion_no= '30 30'
        frame_code_component = [
            self.frame_id,
            self.ststion_no,
            self.network_no,
            self.pc_no,
            self.self_ststion_no
        ]
        self.frame_code = ' '.join(filter(None, frame_code_component)) #將所有的字串組合起來

        #指令代碼
        self.batch_read = 401
        self.batch_write = 1401

    def device_code_defind (self, device_code):
        """ 取得裝置代碼（例：'M', 'D'） """
        start = format(ord('*'), 'X')
        code_with_0x = format(ord(device_code), 'X')
        device_code = code_with_0x + ' ' + start
        #print(device_code)
        return device_code

    def str_to_ascii (self, address_int, length):
        """定義from int to hex(Ascii),給定int,格子數"""
        i=0
        arr = list(str(address_int)) #int >>str >>矩陣
        address_arr = ['0']*length #定義一個矩陣裝入address
        for i in range (len(arr)) : #前面補0
            address_arr[length-1-i] = arr[len(arr)-1-i]
        #print(address_arr)

        #矩陣 from ascii 一個一個 to Hex
        address_ascii = [30]* length #避免錯誤定預設0 >> ascii=30
        for i in range (length):
            address_ascii[length-1-i] = format(ord(address_arr[length-1-i]), 'X')

        address_str = ' '

        return address_str.join(address_ascii) #Convert a list to string out put

    def point_status_qty (self, point_ststus):
        """點位輸狀態；配合點位數量(實際輸出為先數量再狀態)"""
        #point_ststus = [0, 1] #debug測試點
        point_qty_int = len(point_ststus)
        point_qty_in_hex = self.str_to_ascii(point_qty_int, 4)

        #list transfor from int to Ascii
        point_ststus_ascii = [1]*point_qty_int #避免錯誤定預設1個，status in '0'

        for i in range (point_qty_int):
            point_ststus_ascii[i] = format(ord(str(point_ststus[i])), 'X')

        point_in_str = ' '

        return point_qty_in_hex+' '+point_in_str.join(point_ststus_ascii)

    def data_qty_unit (self, word):
        """
            當點位是D記存器且傳送內容為word時
            1. 傳入矩陣元素個數，自動生出點位數量
        """
        point_qty_int = len(word)
        point_qty_in_hex = self.str_to_ascii(point_qty_int, 4)

        i = 0
        data_qty_and_words = ''

        for i in range (point_qty_int) :
            # 將 word[i] 轉為 4 字元長的 ASCII 字串，並加到結果字串中
            ascii_str = f"0x{word[i]:X}"[2:]
            data_qty_and_words = data_qty_and_words + f' {self.str_to_ascii(ascii_str, 4)}'
        return point_qty_in_hex+data_qty_and_words

    def check_sum(self, data):
        """ 求CRC校驗碼 """
        sumtest = 0 # sumtest intial
        d = [int(x, 16) for x in data.split(' ')] # 將str轉list，並以int儲存
        for value in d:  # 直接遍歷元素
            sumtest += value  # 累加每個元素的值

        code1 = f"{sumtest:X}"[-2]  # 將轉為 ASCII
        code2 = f"{sumtest:X}"[-1]  # 將轉為 ASCII
        #print (code1) #印出來確認values

        check_code = format(ord(code1), "x") +' '+ format(ord(code2), "x")

        return check_code

    def commant_batch (self, headdevice, values):
        """ batch 命令"""
        crc_code = None
        end_code =None
        if headdevice[0] == 'M':
            # print('Batch write data in bit M, Y...')
            command_code= self.str_to_ascii(14010001, 8) # 1401, 0001
            # 取得裝置代碼（例：'M', 'D'）
            device_code = self.device_code_defind(headdevice[0])

            # 將裝置地址轉為 ASCII 字串（取 headdevice 後面字元，共 6 位）
            device_address = self.str_to_ascii (headdevice[1:], 6)
            point_qty_va_ststus = self.point_status_qty(values) #self.point_status_qty([1,1])
            crc_components = [
                self.frame_code,
                command_code,
                device_code,
                device_address,
                point_qty_va_ststus
            ]
            code_crc = ' '.join(filter(None, crc_components)) #將所有的字串組合起來
            crc_code = self.check_sum (code_crc)
            end_code = self.cr+' '+self.lf

        elif headdevice[0] == 'D':
            # print ('Batch write data in word D, W...')
            command_code= self.str_to_ascii(14010000, 8) # 1401, 0000
            # 取得裝置代碼（例：'M', 'D'）
            device_code = self.device_code_defind(headdevice[0])

            # 將裝置地址轉為 ASCII 字串（取 head_device 後面字元，共 6 位）
            device_address = self.str_to_ascii (headdevice[1:], 6)
            point_qty_va_ststus = self.data_qty_unit(values) #Point_qty_and_data
            crc_components=[
                self.frame_code,
                command_code,
                device_code,
                device_address,
                point_qty_va_ststus
            ]
            code_crc = ' '.join(filter(None, crc_components)) #將所有的字串組合起來
            crc_code = self.check_sum (code_crc)
            end_code = self.cr+' '+self.lf

        else :
            print ('Err function not yet define')
            # pass
        crc_components = [
            self.enq_code,
            self.frame_code,
            command_code,
            device_code,
            device_address,
            point_qty_va_ststus,
            crc_code,
            end_code
        ]
        commant_code = ' '.join(filter(None, crc_components)) #將所有的字串組合起來
        # print ( commant_code )
        return bytes.fromhex( commant_code )

    def commant_random (self, headdevice, values):
        """ Random_write """
        i = 0
        commant_code = None
        if len(headdevice) != len(values): #確保點位數量，與變數數量一致
            print('Err Qty in points and values notmatch')
            exit()
        else :
            pass

        #Writing data in bit units
        if headdevice[0][0] == 'M': #目前針對M機碼
            # print('Random writing data in bit M, Y...')
            command_code= self.str_to_ascii(14020001, 8) # 1402, 0001
            qty_of_points = self.str_to_ascii (len(headdevice), 2 )
            word_pack = ''

            for i, device in enumerate(headdevice):
                # 取得裝置代碼（例：'M', 'D'）
                device_code = self.device_code_defind(device[0])
                device_address = self.str_to_ascii(device[1:], 6) #address6位
                device_ststus = self.str_to_ascii(values[i], 2)
                word_pack = word_pack +' ' +device_code + ' '+device_address +' '+device_ststus

            crc_components = [
                self.frame_code,
                command_code,
                qty_of_points
            ]
            code_crc = ' '.join(filter(None, crc_components)) + word_pack
            crc_code = self.check_sum (code_crc)
            commant_code = self.enq_code+' '+code_crc+' '+crc_code+' '+self.end_code

        elif headdevice[0][0] == 'D' :
            # print('Random writing data in word D, W...')
            command_code= self.str_to_ascii(14020000, 8) #1402, 0001
            qty_of_words = self.str_to_ascii (len(headdevice), 2 )
            qty_of_double_words = self.str_to_ascii (0, 2 )
            word_pack = ''

            for i, device in enumerate(headdevice):
                # 取得裝置代碼（例：'M', 'D'）
                device_code = self.device_code_defind(device[0])
                device_address = self.str_to_ascii(device[1:], 6)  # address 6 位
                device_ststus = values[i]  # 已經是 Ascii
                word_pack = word_pack +' ' +device_code +' ' +device_address +' ' +device_ststus

            crc_components = [
                self.frame_code,
                command_code,
                qty_of_words,
                qty_of_double_words
            ]
            code_crc = ' '.join(filter(None, crc_components)) + word_pack
            crc_code = self.check_sum (code_crc)
            commant_code = self.enq_code+' '+code_crc+' '+crc_code+' '+self.end_code

        else :
            pass

        return bytes.fromhex( commant_code )
