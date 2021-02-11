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
    ]

    def test_single_opcodes(self):
        for i, (bytecode, disassembly) in enumerate(self.SINGLE_OPCODE_CASES):
            with self.subTest(msg=disassembly):
                actual_disassembly = disassemble(bytecode)
                self.assertIn(disassembly.encode(), actual_disassembly)


if __name__ == '__main__':
    unittest.main()
