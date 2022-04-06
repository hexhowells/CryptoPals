import codecs

hex_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
decoded_hex = codecs.decode(hex_string, 'hex')

base64_string = codecs.encode(decoded_hex, 'base64').decode()

print("\nBase64: ", base64_string)

hex_data = bytes.fromhex(hex_string)
print("String: ", hex_data.decode('utf-8'))