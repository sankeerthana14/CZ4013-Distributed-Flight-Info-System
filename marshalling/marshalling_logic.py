#MARSHALLING and UNMARSHALLING

"""
Going with Binary - all in all there are 95 characters to encode, including whitespace.

Assuming that all the data is transferred as strings.
Every binary number will be of 7 digits as the closest numbe rot 94 is 128 = 2^7

"""
#Characters to be mapped
uppercase_letters = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
punctuations = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

final_list = uppercase_letters + lowercase_letters + numbers + punctuations

mapping = {}

#Function to creat the mapping -> characters and their respective binary values
def create_mapping():
    for i in range(len(final_list)):
            #removes the 0b in front of the binary number
            bin_num = bin(i)[2:]

            #padding to make it a 7 digit binary number
            if len(bin_num) != 7:
                bin_num = bin_num.zfill(7)
            mapping[final_list[i]] = bin_num

create_mapping()

"""
»» Storing the mapping in a text file:
with open('/Users/sankeerthana/Documents/NTU/YEAR_4/SEM_2/CZ4013/CZ4013-Distributed-Flight-Info-System/marshalling/mapping.txt', 'w') as f:
     f.writelines(str(mapping))
"""    

#Function to encode
def marshall(string):
    encoded = ''
    for letter in string:
        encoded += mapping[letter]
    return encoded

#Function to decode
def unmarshall(string):
    decoded = ''
    for i in range(0, len(string), 7):
        term = string[i:i+7]
        idx = list(mapping.values()).index(term)
        decoded += list(mapping.keys())[idx]
    return decoded
    
#Testing it out
text = "Flight is delayed by 2 hours!"

encoded_string = marshall(text)
decoded_string = unmarshall(encoded_string)

print(f"Original String: {text}")
print(f"Encoded String: {encoded_string}")
print(f"Decoded String: {decoded_string}")



    
          


