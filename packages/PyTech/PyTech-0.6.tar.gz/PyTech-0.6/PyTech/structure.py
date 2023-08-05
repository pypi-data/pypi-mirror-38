import struct, inspect
from tkinter import *
def group(lst, n):
    return zip(*[lst[i::n] for i in range(n)])

class InputOutput:
    def __init__(self, bit=64, in_registries=1024, out_registries=1024):
        self.bytesize = bit
        self.funcs = dict()
        self.typ = "IO"
        if bit == 8:
            self.mbl = 'b'
            self.imbl = 'b'
        elif bit == 16:
            self.mbl = 'h'
            self.imbl = 'h'
        elif bit == 32:
            self.mbl = 'f'
            self.imbl = 'i'
        elif bit == 64:
            self.mbl = 'd'
            self.imbl = 'q'
        else:
            raise ValueError("'bit' must be 8, 16, 32, or 64")
        self.ireg = [struct.pack(self.mbl, 0) for x in range(in_registries)]
        self.oreg = [struct.pack(self.mbl, 0) for x in range(out_registries)]
        
    def set_input_registry(self, num, input_registry=9999):
        if type(num) == type(b''):
            if not struct.unpack(self.mbl, num)[0] > 2**self.bytesize:
                self.ireg[input_registry] = num
            else:
                raise ValueError("Integer cannot be greater than the max bits of the CPU")
        else:
            raise ValueError("Integer argument must be a bytes object (try using CPU.binForm)")

    def get_input_registry(self, input_registry=9999, unpacked=False):
        if unpacked == True:
            return self.binDeform(self.oreg[input_registry])
        else:
            return self.ireg[input_registry]


    def set_output_registry(self, num, output_registry=9999):
        if type(num) == type(b''):
            if not struct.unpack(self.mbl, num)[0] > 2**self.bytesize:
                self.oreg[output_registry] = num
            else:
                raise ValueError("Integer cannot be greater than the max bits of the CPU")
        else:
            raise ValueError("Integer argument must be a bytes object (try using CPU.binForm)")
            
    def get_output_registry(self, output_registry=9999, unpacked=False):
        if unpacked==True:
            return self.binDeform(self.oreg[output_registry])
        else:
            return self.oreg[output_registry]
        
    def input(self, output_registry, intype=1):
        if intype==0:
            try:
                self.oreg[output_registry] = struct.pack(self.imbl, ord(input('chr?>>> ')))
            except TypeError:
                raise TypeError('length of input does not meet specified length of \'char\'')
        elif intype==1:
            self.oreg[output_registry] = struct.pack(self.mbl, float(input('flt?>>> ')))
        elif intype==2:
            self.oreg[output_registry] = struct.pack(self.mbl, int(input('bin?>>> '), 2))
        elif intype==3:
            self.oreg[output_registry] = struct.pack(self.mbl, int(input('hex?>>> '), 16))
        else:
            raise ValueError('intype argument must be \'char\', \'num\', \'bin\', or \'hex\'')

    def output(self, input_registry, outtype=1):
        if outtype==0:
            print(chr(struct.unpack(self.imbl, self.ireg[input_registry])[0]))
        elif outtype==1:
            print(struct.unpack(self.mbl, self.ireg[input_registry])[0])
        elif outtype==2:
            print(bin(int(struct.unpack(self.mbl, self.ireg[input_registry])[0])).replace('0b',''))
        elif outtype==3:
            print(hex(int(struct.unpack(self.mbl, self.ireg[input_registry])[0])).replace('0x',''))
        else:
            raise ValueError('intype argument must be \'char\', \'num\', \'bin\', or \'hex\'')

class Cpu:
    def __init__(self, in_registries=10240, out_registries=10240, bit=64, runtag=114, functag=116, bytetag=98, inttag=105, floattag=102):
        self.runtag, self.functag, self.bytetag, self.inttag, self.floattag = runtag, functag, bytetag, inttag, floattag
        self.bytesize = bit
        self.funcs = dict()
        self.typ = "CPU"
        if bit == 8:
            self.mbl = 'b'
        elif bit == 16:
            self.mbl = 'h'
        elif bit == 32:
            self.mbl = 'f'
        elif bit == 64:
            self.mbl = 'd'
        else:
            raise ValueError("'bit' must be 8, 16, 32, or 64")
        self.current = b''
        self.ireg = [struct.pack(self.mbl, 0) for x in range(in_registries)]
        self.oreg = [struct.pack(self.mbl, 0) for x in range(out_registries)]

    def run(self, byte):
        rundata = []
        self.current += byte
        if byte[-1] == self.runtag and len(self.current)%((self.bytesize//8)+1) == 1:
            current = [b''.join([struct.pack('B', y) for y in x]) for x in group(self.current[:-1], ((self.bytesize//8)+1))]
            for n, y in enumerate(current):
                if y[0] == self.functag:
                    args = []
                    for k in current[n+1:n+len(self.funcs[y[1:]][1])+1]:
                        if k[0] == self.bytetag:
                            args.append(k[1:])
                        if k[0] == self.inttag:
                            args.append(int(self.binDeform(k[1:])))
                        if k[0] == self.floattag:
                            args.append(self.binDeform(k[1:]))
                    rundata.append(self.funcs[y[1:]][0](*args))
            self.current = b''
            return rundata
            
            
        
    def bind(self, func, tag):
        self.funcs[tag] = (func, list(inspect.signature(func).parameters))
        
    def add(self, input_registry1=9998, input_registry2=9999, output_registry=9999):
        i1 = struct.unpack(self.mbl, self.ireg[input_registry1])
        i2 = struct.unpack(self.mbl, self.ireg[input_registry2])
        self.oreg[output_registry] = struct.pack(self.mbl, i1[0] + i2[0])
        
    def sub(self, input_registry1=9998, input_registry2=9999, output_registry=9999):
        i1 = struct.unpack(self.mbl, self.ireg[input_registry1])
        i2 = struct.unpack(self.mbl, self.ireg[input_registry2])
        self.oreg[output_registry] = struct.pack(self.mbl, i1[0] - i2[0])

    def mult(self, input_registry1=9998, input_registry2=9999, output_registry=9999):
        i1 = struct.unpack(self.mbl, self.ireg[input_registry1])
        i2 = struct.unpack(self.mbl, self.ireg[input_registry2])
        self.oreg[output_registry] = struct.pack(self.mbl, i1[0] * i2[0])
        
    def div(self, input_registry1=9998, input_registry2=9999, output_registry=9999):
        i1 = struct.unpack(self.mbl, self.ireg[input_registry1])
        i2 = struct.unpack(self.mbl, self.ireg[input_registry2])
        if self.bytesize in [32, 64]:
            self.oreg[output_registry] = struct.pack(self.mbl, i1[0] / i2[0])
        else:
            self.oreg[output_registry] = struct.pack(self.mbl, i1[0] // i2[0])
    def lessthan(self, input_registry1=9998, input_registry2=9999, output_registry=9999):
        i1 = struct.unpack(self.mbl, self.ireg[input_registry1])
        i2 = struct.unpack(self.mbl, self.ireg[input_registry2])
        if i1 < i2:
            self.oreg[output_registry] = struct.pack(self.mbl, 1)
        else:
            self.oreg[output_registry] = struct.pack(self.mbl, 0)

    def greaterthan(self, input_registry1=9998, input_registry2=9999, output_registry=9999):
        i1 = struct.unpack(self.mbl, self.ireg[input_registry1])
        i2 = struct.unpack(self.mbl, self.ireg[input_registry2])
        if i1 > i2:
            self.oreg[output_registry] = struct.pack(self.mbl, 1)
        else:
            self.oreg[output_registry] = struct.pack(self.mbl, 0)
        
    def equals(self, input_registry1=9998, input_registry2=9999, output_registry=9999):
        i1 = struct.unpack(self.mbl, self.ireg[input_registry1])
        i2 = struct.unpack(self.mbl, self.ireg[input_registry2])
        if i1 == i2:
            self.oreg[output_registry] = struct.pack(self.mbl, 1)
        else:
            self.oreg[output_registry] = struct.pack(self.mbl, 0)
        

    def set_input_registry(self, num, input_registry=9999):
        if type(num) == type(b''):
            if not struct.unpack(self.mbl, num)[0] > 2**self.bytesize:
                self.ireg[input_registry] = num
            else:
                raise ValueError("Integer cannot be greater than the max bits of the CPU")
        else:
            raise ValueError("Integer argument must be a bytes object (try using CPU.binForm)")

    def get_input_registry(self, input_registry=9999, unpacked=False):
        if unpacked == True:
            return self.binDeform(self.oreg[input_registry])
        else:
            return self.ireg[input_registry]


    def set_output_registry(self, num, output_registry=9999):
        if type(num) == type(b''):
            if not struct.unpack(self.mbl, num)[0] > 2**self.bytesize:
                self.oreg[output_registry] = num
            else:
                raise ValueError("Integer cannot be greater than the max bits of the CPU")
        else:
            raise ValueError("Integer argument must be a bytes object (try using CPU.binForm)")
            
    def get_output_registry(self, output_registry=9999, unpacked=False):
        if unpacked==True:
            return self.binDeform(self.oreg[output_registry])
        else:
            return self.oreg[output_registry]

    def binForm(self, data):
        try:
            return struct.pack(self.mbl, data)
        except struct.error:
            raise ValueError('Number is not within specified bytesize (The CPU is %s bit)' % self.bytesize)
        
    def binDeform(self, data):
        return struct.unpack(self.mbl, data)[0]


class Ram:
    def __init__(self, cells=1048576, bit=64):
        self.bytesize = bit
        self.typ = "RAM"
        if bit == 8:
            self.mbl = 'c'
        elif bit == 16:
            self.mbl = 'h'
        elif bit == 32:
            self.mbl = 'f'
        elif bit == 64:
            self.mbl = 'd'
        else:
            raise ValueError("'bit' must be 8, 16, 32, or 64")
        self.cells = [struct.pack(self.mbl, 0) for x in range(cells)]
        
    def set_cell(self, num, cell=1048575):
        if type(num) == type(b''):
            if not struct.unpack(self.mbl, num)[0] > 2**self.bytesize:
                self.cells[cell] = num
            else:
                raise ValueError("Integer cannot be greater than the max bits of the RAM")
        else:
            raise ValueError("Integer argument must be a bytes object (try using RAM.binForm)")
        
    def get_cell(self, cell=1048575, unpacked=False):
        if unpacked==True:
            return self.binDeform(self.cells[cell])
        else:
            return self.cells[cell]
        
    def swap_cells(self, cell_1=1048574, cell_2=1048575):
        a = self.cells[cell_1]
        b = self.cells[cell_2]
        self.cells[cell_1] = b
        self.cells[cell_2] = a
    
    def binForm(self, data):
        try:
            return struct.pack(self.mbl, data)
        except struct.error:
            raise ValueError('Number is not within specified bytesize (The RAM is %s bit)' % self.bytesize)
        
    def binDeform(self, data):
        return struct.unpack(self.mbl, data)[0]
    
class Connection:
    def __init__(self, connection):
        self.obs = connection
        
    def transfer(self, reg1, reg2):
        if self.obs[0].typ == "CPU" and self.obs[1].typ == "CPU":
            self.obs[1].set_input_registry(self.obs[0].get_output_registry(output_registry=reg1), input_registry=reg2)
        if self.obs[0].typ == "RAM" and self.obs[1].typ == "CPU":
            self.obs[1].set_input_registry(self.obs[0].get_cell(cell=reg1), input_registry=reg2)
        if self.obs[0].typ == "CPU" and self.obs[1].typ == "RAM":
            self.obs[1].set_cell(self.obs[0].get_output_registry(output_registry=reg1),  cell=reg2)
        if self.obs[0].typ == "RAM" and self.obs[1].typ == "RAM":
            self.obs[1].set_cell(self.obs[0].get_cell(cell=reg1),  cell=reg2)
        if self.obs[0].typ == "IO" and self.obs[1].typ == "IO":
            self.obs[1].set_input_registry(self.obs[0].get_output_registry(output_registry=reg1), input_registry=reg2)
        if self.obs[0].typ == "RAM" and self.obs[1].typ == "IO":
            self.obs[1].set_input_registry(self.obs[0].get_cell(cell=reg1), input_registry=reg2)
        if self.obs[0].typ == "IO" and self.obs[1].typ == "RAM":
            self.obs[1].set_cell(self.obs[0].get_output_registry(output_registry=reg1),  cell=reg2)
        if self.obs[0].typ == "IO" and self.obs[1].typ == "CPU":
            self.obs[1].set_input_registry(self.obs[0].get_output_registry(output_registry=reg1), input_registry=reg2)
        if self.obs[0].typ == "CPU" and self.obs[1].typ == "IO":
            self.obs[1].set_input_registry(self.obs[0].get_output_registry(output_registry=reg1), input_registry=reg2)
            
class Motherboard:
    def __init__(self, bit=64):
        self.bytesize = bit
        if bit == 8:
            self.mbl = 'c'
        elif bit == 16:
            self.mbl = 'h'
        elif bit == 32:
            self.mbl = 'f'
        elif bit == 64:
            self.mbl = 'd'
        else:
            raise ValueError("'bit' must be 8, 16, 32, or 64")
        self.connections = []
        
    def add_connection(self, part1, part2):
        if part1.bytesize == part2.bytesize == self.bytesize:
            return Connection((part1,part2))
        else:
            raise ValueError('All included parts and the motherboard in the connection must have the same bytesize (%s bit)' % self.bytesize)

    def binForm(self, data):
        try:
            return struct.pack(self.mbl, data)
        except struct.error:
            raise ValueError('Number is not within specified bytesize (The Motherboard is %s bit)' % self.bytesize)
        
    def binDeform(self, data):
        return struct.unpack(self.mbl, data)[0]

if __name__ == '__main__':
    BYTESIZE = 32
    KILOBYTE = 1024
    MEGABYTE = 1048576

    Core = Cpu(bit=BYTESIZE, in_registries=KILOBYTE, out_registries=KILOBYTE, inttag=112)
    Card = Ram(bit=BYTESIZE, cells=MEGABYTE) 
    Board = Motherboard(bit=BYTESIZE)
    IO = InputOutput(bit=BYTESIZE, in_registries=KILOBYTE, out_registries=KILOBYTE)

    CpuToRam = Board.add_connection(Core, Card)
    RamToCpu = Board.add_connection(Card, Core)
    RamToIO = Board.add_connection(Card, IO)
    IOToRam = Board.add_connection(IO, Card)
    print([ob.typ for ob in IOToRam.obs])
    Core.bind(Core.add, Board.binForm(0))
    Core.bind(Core.set_input_registry, Board.binForm(1))
    Core.bind(IO.input, Board.binForm(2))
    Core.bind(IO.output, Board.binForm(3))
    Core.bind(IOToRam.transfer, Board.binForm(4))
    Core.bind(RamToIO.transfer, Board.binForm(5))
    Core.bind(RamToCpu.transfer, Board.binForm(6))
    Core.bind(CpuToRam.transfer, Board.binForm(7))

    TakeInput = b't' + Board.binForm(2) + b'p' + Board.binForm(1023) + b'p' + Board.binForm(1)
    MoveInputToRam = b't' + Board.binForm(4) + b'p' + Board.binForm(1023) + b'p' + Board.binForm(1023)
    print(Core.run(TakeInput + MoveInputToRam + b'r'))
    IOToRam.transfer(1023,1023)
    print(IO.get_output_registry(1023))
    print(Card.get_cell(1023))

