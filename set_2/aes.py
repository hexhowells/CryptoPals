from Crypto.Cipher import AES
import base64
import random

def load_data():
	# load the data to crack
	with open("data_chal_10.txt", "r") as myfile:
		return myfile.read()


def pad(hex_block):
	if (len(hex_block) % 16) == 0:
		return hex_block
	else:
		num_of_padded_bytes = 16 - (len(hex_block) % 16)
	pad_byte = bytes.fromhex("04")

	return hex_block + (pad_byte * num_of_padded_bytes)


def pkcs7_pad(hex_block):
	if (len(hex_block) % 16) == 0:
		return hex_block
	else:
		num_of_padded_bytes = 16 - (len(hex_block) % 16)

	pad_hex = "0" + str(num_of_padded_bytes)
	pad_byte = bytes.fromhex(pad_hex[-2:])

	return hex_block + (pad_byte * num_of_padded_bytes)


def encrypt_ecb_block(data, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.encrypt(data)


def decrypt_ecb_block(data, key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.decrypt(data)


def xor_blocks(block_1, block_2):
	for byte_1, byte_2 in zip(block_1, block_2):
		yield byte_1 ^ byte_2


def encrypt_cbc_block(plain_block, iv_vector, key):
	combined_blocks = bytes(xor_blocks(plain_block, iv_vector))
	encrypted_block = encrypt_ecb_block(combined_blocks, key)

	return encrypted_block


def decrypt_cbc_block(ciphertext, iv_vector, key):
	prev_block = iv_vector
	decrypted_text = ""

	for cipher_block in ciphertext:
		ebc_block = decrypt_ebc_block(cipher_block, key)
		plain_block = xor_blocks(ebc_block, prev_block)
		decrypted_text += str(bytes(plain_block))[2:-1]
		prev_block = cipher_block

	return decrypted_text

