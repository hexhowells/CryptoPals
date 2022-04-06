import base64
import XorCracker


def edit_distance(byte_buffer1, byte_buffer2, keysize):
	distance = 0
	for byte1, byte2 in zip(byte_buffer1, byte_buffer2):
		xor_string = byte1 ^ byte2
		distance += bin(xor_string).count("1")
	
	return distance / keysize


def xor_encrypt_chunk(byte_chunk, key):
	encrypted_chunk = ""
	for byte, key_byte in zip(byte_chunk, key):
		encrypted_chunk += chr(byte ^ key_byte)

	return encrypted_chunk.encode('utf-8').hex()


def xor_decrypt(byte_data, key):
	encrypted_string = ""
	x = 0
	key_len = len(key)
	while x < len(byte_data):
		
		encrypted_string += xor_encrypt_chunk(byte_data[x:x+key_len], key)
		x += key_len

	return encrypted_string


def transpose_block(block_data, index):
		transposed_chunk = ""
		for block in block_data:
			transposed_chunk += chr(block[index])
		
		return bytes(transposed_chunk, 'utf-8')


def load_data():
	# load the data to crack
	with open("data_chal_6.txt", "r") as myfile:
		return myfile.read()


def get_highest_keylens(key_dists, return_num):
	highest_distances = sorted(zip(key_dists))[:return_num]
	highest_keys = []
	for dists in highest_distances:
		highest_keys.append(key_dists[dists[0]])

	return highest_keys


def find_keylen(encoded_data, minlen, maxlen):
	# Find the most probable key size
	lowest_dist = 10
	keylen = 0
	distances = {}
	for keysize in range(minlen, maxlen):
		byte_block1 = encoded_data[0: keysize]
		byte_block2 = encoded_data[keysize: keysize*2]
		byte_block3 = encoded_data[keysize*2: keysize*3]
		byte_block4 = encoded_data[keysize*3: keysize*4]

		dist1 = edit_distance(byte_block1, byte_block2, keysize)
		dist2 = edit_distance(byte_block1, byte_block3, keysize)
		dist3 = edit_distance(byte_block1, byte_block4, keysize)

		dist = (dist1 + dist2 + dist3) / 3
		distances[dist] = keysize

		if dist < lowest_dist:
			keylen = keysize
			lowest_dist = dist

	best_keylens = get_highest_keylens(distances, 3)
	
	return best_keylens


def chunk_data(encoded_data, keylen):
	# chunk and transpose the data
	chunked_data = [encoded_data[i:i+keylen] for i in range(0, len(encoded_data), keylen)]
	padding = "0" * (keylen - len(chunked_data[-1]))
	chunked_data[-1] += bytes(padding, 'utf-8')


	transposed_data = []
	for i in range(keylen):
		transposed_data.append(transpose_block(chunked_data, i))

	return transposed_data




encoded_base64 = load_data()
# convert base64 to bytearay
encoded_hex = base64.b64decode(encoded_base64)


keylens = find_keylen(encoded_hex, 2, 50)

print("\nMost Probable Keysizes: {}\n".format(keylens))
print("Cracking Passwords, Please Hold...\n\n" + "-"*100)


# brute force keylen
for keylen in keylens:

	# chunk data
	chunked_data = chunk_data(encoded_hex, keylen)

	# Crack the xor encryption
	decryption_key = ""
	decryption_keys = [""]
	for block in chunked_data:
		keys = XorCracker.find_keys(block)
		
		for i in range(len(decryption_keys)):
			decryption_keys[i] += keys[0]

		if len(keys) == 2:
			forked_keys = []
			for dekey in decryption_keys:
				forked_key = dekey[:-1]
				forked_key += keys[1]
				forked_keys.append(forked_key)
			[decryption_keys.append(fkey) for fkey in forked_keys]
	
	for potential_key in decryption_keys:
		print("Keylen: [{}] decryption key: {}\n".format(keylen, potential_key))

		# convert key from string to bytes
		decryption_key_bytes = bytes.fromhex(potential_key.encode('utf-8').hex())
		# decrypt the data
		data = xor_decrypt(encoded_hex, decryption_key_bytes)
		
		print(bytes.fromhex(data)[:700].decode('utf-8'))
		print("\n" + "-"*50)

	print("\n" + "#"*100)
