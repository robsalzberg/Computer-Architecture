"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

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
        self.PC = self.reg[0]
        # Store the Instruction Register
        # self.IR = self.reg[1]
        # Store the Memory Address Register
        # self.MAR = self.reg[2]
        # Store the Memory Data Register
        # self.MDR = self.reg[3]
        # Store the Flags
        # self.FL = self.reg[4]

        # self.reg[5] Reserved: Interrupt Mask
        # self.reg[6] Reserved: Interrupt Status
        # self.reg[7] Reserved: Stack Pointer
        # self.reg[8] Unassigned

    def __repr__(self):
        return f'RAM: {self.ram} \n Register: {self.reg}'

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        try:
            address = 0

            with open(program) as f:
                for line in f:
                    comment_split = line.split("#")

                    number = comment_split[0].strip()

                    if number == "":
                        continue
                    
                    value = int(number, 2)

                    self.ram_write(value, address)

                    address += 1

        except FileNotFoundError:
            print(f"{program} not found")
            sys.exit(2)
        
        if len(sys.argv) != 2:
            print(f"Please format the command like so: \n python3 ls8.py <filename>", file=sys.stderr)
            sys.exit(1)

        print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a]) * (self.reg[reg_b])
            return 2

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram[self.PC]

            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            # print(f"Operand A: {operand_a} Operand B: {operand_b}")
            # print(f"Register: {self.reg}")

            if IR == HLT:
                # halt the program
                running = False

            elif IR == LDI:
                # sets register to a value
                self.reg[operand_a] = operand_b
                self.PC += 2

            elif IR == PRN:
                # print the value at a register
                print(self.reg[operand_a])
                self.PC += 1

            elif IR == MUL:
                self.PC += self.alu("MUL", operand_a, operand_b)

            else:
                print(f"Unknown command: {IR}")
                sys.exit(1)
            
            self.PC += 1
