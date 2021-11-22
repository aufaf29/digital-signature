import algorithms
import tkinter as tk
from tkinter import *
from tkinter import filedialog

machine = algorithms.ElGamalMachine()

root = Tk()
root.geometry("1000x800")
root.title("Encryption")

key_size_option = [64, 128, 256, 512, 1024]
    
def upload_key1():
    file = filedialog.askopenfile()
    key_1.delete('1.0', END)
    key_1.insert(END, file.read())
    
def save_key1():
    file = filedialog.asksaveasfile(initialfile = 'privatekey.pri', defaultextension=".pri", filetypes=[("All Files","*.*"),("Private Key","*.pri")])
    file.write(key_1.get("1.0", "end-1c"))
    
def upload_key2():
    file = filedialog.askopenfile()
    key_2.delete('1.0', END)
    key_2.insert(END, file.read())
    
def save_key2():
    file = filedialog.asksaveasfile(initialfile = 'publickey.pub', defaultextension=".pub", filetypes=[("All Files","*.*"),("Public Key","*.pub")])
    file.write(key_2.get("1.0", "end-1c"))

def generate_key():
    pub_key, pri_key = machine.create_key(int(key_size.get()))

    key_1.delete('1.0', END)
    key_1.insert(END, str(pub_key))

    key_2.delete('1.0', END)
    key_2.insert(END, str(pri_key))

def encrypt():
    pub_key = key_1.get("1.0", "end-1c")
    public_key = pub_key.split("=\n")[:-1]
    public_key = { 'y': public_key[0] + "=\n", 'g': public_key[1] + "=\n", 'p': public_key[2] + "=\n" }
    
    plaintext_value = plaintext.get("1.0", "end-1c")
    plaintext.delete('1.0', END)
    encrypted = machine.encrypt(plaintext_value, public_key)

    ciphertext.delete('1.0', END)
    ciphertext.insert(END, encrypted)

def decrypt():
    pri_key = key_2.get("1.0", "end-1c")
    private_key = pri_key.split("=\n")[:-1]
    private_key = { 'x': private_key[0] + "=\n", 'p': private_key[1] + "=\n" }

    ciphertext_value = ciphertext.get("1.0", "end-1c")
    ciphertext.delete('1.0', END)
    decrypted = machine.decrypt(ciphertext_value, private_key)

    plaintext.delete('1.0', END)
    plaintext.insert(END, decrypted)
    

def sign(filename, signature):
    with open(filename, 'a') as file:
        file.write("\n\n<ds>")
        file.write(signature)
        file.write("<\ds>")


def verify(filename, signature):
    with open(filename) as file:
        f = file.read()
        loc_start = f.find("<ds>") + 4
        loc_end = f.find("<\ds>")

        found_signature = f[loc_start:loc_end]

        return found_signature == signature

      
main_title = Label(text = "ElGamal Encryption")

key_size = StringVar(root); key_size.set(key_size_option[2]);
key_size_dropdown = OptionMenu(root, key_size, *key_size_option)

generate_key_button = Button(root, height = 2, width = 60, text ="Generate Key", command = lambda: generate_key())


key1_title = Label(text = "Private Key", pady=10)
key1_open = Button(root, text="Open Key", command=upload_key1)
key1_save = Button(root, text= "Save Key", command=lambda:save_key1())
key_1 = Text(root, height = 4, width = 60)

key2_title = Label(text = "Public Key", pady=10)
key2_open = Button(root, text="Open Key", command=upload_key2)
key2_save = Button(root, text= "Save Key", command=lambda:save_key2())
key_2 = Text(root, height = 4, width = 60)

crypt_title = Label(text = "EnDeCrypt", pady=10)

plaintext = Text(root, height = 4, width = 60)
encrypt_button = Button(root, height = 2, width = 60, text ="Encrypt!", command = lambda: encrypt())

ciphertext = Text(root, height = 4, width = 60)
decrypt_button = Button(root, height = 2, width = 60, text ="Decrypt!", command = lambda: decrypt())

  
main_title.pack()

key_size_dropdown.pack()
generate_key_button.pack()

key1_title.pack()
key1_open.pack()
key1_save.pack()
key_1.pack()

key2_title.pack()
key2_open.pack()
key2_save.pack()
key_2.pack()

crypt_title.pack()
  
plaintext.pack()
encrypt_button.pack()

ciphertext.pack()
decrypt_button.pack()


mainloop()