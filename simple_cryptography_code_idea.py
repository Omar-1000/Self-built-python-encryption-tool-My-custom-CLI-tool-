import random
def caesar_cipher_standard(text, shift):
    text = text.lower()  # Convert all characters to lowercase
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            base = ord('a')
            shifted_char = chr(((ord(char) - base + shift) % 26) + base)
            encrypted_text += shifted_char
        else:
            print("error ! only alphabets ")
    return encrypted_text
    
def rail_fence_encrypt(plaintext, depth , ceser_key ,  direction='left'):
    rail = ['' for i in range(depth)]
    # Suppose depth = 3
    #rail = [' ', ' ', ' ']
    
    direction_change = 1  # Default direction is upward
    row = 0
   
    for char in plaintext:
        rail[row] += char
        if row == 0:
            direction_change = 1
        elif row == depth - 1:
            direction_change = -1
        row = row + direction_change
        
        # Shuffle the order of rails
    print (rail)
    random.shuffle(rail)
    print(rail)
    # Apply Caesar cipher to each rail
    for i in range(depth):
        rail[i] = caesar_cipher_standard(rail[i], ceaser_key)
      
        if direction == 'right':
            rail[i] = rail[i][::-1]

    encrypted_text = ''.join(rail)
    return encrypted_text

plaintext = "helloword"
depth = 3
ceaser_key=1
encrypted_text = rail_fence_encrypt(plaintext, depth ,ceaser_key , "right")
print("Encrypted text:", encrypted_text)


'''
the output : 
order of rows : ['hod', 'elwr', 'lo']
order of rows sfter the random shuffle ['elwr', 'lo', 'hod']
Encrypted text : sxmfpmepi
'''








