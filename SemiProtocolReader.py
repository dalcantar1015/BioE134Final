from operations.addContainer import addContainer
from operations.removeContainer import removeContainer
from operations.transfer import transfer
from operations.dispense import dispense
from operations.multichannel import multichannel

#Essentially a ported over version of the Java SemiProtocolReader
class SemiProtocolReader():

    def __init__(self):
        self.operations = {"addContainer": addContainer, "removeContainer": removeContainer, "transfer": transfer, "dispense": dispense, "multichannel": multichannel}

    def run(self, local_file_path):
        tasks = []
        semiprotocol = open("Semiprotocols/" + local_file_path, mode="r")

        for line in semiprotocol:
            if line.startswith("//"):
                continue
            if line.replace("\t", "").replace("\n", "") == "":
                continue
            #Addin removal of empty lines and tabs at the end of lines
            line = line.strip("\n")
            tabs = line.split("\t")
            operation = self.operations[tabs[0]]
            task = operation(tabs)
            tasks.append(task)
        semiprotocol.close()
        return tasks


if __name__ == '__main__':
    reader = SemiProtocolReader()
    tasks = reader.run("alibaba")
    for task in tasks:
        task.print()
