import csv

alphabet = "abcdefghijklmnopqrstuvwxyz"


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


def get_freq_score(plain_text):
	char_freq = []
	for char in alphabet:
		char_freq.append(char_frequency(char, plain_text))

	return sum(score_chars(char_freq))
	

def crack(hex_string):
	best_score = 10000

	for char in range(126):
		output = bytes(xor_byte_buffers(hex_string, char))
		score = get_freq_score(output)

		if score < best_score:
			best_score = score
			best_output = output 

	return best_output


def find_key(hex_string):
	best_score = 10000

	for char in range(126):
		output = bytes(xor_byte_buffers(hex_string, char))
		score = get_freq_score(output)

		if score < best_score:
			best_score = score
			best_char = char

	return chr(best_char)


# returns list of potential keys if multiple characters have the same score
def find_keys(hex_string):
	best_score = 10000
	best_chars = []

	for char in range(126):
		output = bytes(xor_byte_buffers(hex_string, char))
		score = get_freq_score(output)

		if score < best_score:
			best_score = score
			best_chars = [char]
		elif score == best_score:
			best_chars.append(char)

	return [chr(char) for char in best_chars]