hex_buffer_1 = "1c0111001f010100061a024b53535009181c"
hex_buffer_2 = "686974207468652062756c6c277320657965"


def xor_byte_buffers(byte_buffer_1, byte_buffer_2):
	for byte1, byte2 in zip(byte_buffer_1, byte_buffer_2):
		yield byte1 ^ byte2


# convert the hex buffers to a bytearray
byte_buffer_1 = bytes.fromhex(hex_buffer_1)
byte_buffer_2 = bytes.fromhex(hex_buffer_2)

# xor the two bytearrays
xor_bytes = bytes(xor_byte_buffers(byte_buffer_1, byte_buffer_2))

print(xor_bytes.decode('utf-8'))