import algorithms
import tkinter as tk
from tkinter import *
from tkinter import filedialog



import algorithms

machine = algorithms.ElGamalMachine()

root = Tk()
root.geometry("1000x800")
root.title("Encryption")

key_size_option = [64, 128, 256, 512, 1024]
  
def upload_file(event=None):
    filename = filedialog.askopenfile()
    print('selected:', filename)
    print(filename.readlines())
    
def save_file():
    file = filedialog.asksaveasfile(initialfile = 'Untitled.txt', defaultextension=".txt", filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    print('selected:', file)

    
    
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
      
main_title = Label(text = "ElGamal Encryption")

key_size = StringVar(root); key_size.set(key_size_option[2]);
key_size_dropdown = OptionMenu(root, key_size, *key_size_option)

generate_key_button = Button(root, height = 2, width = 60, text ="Generate Key", command = lambda: generate_key())

key_1 = Text(root, height = 5, width = 60)
key_2 = Text(root, height = 5, width = 60)

crypt_title = Label(text = "EnDeCrypt", pady=20)

plaintext = Text(root, height = 5, width = 60)
encrypt_button = Button(root, height = 2, width = 60, text ="Encrypt!", command = lambda: encrypt())

ciphertext = Text(root, height = 5, width = 60)
decrypt_button = Button(root, height = 2, width = 60, text ="Decrypt!", command = lambda: decrypt())

open = Button(root, text='Open File', command=upload_file)
save= Button(root, text= "Save", command= lambda:save_file())
  
main_title.pack()

key_size_dropdown.pack()
generate_key_button.pack()

key_1.pack()
key_2.pack()

crypt_title.pack()
  
plaintext.pack()
encrypt_button.pack()

ciphertext.pack()
decrypt_button.pack()

open.pack()
save.pack()


mainloop()