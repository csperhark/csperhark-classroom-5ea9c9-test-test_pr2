def adjusted_key(text, key):
    """
    Adjusts the key by repeating it until it matches the length of the text.
    Only advances a key character when an alphabetic letter is found in the text.
    """
    adjusted = ""
    key_index = 0
    key_length = len(key)
    
    for char in text:
        if char.isalpha():
            adjusted += key[key_index % key_length]
            key_index += 1
        else:
            # Non-alphabetic characters do not advance the key index
            adjusted += char
            
    return adjusted


def encrypt_vigenere():
    """
    Part 1 & 2: Reads plaintext from an input file, applies the Vigenère cipher,
    and writes the encrypted result to an output file.
    """
    print("\nENCRYPTING TEXT...")
    input_filename = input("Enter name of file to be encrypted: ")
    key = input("Enter the encryption key: ")
    output_filename = input("Enter name for the output file (must be .txt): ")

    try:
        with open(input_filename, "r") as infile:
            text = infile.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        return

    # Convert text and key to lowercase
    text = text.lower()
    key = key.lower()

    adj_key = adjusted_key(text, key)
    encrypted_text = ""

    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            # Get shift value based on the key (a=0, b=1, ...)
            shift = ord(adj_key[i]) - 97
            # Apply shift maintaining ASCII code within lowercase range [97, 122]
            new_code = ((ord(char) - 97 + shift) % 26) + 97
            encrypted_text += chr(new_code)
        else:
            # Keep non-alphabetic characters unchanged
            encrypted_text += char

    with open(output_filename, "w") as outfile:
        outfile.write(encrypted_text)

    print("DONE!")


def decrypt_vigenere():
    """
    Part 2: Reads ciphertext from an input file, reverses the Vigenère cipher,
    and writes the decrypted plaintext to an output file.
    """
    print("\nDECRYPTING TEXT...")
    input_filename = input("Enter name of file to be decrypted: ")
    key = input("Enter the encryption key: ")
    output_filename = input("Enter name for the output file (must be .txt): ")

    try:
        with open(input_filename, "r") as infile:
            text = infile.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
        return

    # Convert text and key to lowercase
    text = text.lower()
    key = key.lower()

    adj_key = adjusted_key(text, key)
    decrypted_text = ""

    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            # Get shift value based on the key (a=0, b=1, ...)
            shift = ord(adj_key[i]) - 97
            # Reverse shift by subtracting the key shift and using modulo 26
            new_code = ((ord(char) - 97 - shift + 26) % 26) + 97
            decrypted_text += chr(new_code)
        else:
            # Keep non-alphabetic characters unchanged
            decrypted_text += char

    with open(output_filename, "w") as outfile:
        outfile.write(decrypted_text)

    print("DONE!")


def menu():
    """
    Part 3: Displays the menu options and validates user input.
    """
    while True:
        print("\n=== VIGENERE CIPHER ===")
        print("Select Operation:")
        print("1) to encrypt text")
        print("2) to decrypt text")
        print("9) Quit")
        
        option = input(">>> ").strip()
        
        if option in ["1", "2", "9"]:
            return option
        else:
            print("Invalid option. Try again.")


def main():
    """
    Part 3: Main program loop that executes the selected action until 9 is selected.
    """
    while True:
        choice = menu()
        if choice == "1":
            encrypt_vigenere()
        elif choice == "2":
            decrypt_vigenere()
        elif choice == "9":
            print("Quitting program. Bye!")
            break


# Entry point of the program
if __name__ == "__main__":
    main()