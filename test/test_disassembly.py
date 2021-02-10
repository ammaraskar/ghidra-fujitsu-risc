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
        (b'\xA5\xF4', 'ADD2 #0xf, R4')
    ]

    def test_single_opcodes(self):
        for i, (bytecode, disassembly) in enumerate(self.SINGLE_OPCODE_CASES):
            with self.subTest(msg=disassembly):
                actual_disassembly = disassemble(bytecode)
                self.assertIn(disassembly.encode(), actual_disassembly)

if __name__ == '__main__':
    unittest.main()
