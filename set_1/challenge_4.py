import XorCracker

with open("data_chal_4.txt", "r") as myfile:
	raw_data = myfile.read()
	encoded_hex = raw_data.split('\n')

# decode hex strings to bytes
def decode_hex(hex_string):
	return bytes.fromhex(hex_string)

print("Cracking Hex Codes...\n")

best_score = 1000

for hex_string in encoded_hex:
	hex_bytes = decode_hex(hex_string)
	attempted_crack = XorCracker.crack(hex_bytes)
	crack_score = XorCracker.get_freq_score(attempted_crack)

	if crack_score < best_score:
		best_score = crack_score 
		best_output = attempted_crack


print(best_output.decode('utf-8'))



