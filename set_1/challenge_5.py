import base64	

input_data = "Burning 'em, if you ain't quick and nimble\n" \
"I go crazy when I hear a cymbal"


def xor_encrypt_chunk(byte_chunk, key):
	encrypted_chunk = ""
	for byte, key_byte in zip(byte_chunk, key):
		encrypted_chunk += chr(byte ^ key_byte)

	return encrypted_chunk.encode('utf-8').hex()


def xor_encrypt(byte_buffer, byte_key):

	encrypted_string = ""
	x = 0
	key_len = len(byte_key)
	while x < len(byte_buffer):
		
		encrypted_string += xor_encrypt_chunk(byte_buffer[x:x+key_len], byte_key)
		x += key_len

	return encrypted_string


def open_file():
	# open the data file
	with open("input_data.txt", "r") as myfile:
		return myfile.read()

key = "ICER"

input_data = open_file()

padding = len(input_data) % len(key)
input_data += "" * padding


# XOR encrypt message
byte_buffer = bytes.fromhex(input_data.encode('utf-8').hex())
byte_key = bytes.fromhex(key.encode('utf-8').hex())

encrypted_hex = xor_encrypt(byte_buffer, byte_key)
#print(encrypted_hex)


# XOR decrypt message
byte_encrypted_hex = bytes.fromhex(encrypted_hex)

print(bytes.fromhex(xor_encrypt(byte_encrypted_hex, byte_key)).decode('utf-8'))

	