import unittest
import subprocess
from pathlib import Path


TEST_DIRECTORY = Path(__file__).resolve().parent
TEST_HARNESS = TEST_DIRECTORY / 'bin' / 'test_harness'


def disassemble(bytecode):
    return subprocess.check_output([TEST_HARNESS], input=bytecode)


class DisassemblyTest(unittest.TestCase):
    SINGLE_OPCODE_CASES = [
        (b'\x9F\xA0', 'NOP'),
        (b'\xA6\x39', 'ADD R3, R9'),
        (b'\xA4\x52', 'ADD #0x5, R2'),
        (b'\xA5\xF4', 'ADD2 #-0x1, R4'),
        (b'\xA7\x0F', 'ADDC R0, R15'),
        (b'\xA2\x69', 'ADDN R6, R9'),
        (b'\xA0\xF2', 'ADDN #0xf, R2'),
        (b'\xA1\x53', 'ADDN2 #0x5, R3'),
        (b'\xAC\x85', 'SUB R8, R5'),
        (b'\xAD\xC7', 'SUBC R12, R7'),
        (b'\xAE\xED', 'SUBN R14, R13'),
        (b'\xAA\x12', 'CMP R1, R2'),
        (b'\xA8\x33', 'CMP #0x3, R3'),
        (b'\xA9\xD3', 'CMP2 #-0x3, R3'),
        (b'\x82\x23', 'AND R2, R3'),
        (b'\x84\x34', 'AND R3, @R4'),
        (b'\x85\x45', 'ANDH R4, @R5'),
        (b'\x86\x56', 'ANDB R5, @R6'),
        (b'\x92\x78', 'OR R7, R8'),
        (b'\x94\x89', 'OR R8, @R9'),
        (b'\x95\x9A', 'ORH R9, @R10'),
        (b'\x96\xAB', 'ORB R10, @R11'),
        (b'\x9A\xBC', 'EOR R11, R12'),
        (b'\x9C\xCD', 'EOR R12, @R13'),
        (b'\x9D\xDE', 'EORH R13, @R14'),
        (b'\x9E\xEF', 'EORB R14, @R15'),
        (b'\x80\xF0', 'BANDL #0xf, R0'),
        (b'\x81\x01', 'BANDH #0x0, R1'),
        (b'\x90\x12', 'BORL #0x1, R2'),
        (b'\x91\x23', 'BORH #0x2, R3'),
        (b'\x98\x34', 'BEORL #0x3, R4'),
        (b'\x99\x45', 'BEORH #0x4, R5'),
        (b'\x88\x56', 'BTSTL #0x5, R6'),
        (b'\x89\x67', 'BTSTH #0x6, R7'),
        (b'\xAF\x78', 'MUL R7, R8'),
        (b'\xAB\x89', 'MULU R8, R9'),
        (b'\xBF\x9A', 'MULH R9, R10'),
        (b'\xBB\xAB', 'MULUH R10, R11'),
        (b'\x97\x4C', 'DIV0S R12'),
        (b'\x97\x5D', 'DIV0U R13'),
        (b'\x97\x6E', 'DIV1 R14'),
        (b'\x97\x7F', 'DIV2 R15'),
        (b'\x9F\x60', 'DIV3'),
        (b'\x9F\x70', 'DIV4S'),
        (b'\xB6\xA0', 'LSL R10, R0'),
        (b'\xB4\xB1', 'LSL #0xb, R1'),
        (b'\xB5\xC2', 'LSL2 #0xc, R2'),
        (b'\xB2\xD3', 'LSR R13, R3'),
        (b'\xB0\xE4', 'LSR #0xe, R4'),
        (b'\xB1\xF5', 'LSR2 #0xf, R5'),
        (b'\xBA\x06', 'ASR R0, R6'),
        (b'\xB8\x17', 'ASR #0x1, R7'),
        (b'\xB9\x28', 'ASR2 #0x2, R8'),
        (b'\x9F\x83\xDE\xAD\xBE\xEF', 'LDI:32 #0xdeadbeef, R3'),
        (b'\x9B\xCA\xAF\xEB', 'LDI:20 #0xcafeb, R10'),
        (b'\xCC\xAF', 'LDI:8 #0xca, R15'),
        (b'\x04\x18', 'LD @R1, R8'),
        (b'\x00\x29', 'LD @(R13 + R2), R9'),
        (b'\x28\x23', 'LD @(R14 + 4 * -0x7e), R3'),
        (b'\x03\xF4', 'LD @(R15 + 4 * 0xf), R4'),
        (b'\x07\x05', 'LD @R15+, R5'),
        (b'\x07\x83', 'LD @R15+, USP'),
        (b'\x07\x90', 'LD @R15+, PS'),
        (b'\x05\x46', 'LDUH @R4, R6'),
        (b'\x01\x57', 'LDUH @(R13 + R5), R7'),
        (b'\x4F\xD6', 'LDUH @(R14 + 2 * -0x3), R6'),
        (b'\x06\x68', 'LDUB @R6, R8'),
        (b'\x02\x79', 'LDUB @(R13 + R7), R9'),
        (b'\x6F\xD6', 'LDUB @(R14 + -0x3), R6'),
        (b'\x14\x8A', 'ST R10, @R8'),
        (b'\x10\x9B', 'ST R11, @(R13 + R9)'),
        (b'\x3F\x97', 'ST R7, @(R14 + 4 * -0x7)'),
        (b'\x13\xBC', 'ST R12, @(R15 + 4 * 0xb)'),
        (b'\x17\x03', 'ST R3, @-R15'),
        (b'\x17\x83', 'ST USP, @-R15'),
        (b'\x17\x90', 'ST PS, @-R15'),
    ]

    def test_single_opcodes(self):
        for i, (bytecode, disassembly) in enumerate(self.SINGLE_OPCODE_CASES):
            with self.subTest(msg=disassembly):
                actual_disassembly = disassemble(bytecode)
                self.assertIn(disassembly.encode(), actual_disassembly)


if __name__ == '__main__':
    unittest.main()
