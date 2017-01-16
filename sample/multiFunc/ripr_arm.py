from unicorn import *
from unicorn.arm_const import *

import struct
class arm_test(object):
    def __init__(self):
        self.mu =  Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.code_0 = '00482de904b08de208d04de208000be50c100be518009fe5a2ffffeb08301be50c201be5920303e00300a0e104d04be20088bde8'.decode('hex') 
        self.code_1 = '00482de904b08de208d04de208000be50c100be518009fe594ffffeb08201be50c301be5033082e00300a0e104d04be20088bde8'.decode('hex') 
        self.code_2 = '30482de90cb08de22c009fe589ffffeb0210a0e30100a0e3eaffffeb0040a0e10410a0e30300a0e3d8ffffeb0030a0e1033084e00300a0e13088bde8'.decode('hex') 

        self.data_0 = '7f454c4601010100000000000000000002002800010000003c03010034000000981c00000002000534002000090028001e001b0001000070fc050000fc050100fc05010008000000080000000400000004000000060000003400000034000100340001002001000020010000050000000400000003000000540100005401010054010100130000001300000004000000010000000100000000000000000001000000010008060000080600000500000000000100010000000c0f00000c0f02000c0f02002001000024010000060000000000010002000000180f0000180f0200180f0200e8000000e80000000600000004000000040000006801000068010100680101004400000044000000040000000400000051e574640000000000000000000000000000000000000000060000001000000052e574640c0f00000c0f02000c0f0200f4000000f400000004000000010000002f6c69622f6c642d6c696e75782e736f2e330000040000001000000001000000474e550000000000030000000200000000000000040000001400000003000000474e55006424f7c748193d37bf91b5c15959f5136b2234de0300000002000000010000000500000000480221020000000300000005000000117b9c7cb82b6b157ded110f2f4e3df6000000000000000000000000000000002f0000000000000000000000200000000b00000000000000000000001200000016000000000000000000000012000000100000000000000000000000120000001d000000000000000000000012000000006c6962632e736f2e3600707574730061626f7274007072696e7466005f5f6c6962635f73746172745f6d61696e005f5f676d6f6e5f73746172745f5f00474c4942435f322e3400000000000200020002000200010001000100000010000000000000001469690d000002003e0000000000000020100200150100000c100200160300001010020016020000141002001605000018100200160100001c1002001604000008402de9230000eb0880bde804e02de504e09fe50ee08fe008f0bee5040d010000c68fe210ca8ce204fdbce500c68fe210ca8ce2fcfcbce500c68fe210ca8ce2f4fcbce500c68fe210ca8ce2ecfcbce500c68fe210ca8ce2e4fcbce500b0a0e300e0a0e304109de40d20a0e104202de504002de510c09fe504c02de50c009fe50c309fe5ebffffebf0ffffebb0050100140501005005010014309fe514209fe503308fe0022093e7000052e31eff2f01e3ffffea780c0100200000001c309fe51c009fe5003043e0060053e31eff2f9110309fe5000053e31eff2f0113ff2fe12f1002002c1002000000000024109fe524009fe5001041e04111a0e1a11f81e0c110b0e11eff2f0110309fe5000053e31eff2f0113ff2fe12c1002002c1002000000000010402de918409fe50030d4e5000053e31080bd18dfffffeb0130a0e30030c4e51080bde82c10020028009fe5003090e5000053e30000001ae2ffffea18309fe5000053e3fbffff0a10402de933ff2fe11040bde8dbffffea140f02000000000000482de904b08de208d04de208000be50c100be518009fe5a2ffffeb08301be50c201be5920303e00300a0e104d04be20088bde8c005010000482de904b08de208d04de208000be50c100be518009fe594ffffeb08201be50c301be5033082e00300a0e104d04be20088bde8d005010030482de90cb08de22c009fe589ffffeb0210a0e30100a0e3eaffffeb0040a0e10410a0e30300a0e3d8ffffeb0030a0e1033084e00300a0e13088bde8e005010000482de904b08de210d04de210000be514100be5e9ffffeb08000be508101be510009fe570ffffeb0030a0e30300a0e104d04be20088bde8f0050100f0472de94c609fe54c509fe506608fe005508fe0056046e00070a0e10180a0e10290a0e159ffffeb4661b0e1f087bd080040a0e3014084e2043095e40920a0e10810a0e10700a0e133ff2fe1060054e1f7ffff1af087bde8ac090100a40901001eff2fe108402de90880bde801000200496e736964652066756e635f330a0000496e736964652066756e635f320a0000496e736964652066756e635f310a0000416e737765723a2025640a0040fdff7f0100000000000000'.decode('hex') 

        self.mu.mem_map(0x10000L,0x200000)
        self.mu.mem_map(0x7ffff000,0x200000)

        self.mu.mem_write(0x10000L, self.data_0)
        self.mu.mem_write(0x10464L, self.code_0)
        self.mu.mem_write(0x1049cL, self.code_1)
        self.mu.mem_write(0x104d4L, self.code_2)

        self.hookdict = {66744L: 'hook_puts', 66688L: 'hook_puts', 66788L: 'hook_puts'}
    def hook_puts(self):
        pass
    def _start_unicorn(self, startaddr):
        try:
            self.mu.emu_start(startaddr, 0)
        except Exception as e:
            if self.mu.reg_read(UC_ARM_REG_PC) == 4:
                return
            retAddr = self.mu.reg_read(UC_ARM_REG_LR)
            if retAddr in self.hookdict.keys():
                getattr(self, self.hookdict[retAddr])()
                self._start_unicorn(retAddr)
            else:
                raise e
    def run(self):
        self.mu.reg_write(UC_ARM_REG_SP, 0x7fffffff)
        self.mu.reg_write(UC_ARM_REG_LR, 0x4)
        self._start_unicorn(0x104d4)
        return self.mu.reg_read(UC_ARM_REG_R0)
