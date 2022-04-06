from Crypto.Cipher import AES
import base64
import random

def load_data():
	# load the data to crack
	with open("data_chal_10.txt", "r") as myfile:
		return myfile.read()


def encrypt_ebc_block(data, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.encrypt(data)


def decrypt_ebc_block(data, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.decrypt(data)


def xor_blocks(block_1, block_2):
	for byte_1, byte_2 in zip(block_1, block_2):
		yield byte_1 ^ byte_2


def encrypt_cbc_block(plaintext, iv_vector, key):
	prev_block = iv_vector
	encrypted_text = ""

	for plain_block in plaintext:
		combined_blocks = bytes(xor_blocks(plain_block, prev_block))
		encrypted_block = encrypt_ebc_block(combined_blocks, key)
		encrypted_text += str(encrypted_block)
		prev_block = encrypted_block

	return encrypted_text


def decrypt_cbc_block(ciphertext, iv_vector, key):
	prev_block = iv_vector
	decrypted_text = ""

	for cipher_block in ciphertext:
		ebc_block = decrypt_ebc_block(cipher_block, key)
		plain_block = xor_blocks(ebc_block, prev_block)
		decrypted_text += str(bytes(plain_block))[2:-1]
		prev_block = cipher_block

	return decrypted_text



key = 'YELLOW SUBMARINE'

base64_data = load_data()
hex_data = base64.b64decode(base64_data)

# chunk hex data
hex_chunks = [hex_data[i:i+16] for i in range(0, (int(len(hex_data) / 16)), 16)]

#iv_vector = bytes(random.getrandbits(8) for _ in range(16))
iv_vector = bytes.fromhex("00"*16)

print(decrypt_cbc_block(hex_chunks, iv_vector, key))
