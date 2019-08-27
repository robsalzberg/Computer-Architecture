"""CPU functionality."""

import sys

# HLT = 0b00000001
# LDI = 0b10000010
# PRN = 0b01000111
# MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
            # Each index is a byte
        # RAM stores 256 bytes
        self.ram = [0] * 256

        # Each index in reg is a register
        self.reg = [0] * 8

        # Store the Program Counter
        self.PC = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program):
        """Load a program into memory."""
        address = 0

        try:
            # open the program specified by the second command line argument
            with open(sys.argv[1]) as f:
                # for each line in the file
                for line in f:
                    # check if it starts with a binary number
                    if line[0].startswith('0') or line[0].startswith('1'):
                        # only use the first (non-commented) part of the instruction
                        binary = line.split("#")[0]
                        # remove any white space
                        binary = binary.strip()
                        # convert to binary and store it in RAM
                        self.ram[address] = int(binary, 2)
                        address += 1
        except:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found.")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] += self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f'TRACE: %02X | %02X %02X %02X |' % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(' %02X' % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

        running = True

        while running:
            # It needs to read the memory address that's stored in register `PC`, and store
            # that result in `IR`, the _Instruction Register_. This can just be a local
            # variable in `run()`.
            IR = self.ram[self.pc]

            # Using `ram_read()`,read the bytes at `PC+1` and `PC+2` from RAM into variables
            # `operand_a` and `operand_b` in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # Then, depending on the value of the opcode, perform the actions needed for the
            # instruction per the LS-8 spec.
            if IR == HLT:
                running = False
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            else:
                print("Unknown instruction.")
