from Crypto.Cipher import AES
import base64

def load_data():
	# load the data to crack
	with open("data_chal_7.txt", "r") as myfile:
		return myfile.read()

def encrypt_aes(data, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.encrypt(data)


def decrypt_aes(data, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.decrypt(data)	


key = 'YELLOW SUBMARINE'

base64_data = load_data()
hex_data = base64.b64decode(base64_data)

print(decrypt_aes(hex_data, key).decode('utf-8'))
