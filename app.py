import algorithms
import tkinter as tk
from tkinter import *
from tkinter import ttk

root = tk.Tk()
root.geometry("1000x800")
root.title("Digital Signatures")

control = ttk.Notebook(root)

tab1 = ttk.Frame(control)
tab2 = ttk.Frame(control)

control.add(tab1, text='Generate Keys')
control.add(tab2, text='Digital Signature')
control.pack(expand=1, fill="both")

machine = algorithms.ECCElGamalMachine()

key_size_option = [10, 11, 12]


def generate_key():
    pub_key, pri_key = machine.create_key_full(int(key_size.get()))

    key_1.delete('1.0', END)
    key_1.insert(END, str(pub_key))

    key_2.delete('1.0', END)
    key_2.insert(END, str(pri_key))


def encrypt():
    pub_key = key_1.get("1.0", "end-1c")

    plaintext_value = plaintext.get("1.0", "end-1c")
    plaintext.delete('1.0', END)
    encrypted = machine.encrypt_full(plaintext_value, pub_key)

    ciphertext.delete('1.0', END)
    ciphertext.insert(END, encrypted)


def decrypt():
    pri_key = key_2.get("1.0", "end-1c")

    ciphertext_value = ciphertext.get("1.0", "end-1c")
    ciphertext.delete('1.0', END)
    decrypted = machine.decrypt_full(ciphertext_value, pri_key)

    plaintext.delete('1.0', END)
    plaintext.insert(END, decrypted)


def sign(filename, signature):
    with open(filename, 'a') as file:
        file.write("\n\n<ds>")
        file.write(signature)
        file.write("<\ds>")


key_size = StringVar(tab1)
key_size.set(key_size_option[2])
key_size_dropdown = OptionMenu(tab1, key_size, *key_size_option)

generate_key_button = Button(tab1,
                             height=2,
                             width=60,
                             text="Generate Key",
                             command=lambda: generate_key())

key_1 = Text(tab1, height=5, width=60)
key_2 = Text(tab1, height=5, width=60)

plaintext = Text(tab1, height=5, width=60)
encrypt_button = Button(tab1,
                        height=2,
                        width=60,
                        text="Encrypt!",
                        command=lambda: encrypt())

ciphertext = Text(tab1, height=5, width=60)
decrypt_button = Button(tab1,
                        height=2,
                        width=60,
                        text="Decrypt!",
                        command=lambda: decrypt())

ttk.Label(tab1, text="Welcome to GeeksForGeeks").grid(column=0,
                                                      row=0,
                                                      padx=30,
                                                      pady=30)
ttk.Label(tab2, text="Lets dive into the world of computers").grid(column=0,
                                                                   row=0,
                                                                   padx=30,
                                                                   pady=30)

root.mainloop()

# import algorithms

# machine = algorithms.asymmetrickey.ECCElGamalMachine()

# root = Tk()
# root.geometry("1000x800")
# root.title("Encryption")

# key_size_option = [10, 11, 12]

# def generate_key():
#     pub_key, pri_key = machine.create_key_full(int(key_size.get()))

#     key_1.delete('1.0', END)
#     key_1.insert(END, str(pub_key))

#     key_2.delete('1.0', END)
#     key_2.insert(END, str(pri_key))

# def encrypt():
#     pub_key = key_1.get("1.0", "end-1c")

#     plaintext_value = plaintext.get("1.0", "end-1c")
#     plaintext.delete('1.0', END)
#     encrypted = machine.encrypt_full(plaintext_value, pub_key)

#     ciphertext.delete('1.0', END)
#     ciphertext.insert(END, encrypted)

# def decrypt():
#     pri_key = key_2.get("1.0", "end-1c")

#     ciphertext_value = ciphertext.get("1.0", "end-1c")
#     ciphertext.delete('1.0', END)
#     decrypted = machine.decrypt_full(ciphertext_value, pri_key)

#     plaintext.delete('1.0', END)
#     plaintext.insert(END, decrypted)

# main_title = Label(text = "ECC ElGamal Encryption")

# key_size = StringVar(root); key_size.set(key_size_option[2]);
# key_size_dropdown = OptionMenu(root, key_size, *key_size_option)

# generate_key_button = Button(root, height = 2, width = 60, text ="Generate Key", command = lambda: generate_key())

# key_1 = Text(root, height = 5, width = 60)
# key_2 = Text(root, height = 5, width = 60)

# plaintext = Text(root, height = 5, width = 60)
# encrypt_button = Button(root, height = 2, width = 60, text ="Encrypt!", command = lambda: encrypt())

# ciphertext = Text(root, height = 5, width = 60)
# decrypt_button = Button(root, height = 2, width = 60, text ="Decrypt!", command = lambda: decrypt())

# main_title.pack()

# key_size_dropdown.pack()
# generate_key_button.pack()

# key_1.pack()
# key_2.pack()

# plaintext.pack()
# encrypt_button.pack()

# ciphertext.pack()
# decrypt_button.pack()

# mainloop()
