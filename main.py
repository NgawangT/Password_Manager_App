import json
import random
from tkinter import *
from tkinter import messagebox
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_pw():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_number = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_list = password_letters + password_symbols + password_number

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    login_dict = {
        website: {
            "email": email,
            "password": password
        }
    }
    if website == '' or email == '' or password == '':
        messagebox.showwarning(title="Warning", message="Input cannot be empty!")
    else:
        try:
            with open("data.json", mode='r') as file:
                # to update JSON properly can't just append instead = open -> update -> write.
                # 1. Read old data in mode = 'r'. read mode.
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", mode='w') as file:
                json.dump(login_dict, file, indent=4)
        else:
            # update the old data with new data.
            data.update(login_dict)

            with open("data.json", mode='w') as file:
                # save the updated data in mode = w. write mode.
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')

# ---------------------------- Search ------------------------------- #


def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as file:
            website_data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Warning", message="No Data File Found.")
    else:
        if website_data.get(website):
            email = website_data[website].get("email")
            password = website_data[website].get("password")
            messagebox.showinfo(title=website, message=f"Email: {email} and Password: {password}")
        else:
            messagebox.showwarning(title="Warning", message=f"No details for the website {website}")

        # Utilized .get() method on website_data.
        # It returns None if the key is not found,
        # eliminating the need for an explicit check with the in operator.
        # Used .get() method on nested dictionaries.
        # can safely retrieve the values without raising KeyError if they don't exist.

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)


# labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# entries
website_var = StringVar()
website_entry = Entry(width=32, textvariable=website_var)
website_entry.grid(row=1, column=1)

email_var = StringVar()
email_entry = Entry(width=50, textvariable=email_var)
email_entry.grid(row=2, column=1, columnspan=2)
# email_entry.insert(0)
password_var = StringVar()
password_entry = Entry(width=32, textvariable=password_var)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", command=generate_pw)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=42, command=save)
add_button.grid(row=4, column=1, columnspan=2)


window.mainloop()
