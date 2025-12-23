import socket
import threading
import tkinter as tk

HOST = '127.0.0.1'   # Change to server IP for LAN
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

window = tk.Tk()
window.title("Python LAN Chat")

chat_box = tk.Text(window)
chat_box.pack()
chat_box.config(state='disabled')

entry = tk.Entry(window, width=50)
entry.pack()

muted = False

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg == "NAME":
                client.send(name.encode())
            else:
                if not muted:
                    chat_box.config(state='normal')
                    chat_box.insert(tk.END, msg + "\n")
                    chat_box.config(state='disabled')
        except:
            break

def send(event=None):
    global muted
    msg = entry.get()
    entry.delete(0, tk.END)

    if msg == "/exit":
        client.close()
        window.quit()

    elif msg == "/mute":
        muted = True
        chat_box.config(state='normal')
        chat_box.insert(tk.END, "You muted the chat\n")
        chat_box.config(state='disabled')

    else:
        client.send(f"{name}: {msg}".encode())

entry.bind("<Return>", send)

name = tk.simpledialog.askstring("Name", "Enter your name")

thread = threading.Thread(target=receive)
thread.start()

window.mainloop()
