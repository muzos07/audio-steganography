import binascii
import os


class AudioHelper:
    """
    Class AudioHelper contain methods which work with cover file (audio file).
    """

    def convertAudioToBinary(self, filePath):
        """
        Method for converting raw audiofile to list of bits.

        :param filePath:
        :return audioBitList --> list of bits (audi file):
        """
        file = open(filePath, "rb")
        with file:
            contentOfAudio = file.read()
            hexadecimal = binascii.hexlify(contentOfAudio)
            decimal = int(hexadecimal, 16)
            binaryStringAudio = bin(decimal)[2:].zfill(8)
            audioBitList = []

            for bit in binaryStringAudio:
                audioBitList.append(bit)

        return audioBitList

    def countMessageLength(self, filePath):
        lengthOfAudio = os.path.getsize(filePath)
        return int((lengthOfAudio / 8) - 5)

    def convertBinaryToAudio(self, encryptedFileBits, filePath):
        # zde metoda, která je volána z MessageHelper::67, převede bity na soubor a uloží jej do stejné složky
        # vrací plnou cestu k souboru


        # cesta k uloženému souboru bude nazvaná coverFilePath
        coverFilePath = "song - encrypted.mp3" # toto je zde dočasně jen jako kontrola, jestli pak funguje dekryptování
        return coverFilePath
