#generate random aes key
#encryption_oracle(plaintext)
#func
#	append random bytes to start and end
#	choose ecb or cbc
#	encrypt ecb
#	generate random iv vector and encrypt cbc
#	return encrypted hex

import aes
import random

def generate_aes_key():
	return bytes(random.getrandbits(8) for _ in range(16))


def pad(hex_block):
	num_of_padded_bytes = 16 - (len(hex_block) % 16)
	pad_byte = bytes.fromhex("04")

	return hex_block + (pad_byte * num_of_padded_bytes)


def append_bytes(plaintext):
	start_count, end_count = random.sample(range(5,11), 2)
	plaintext = bytes(random.getrandbits(8) for _ in range(start_count)) + plaintext
	plaintext += bytes(random.getrandbits(8) for _ in range(end_count))

	return plaintext


def chunk_data(data):
	num_of_blocks = len(data)
	for i in range(0, num_of_blocks, 16):
		yield data[i:i+16]


def encryption_oracle(plaintext):
	hex_data = bytes.fromhex(plaintext.encode('utf-8').hex())
	hex_data = append_bytes(hex_data)
	hex_data = pad(hex_data)

	aes_key = generate_aes_key()

	encrypted_data = bytes()

	chosen_mode = random.randrange(2)
	if chosen_mode == 1:
		for block in chunk_data(hex_data):
			iv_vector = bytes(random.getrandbits(8) for _ in range(16))
			encrypted_data += aes.encrypt_cbc_block(block, iv_vector, aes_key)

	else:
		for block in chunk_data(hex_data):
			encrypted_data += aes.encrypt_ecb_block(block, aes_key)

	return encrypted_data



input_data = "A"*400
encrypted_data = encryption_oracle(input_data)
print(encrypted_data)

data_blocks = [chunk for chunk in chunk_data(encrypted_data)]
	
if data_blocks[1] == data_blocks[2]:
	print("\nECB Mode Used")
else:
	print("\nCBC Mode Used")

