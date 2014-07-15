class MessageBuilder():
    base_address_0 = 0
    base_address_1 = 3
    base_address_2 = 7
    base_address_3 = 2
    base_address_4 = 10
    send_repeats = 7
    pair_repeats = 10


    def build_simple_message(self, action, repeat, address, subid, cmdparam1, cmdparam2, command):
        m = self.__build_lw_msg(address, subid, cmdparam1, cmdparam2, command)
        r = self.__build_msg_header(action, repeat) + ',' + m + '|'
        return r


    def __build_lw_msg(self, address, subid, cmdparam1, cmdparam2, command):
        return str(cmdparam1) + ',' + str(cmdparam2) + ',' + str(
            address) + ',' + str(
            command) + ',' + str(
            self.base_address_0) + ',' + str(self.base_address_1) + ',' + str(self.base_address_2) + ',' + str(
            self.base_address_3) + ',' + str(self.base_address_4) + ',' + str(subid)


    def __build_msg_header(self, action, repeat):
        return action + ',' + str(repeat)


    def get_on(self, device):
        return self.__build_msg_header('SEND', self.send_repeats) + ',' + self.__build_lw_msg(device.address,
                                                                                              device.subid, 0, 0,
                                                                                              1) + '|'


    def get_off(self, device):
        return self.__build_msg_header('SEND', self.send_repeats) + ',' + self.__build_lw_msg(device.address,
                                                                                              device.subid, 0, 0,
                                                                                              0) + '|'


    def get_pair(self, device):
        return self.__build_msg_header('PAIR', self.pair_repeats) + ',' + self.__build_lw_msg(device.address,
                                                                                              device.subid, 0, 0,
                                                                                              1) + '|'


    def get_unpair(self, device):
        return self.__build_msg_header('PAIR', self.pair_repeats) + ',' + self.__build_lw_msg(device.address,
                                                                                              device.subid, 0, 0,
                                                                                              0) + '|'