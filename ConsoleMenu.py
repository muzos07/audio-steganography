import pygame
import os
import sys
from MessageHelper import MessageHelper
from AudioHelper import AudioHelper

class ConsoleMenu:
    """
    Class ConsoleMenu show menu in console and call methods of another classes
    """
    def __init__(self):
        self.ah = AudioHelper()
        self.mh = MessageHelper()
        self.__menu()

    # main menu
    def __menu(self):
        """
        contain main menu
        """
        while True:
            try:
                self.lineSeparator()
                menu = int(input("\nMAIN MENU:\n\t1: Encode\n\t2: Decode\n\t3: Open AudioPlayer\n\t4: Exit\nYour choice: "))

                if menu == 1:
                    self.__encodeMethod()

                elif menu == 2:
                    self.__decodeMethod()

                elif menu == 3:
                    self.play()

                elif menu == 4:
                    exit()
                else:
                    print("\n Wrong value was inserted - please use number in range 1-3.")
            except ValueError:
                print(
                    "\n ValueError - incorrect input - please use number in range 1-3.")

    def __encodeMethod(self):
        """
        Method which is called by choosing 1.Encode in main menu
        """

        self.lineSeparator()
        fileList = self.getAndShowFileList(False)
        audioFilePath = input("Please write path of .wav file or write number of chosen file: ")

        try:
            if self.representsInt(audioFilePath):
                audioFilePath = os.path.dirname(sys.modules['__main__'].__file__) + "/wavSamples/" + fileList[int(audioFilePath) - 1]
        except IndexError:
            print("\nNo file with such a number. Process has ended!")
            return

        try:
            songBytes = self.ah.openAudioFile(audioFilePath)
        except :
            print(" -> File was not found. Process has ended!")
            return

        maxLength = self.mh.countMessageLength(songBytes)

        self.lineSeparator()
        message = input(
            "\nYou can use %d characters for your secret message.\n\t"
            "Be aware, you can't use character '#'.\n\tPlease, write your message: " % maxLength)


        while len(message) > maxLength:
            message = input(
                "\nYour message is longer than limit. Please write new message with max %d characters:\n" % maxLength)

        self.lineSeparator()
        opt = input("\nWould you like to fill full audio with LSB? (yes/no): ")
        while True:
            if opt == 'yes':
                fillAll = True
                break
            elif opt == 'no':
                fillAll = False
                break
            else:
                opt = input("Please write 'yes' or 'no': ")
        try:
            encryptedSongBytes = self.mh.encodeMessageIntoCoverFile(message, songBytes, fillAll)
            self.ah.convertBytesToAudio(encryptedSongBytes, audioFilePath, fillAll)

            print(
                "\nMessage encoding into audio file was successful! "
                "Your new audio file is located in the same folder as original file.")

        except IndexError:
            print(" -> Index out of range. Process has ended!")
        except ValueError:
            print(" -> Value error. Process has ended!")
        except FileExistsError:
            print(" -> File already exists. Process has ended!")



    def __decodeMethod(self):
        """
        Method which is called by choosin 2. Decode in main menu
        """
        self.lineSeparator()
        fileList = self.getAndShowFileList(True)
        audioFilePath = input("Please write path of .wav file or write number of chosen file: ")
        try:
            if self.representsInt(audioFilePath):
                audioFilePath = os.path.dirname(sys.modules['__main__'].__file__) + "/wavSamples/" + fileList[int(audioFilePath) - 1]
        except IndexError:
            print("\nNo file with such a number. Process has ended!")
            return

        try:
            songBytes = self.ah.openAudioFile(audioFilePath)
        except :
            print(" -> File was not found. Process has ended!")
            return

        try:
            encryptedMessage = self.mh.decodeMessageFromCoverFile(songBytes)
        except SyntaxError:
            print("\nThere is no encrypted message in chosen file. Process has ended!")
            return

        print("\nYour encrypted message in chosen file is:\n\t" + encryptedMessage)

    def play(self):
        self.lineSeparator()
        fileList = self.getAndShowFileList(None)
        audioFilePath = input("Please write path of .wav file or write number of chosen file: ")
        try:
            if self.representsInt(audioFilePath):
                audioFilePath = os.path.dirname(sys.modules['__main__'].__file__) + "/wavSamples/" + fileList[int(audioFilePath)-1]
        except IndexError:
            print("\nNo file with such a number. Process has ended!")
            return

        try:
            self.ah.audioPlayer(audioFilePath)
        except pygame.error:
            print("\nFile could not be opened. Process has ended!")
            return
        except FileNotFoundError:
            print("\nFile could not be opened. Process has ended!")
            return

    def getAndShowFileList(self, onlyEncrypted):
        if onlyEncrypted:
            fileList = list(filter(lambda x: "-encrypted.wav" in x or "-fullyEncrypted.wav" in x,
                                   os.listdir(os.path.dirname(sys.modules['__main__'].__file__)+"/wavSamples/")))
        elif onlyEncrypted == None:
            fileList = list(filter(lambda x: ".wav" in x,
                                   os.listdir(os.path.dirname(sys.modules['__main__'].__file__)+"/wavSamples/")))
        else:
            fileList = list(filter(lambda x: ".wav" in x and "-encrypted" not in x and "-fullyEncrypted.wav" not in x,
                                   os.listdir(os.path.dirname(sys.modules['__main__'].__file__)+"/wavSamples/")))
        print()
        i = 1
        for song in fileList:
            print("\t" + str(i) + ": " + song)
            i += 1
        return fileList

    def representsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def lineSeparator():
        print("----------------------------------------------------------"
              "----------------------------------------------------------", end="")