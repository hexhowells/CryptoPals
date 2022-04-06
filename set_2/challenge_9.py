
def pad(hex_block, desired_len):
	assert type(desired_len) is int, "desired_len is not of type 'int'"
	pad_byte = bytes.fromhex("04")

	return hex_block + (pad_byte * (desired_len - len(hex_block)))


hex_block = bytes.fromhex("YELLOW SUBMARINE".encode("utf-8").hex())
padded_text = pad(hex_block, 20)
print(padded_text)