encoded_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
alphabet = "abcdefghijklmnopqrstuvwxyz"
freq_scores = None

import csv
with open("freq_scores.csv", 'r') as myfile:
	reader = csv.reader(myfile)
	freq_scores = list(reader)[0]
	# convert string to floats
	freq_scores = list(map(float, freq_scores))



def xor_byte_buffers(byte_buffer, byte_char):
	for byte in byte_buffer:
		yield byte ^ byte_char


def char_frequency(char, plain_text):
	char_count = plain_text.count(bytes(char, "utf-8"))
	return char_count / len(plain_text)
	

def score_chars(chars):
	for i in range(len(chars)):
		yield freq_scores[i] - chars[i]


def score_text(plain_text):
	char_freq = []
	for char in alphabet:
		char_freq.append(char_frequency(char, plain_text))

	return sum(score_chars(char_freq))
	


encoded_bytes = bytes.fromhex(encoded_string)
best_score = 10000

for char in range(127):
	score = score_text(bytes(xor_byte_buffers(encoded_bytes, char)))
	if score < best_score:
		best_score = score
		best_output = bytes(xor_byte_buffers(encoded_bytes, char)) 

print(best_output.decode('utf-8'))