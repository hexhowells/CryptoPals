import base64
import aes
import random

def gen_aes_key():
	with open("aes_key.txt", "w")  as key_file:
		aes_key = bytes(random.getrandbits(8) for _ in range(16))
		key_file.write(str(base64.b64encode(aes_key))[2:-1])
		key_file.close()


def load_data():
	# load the data to crack
	with open("unknown_string.txt", "r") as myfile:
		return myfile.read()


def load_aes_key():
	with open("aes_key.txt", "r") as keyfile:
		return base64.b64decode(keyfile.read())


def get_input_text(input_string):
	base64_unknown_string = load_data()
	unknown_string = base64.b64decode(base64_unknown_string)

	plaintext = bytes(input_string, 'utf-8')

	input_text = bytes(plaintext + unknown_string)
	return aes.pad(input_text)


def detect_block_size(aes_key):
	input_text = get_input_text("A")
	encrypted_text = aes.encrypt_ecb_block(input_text, aes_key)	
	cipher_size = len(encrypted_text)

	for num_of_bytes in range(2, 100):
		input_text = get_input_text("A" * num_of_bytes)
		encrypted_text = aes.encrypt_ecb_block(input_text, aes_key)
		if cipher_size != len(encrypted_text):
			return len(encrypted_text) - cipher_size


def ecb_is_used(aes_key, block_size):
	input_text = get_input_text("A" * (block_size*2))
	encrypted_text = aes.encrypt_ecb_block(input_text, aes_key)
	if encrypted_text[0:block_size] == encrypted_text[block_size:block_size*2]:
		return True
	else:
		return False


def attack_ecb(aes_key, block_size):
	found_chars = ""
	block_pointer = 0

	while True:
		for i in range(block_size-1, -1, -1):
			if len(found_chars) % block_size == 0 and len(found_chars) != 0:
				block_pointer += block_size
				# check if we have reached the end of the text
				if found_chars[-2:] == "\x04\x04":
					return found_chars


			attack_string = ("A" * i)# + found_blocks
			input_text = get_input_text(attack_string) # !!dont print this!!

			encrypted_block = aes.encrypt_ecb_block(input_text, aes_key)
			first_block = encrypted_block[block_pointer:block_pointer+block_size]

			for char in range(127):
				probe_text = (attack_string + found_chars + chr(char))[-block_size:]
				encrypted_probe = aes.encrypt_ecb_block(probe_text, aes_key)

				if encrypted_probe == first_block:
					found_chars += chr(char)
					break



aes_key = load_aes_key()

block_size = detect_block_size(aes_key)
if ecb_is_used(aes_key, block_size):
	print(attack_ecb(aes_key, block_size))


