# client.py
import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

HOST = '127.0.0.1'
PORT = 55558

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Prompt for user name
root = tk.Tk()
root.withdraw()
name = simpledialog.askstring("Name", "Enter your name:", parent=root)
client.send(name.encode('utf-8'))

# GUI setup
root = tk.Tk()
root.title("Python Chat")
root.configure(bg="#2E2E2E")

chat_area = tk.Text(root, bg="#1E1E1E", fg="#D3D3D3", font=("Segoe UI", 10), wrap=tk.WORD, state='disabled', bd=0, padx=10, pady=10)
chat_area.pack(expand=True, fill='both', padx=10, pady=(10, 5))

input_frame = tk.Frame(root, bg="#2E2E2E")
input_frame.pack(fill='x', padx=10, pady=(0, 10))

input_area = tk.Entry(input_frame, bg="#3E3E3E", fg="#FFFFFF", font=("Segoe UI", 10), insertbackground="white")
input_area.pack(side='left', expand=True, fill='x', padx=(0, 10), ipady=6)

send_button = tk.Button(input_frame, text="Send", bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), width=10, command=lambda: send())
send_button.pack(side='right')

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            chat_area.config(state='normal')
            chat_area.insert(tk.END, message + "\n")
            chat_area.yview(tk.END)
            chat_area.config(state='disabled')
        except:
            print("An error occurred!")
            client.close()
            break

def send():
    message = input_area.get().strip()
    if message:
        if message.lower() == "/exit":
            client.send("/exit".encode('utf-8'))
            root.quit()
            return

        timestamp = datetime.now().strftime("%H:%M")
        formatted = f"{name} [{timestamp}]: {message}"
        chat_area.config(state='normal')
        chat_area.insert(tk.END, formatted + "\n")
        chat_area.yview(tk.END)
        chat_area.config(state='disabled')

        client.send(formatted.encode('utf-8'))
        input_area.delete(0, tk.END)

# Threads
receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

root.protocol("WM_DELETE_WINDOW", lambda: (client.send("/exit".encode('utf-8')), root.destroy()))
root.mainloop()
