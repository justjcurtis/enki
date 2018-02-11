import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

import os
from pathlib import Path
import zipfile

zipW = zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED)

class AESCipher(object):


    _pad = lambda self, s: s + (self.bs - len(s) % self.bs) * \
	                   chr(self.bs - len(s) % self.bs).encode()
    _unpad = lambda self, s: s[:-ord(s[len(s) - 1:])]

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raww = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raww))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))


def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clr()
    phil = getFile()
    if phil[-5:] != ".enki":
        print("Enter password to lock " + phil)
        key = input("--> ")
        print("Encrypting...")
        encd = enc(phil, key)
        out = phil + ".enki"
        writeByt(encd, out)
        print("Successfuly encryted")
    else:
        print("Enter password to unlock " + phil)
        key = input("--> ")
        print("Decrypting...")
        dencd = denc(phil, key)
        out = phil[:-5]
        writeByt(dencd, out)
        if out[-2:] == ".z":
            unzipDir(out)
        print("Successfuly decrypted")
    print("")
    print("====================================")
    input("Press enter to return to file select")
    main()

def enc(phil, key):
    data = readByt(phil)
    dave = AESCipher(key)
    res = dave.encrypt(data)

    return res


def denc(phil, key):
    data = readByt(phil)
    dave = AESCipher(key)
    res = dave.decrypt(data)

    return res

def writeByt(dat, filly):
    with open(filly, "wb") as f:
        f.write(dat)

def readByt(filly):
    with open(filly, "rb") as f:
        res = f.read()
    return res

def unzipDir(pathh):
    parentDir, zipName = os.path.split(pathh)
    with zipfile.ZipFile(pathh, 'r') as zf:
        zf.extractall(parentDir)

def getFile():
    print("Enter path to file or folder or drag and drop file here")
    print("Press Ctrl+c to exit at any time")
    phil = input("--> ")
    print("")
    print("========================================================")
    res = ""

    if "\'" in phil:
        for char in phil:
            if (char == "\'"):
                char = ""
            res = res + char
        phil = res

    if phil[-7:] == ".z.enki":
        print("============================================================")
        print("A \".z\" file will be created to encrypt and decrypt folders")
        print("This will be unencrypted and left for you to delete safely")
        print("Press enter to continue")
        print("============================================================")
        input("")

    if os.path.isdir(phil):
        print("============================================================")
        print("A \".z\" file will be created to encrypt and decrypt folders")
        print("This will be unencrypted and left for you to delete safely")
        print("Press enter to continue")
        print("============================================================")
        input("")
        zipDir(phil)
        phil = phil + ".z"
    elif not os.path.isfile(phil):
        print("Please enter a valid file path")
        input("Press enter to continue..")
        getFile()
    return phil

def zipDir(pathh):
    parentDir, dirToZip = os.path.split(pathh)


    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        return os.path.normcase(archivePath)


    with zipfile.ZipFile(pathh + ".z", "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for (archiveDirPath, dirNames, fileNames) in os.walk(pathh):
            for fileName in fileNames:
                filePath = os.path.join(archiveDirPath, fileName)
                zf.write(filePath, trimPath(filePath))
            #Make sure we get empty directories as well
            if not fileNames and not dirNames:
                zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
                zf.writestr(zipInfo, "")
#run
main()
