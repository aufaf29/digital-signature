import algorithms
import tkinter as tk
from tkinter import *
from tkinter import filedialog

machine = algorithms.ElGamalMachine()

root = Tk()
root.geometry("1000x800")
root.title("Encryption")

key_size_option = [64, 128, 256, 512, 1024]

signing_file = ''
    
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

def upload_signing():
    file = filedialog.askopenfile()
    signing_file = file.read()
    signature_ = algorithms.SHA256().compute(signing_file)
    
    pub_key = key_1.get("1.0", "end-1c")
    
    if(pub_key == ""):
        signature.delete('1.0', END)
        signature.insert(END, "Please Write or Upload Private Key First!")
        return False
    
    public_key = pub_key.split("=\n")[:-1]
    public_key = {
        'y': public_key[0] + "=\n",
        'g': public_key[1] + "=\n",
        'p': public_key[2] + "=\n"
    }
   
    signature_ = machine.encrypt_hex(signature_, public_key)
    signature.delete('1.0', END)
    signature.insert(END, signing_file + "\n\n<ds>" +signature_ + "<\ds>")
    
def save_signing():
    file = filedialog.asksaveasfile(initialfile = 'signatured', defaultextension=".txt", filetypes=[("All Files","*.*"),("Text Document","*.txt")])
    file.write(signature.get("1.0", "end-1c"))

def upload_verify():
    file = filedialog.askopenfile()
    verify_file = file.read()
    loc_start = verify_file.find("<ds>")
    if (loc_start == -1):
        return False
    loc_end = verify_file.find("<\ds>")

    found_signature = verify_file[loc_start + 4:loc_end]
    
    pri_key = key_2.get("1.0", "end-1c")
    
    if(pri_key == ""):
        verify_result.delete('1.0', END)
        verify_result.insert(END, "Please Write or Upload Public Key First!")
        return False
    
    private_key = pri_key.split("=\n")[:-1]
    private_key = {'x': private_key[0] + "=\n", 'p': private_key[1] + "=\n"}

    try:
        decrypted = machine.decrypt_hex(found_signature, private_key)
    except:
        verify_result.delete('1.0', END)
        verify_result.insert(END, "NOT VERIFIED !!! FILE MAYBE CHANGED")
        return False
    
    signature__ = algorithms.SHA256().compute(verify_file[:loc_start - 2])
    
    verify_result.delete('1.0', END)
    
    if(decrypted == signature__):
        verify_result.insert(END, "VERIFIED !!!" + "\n")
    else:
        verify_result.insert(END, "NOT VERIFIED !!! FILE MAYBE CHANGED" + "\n")
        
    verify_result.insert(END, "==> Signature\t: " + decrypted + "\n")
    verify_result.insert(END, "==> Recalculate\t: " + signature__)
        
def generate_key():
    pub_key, pri_key = machine.create_key(int(key_size.get()))

    key_1.delete('1.0', END)
    key_1.insert(END, str(pub_key))

    key_2.delete('1.0', END)
    key_2.insert(END, str(pri_key))


def remove_sign(filename):
    with open(filename) as file:
        f = file.read()
        loc_start = f.find("<ds>")
        if (loc_start == -1):
            return

    with open(filename, 'w') as file:
        file.write(f[:loc_start - 2])


main_title = Label(text="Digital Signature")

key_size = StringVar(root)
key_size.set(key_size_option[2])
key_size_dropdown = OptionMenu(root, key_size, *key_size_option)

generate_key_button = Button(root,
                             height=2,
                             width=60,
                             text="Generate Key",
                             command=lambda: generate_key())


key1_title = Label(text = "Private Key", pady=10)
key1_open = Button(root, text="Open Key", command=lambda:upload_key1())
key1_save = Button(root, text= "Save Key", command=lambda:save_key1())
key_1 = Text(root, height = 4, width = 60)

key2_title = Label(text = "Public Key", pady=10)
key2_open = Button(root, text="Open Key", command=lambda:upload_key2())
key2_save = Button(root, text= "Save Key", command=lambda:save_key2())
key_2 = Text(root, height = 4, width = 60)

signing_title = Label(text = "Signing (Add Signature to File)", pady=10)

signing_open = Button(root, text="Open to be Signed File", command=lambda:upload_signing())
signing_save = Button(root, text= "Save File with Signature", command=lambda:save_signing())
signature = Text(root, height = 4, width = 60)

verify_title = Label(text = "Verifying (Validate Signatured File)", pady=10)

verify_open = Button(root, text="Open to be Verify File", command=lambda:upload_verify())
verify_result = Text(root, height = 4, width = 60)
  
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

signing_title.pack()
signing_open.pack()
signing_save.pack()
signature.pack()

verify_title.pack()
verify_open.pack()
verify_result.pack()


mainloop()