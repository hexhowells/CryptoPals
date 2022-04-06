import itertools

def load_data():
	# load the data to crack
	with open("data_chal_8.txt", "r") as myfile:
		return myfile.read()


def edit_distance(byte_buffer1, byte_buffer2, keysize):
	distance = 0

	for byte1, byte2 in zip(byte_buffer1, byte_buffer2):
		xor_string = byte1 ^ byte2
		dist = bin(xor_string).count("1")
		distance += dist 
		if dist == 0:
			print(byte_buffer1)
			print(byte_buffer2)
			print("-----")
	
	return distance / keysize


hex_data = load_data().split("\n")
best_score = 1000

for data in hex_data[:-1]:
	print("="*50)
	data = bytes.fromhex(data)
	chunked_data = [data[i:i+16] for i in range(0, len(data), 16)]

	score = 0
	for block_pair in itertools.combinations(chunked_data, 2):
		dist = edit_distance(block_pair[0], block_pair[1], 16)
		score += dist

	if score < best_score:
		best_score = score
		best_data = data.hex()


print("\n")
print("Best Score: ", best_score)
print("\nECB cyphertext:\n{}".format(best_data))
