# DataGenerator.py - Used to automatically generate classes used to convert raw bytes to variables
# Created by Lauren Jones and Rahul Goyal, April 2024
# Released Cal Poly Baja SAE ;)

class DataGenerator:
    def __init__(self, filepath, structName, structIndex, outputDirectory, outputFilename) -> None:
        self.filepath = filepath
        self.structName = structName
        self.structIndex = structIndex
        self.outputDirectory = outputDirectory
        self.outputFilename = outputFilename

        self.names = []
        self.types = []
        self.sizes = []
        self.indices = []

        self.currIndex = 0
        self.output = ""


    def parse(self):
        isFound = False
        with open(self.filepath, 'r') as dataFile:
            for line in dataFile:

                # Find struct
                if not isFound:
                    if line.find(f"struct {self.structName}") != -1:
                        isFound = True
                    continue

                # Remove leading whitespace
                line = line.lstrip()

                # Find end of struct
                if line.find('}') != -1:
                    return

                # If line is a comment
                if line.startswith("//"):
                    continue

                # Remove everything until space
                space_index = line.find(" ")
                semicolon_index = line.find(";")
                if space_index == -1 or semicolon_index == -1:
                    continue
                int_index = line.find("int")
                if int_index == -1:
                    raise Exception
                var = line[space_index+1:semicolon_index]
                type = line[0:space_index]
                size = int(line[int_index+len('int'):space_index]) // 8

                # Append each found into a list
                self.names.append(var)
                self.types.append(type)
                self.sizes.append(size)
                self.indices.append(self.currIndex)

                self.currIndex += size


    def create(self):
        output = f""
        output += f"#### ## AUTO-GENERATED FILE ## ####\n"
        output += f"# DO NOT EDIT - USE DataGenerator.py\n"
        output += f"# Authored by Lauren Jones and Rahul Goyal\n"
        output += f"# Released to Cal Poly Baja SAE ;)\n"

        output += f"\n"
        output += f"import struct\n"

        output += f"\n"
        output += f"class {self.outputFilename}:\n"

        output += f"\tsize = {self.indices[-1] + self.sizes[-1]}\n"

        output += f"\n"
        for var in self.names:
            output += f"\t{var} = 0\n"

        output += f"\n"
        output += f"\tdef __init__(self):\n"
        output += f"\t\tself.all_data = {{}}\n"
        for i in range(len(self.names)):
            output+=f"\t\tself.all_data[\"{self.names[i]}\"] = 0\n"

        output += f"\n"
        output += f"\t\tself.names = {self.names}\n"
        output += f"\n"
        output += f"\tdef update(self, bytes):\n"
        output += f"\t\tif len(bytes) < self.size:\n"
        output += f"\t\t\treturn\n"

        output += f"\n"
        for i in range(len(self.names)):
            output += f"\t\tself.{self.names[i]} = struct.unpack(\"{self.type_to_format(self.types[i])}\", bytes[{self.indices[i]}:{self.indices[i] + self.sizes[i]}])[0]\n"

        output += f"\n"
        for i in range(len(self.names)):
            output+=f"\t\tself.all_data[\"{self.names[i]}\"] = self.{self.names[i]}\n"
        self.output = output

    def type_to_format(self, type):
        if type == "int8":
            return "b"
        if type == "uint8":
            return "B"
        if type == "int16":
            return "h"
        if type == "uint16":
            return "H"
        if type == "int32":
            return "l"
        if type == "uint32":
            return "L"
        if type == "bool":
            return "?"
        raise Exception


    def write(self):
        with open (f"{self.outputDirectory}/{self.outputFilename}.py", "w") as data:
            data.write(self.output)

    def update(self):
        self.parse()
        self.create()
        self.write()

eCVTDataGen = DataGenerator("DAQ_COMMON/data.h", 'ecvt_data', 0x0, "DataModel", "eCVTData")
eCVTDataGen.update()

#powertrainDataGen = DataGenerator("DAQ_COMMON/data.h", 'powertrain_data', 0x10, "DataModel", "PowertrainData")
#powertrainDataGen.update()
