import unittest
import subprocess
from pathlib import Path


TEST_DIRECTORY = Path(__file__).resolve().parent
TEST_HARNESS = TEST_DIRECTORY / 'bin' / 'test_harness'


def disassemble(bytecode):
    return subprocess.check_output([TEST_HARNESS], input=bytecode)

class DisassemblyTest(unittest.TestCase):
    def test_noop(self):
        single_noop = b'\x9F\xA0'
        disassembly = disassemble(single_noop)
        self.assertIn(b'NOP', disassembly)

    def test_add(self):
        add_r3_r9 = b'\xA6\x39'
        disassembly = disassemble(add_r3_r9)
        self.assertIn(b'ADD R3, R9', disassembly)

    def test_add_with_immediate(self):
        add_5_r2 = b'\xA4\x52'
        disassembly = disassemble(add_5_r2)
        self.assertIn(b'ADD #0x5, R2', disassembly)

if __name__ == '__main__':
    unittest.main()
