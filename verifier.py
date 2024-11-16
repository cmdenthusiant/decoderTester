import hashlib

filePath = "main.py"
originalHash = "96e2c471cd36e87271982748bc796b79f6353f350f13b279397d0830"

#Use sha3-244 to generate current main.py's Hash
sha3 = hashlib.sha224()

file = open(filePath, 'rb')
fileCode = file.read()

sha3.update(fileCode)
fileHash = sha3.hexdigest()
print("Current", filePath, "sha3-224 Hash Value:", fileHash)

if fileHash == originalHash:
    print("Hash Value MATCHED Original Hash! VERIFIED")
else:
    print("Hash Value DID NOT MATCHED Original Hash!")