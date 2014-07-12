class MessageBuilder():
    base_address_0 = 0
    base_address_1 = 3
    base_address_2 = 7
    base_address_3 = 2
    base_address_4 = 10

    def build_simple_message(self, action, address, subid, cmdparam1, cmdparam2, command):
        return action + ',' + str(cmdparam1) + ',' + str(cmdparam2) + ',' + str(address) + ',' + str(
            command) + ',' + str(
            self.base_address_0) + ',' + str(self.base_address_1) + ',' + str(self.base_address_2) + ',' + str(
            self.base_address_3) + ',' + str(self.base_address_4) + ',' + str(subid) + '|'
