# TODO: create  pomodoro
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import pymongo
import pandas as pd


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def mongo(informacoes):

    # não esqueça de registrar o ip no mongoatlas para acesso

    client = pymongo.MongoClient(
        "mongodb+srv://root:root@cluster0.iyube.mongodb.net/?retryWrites=true&w=majority")


    df = pd.read(informacoes, sep=',')  # le o arquivo csv
    # print(df.shape)
    data = df.to_dict(orient='records')  # converte para um dicionario (que é a forma que o mongo le ( tipo json))

    db = client.minhas_senhas  # cria um banco de dados

    db.projetinho.insert_many(data)  # insere os dados no banco de dados

    print(db)  # lista localização da coleção

    print('Dados inseridos com sucesso!')
def save():
    site = website_entry.get().lower()
    user = username_entry.get()
    password = password_entry.get()
    new_data_dict = {site:{'user': user, 'password': password}}

    if len(site) == 0 or len(password) == 0 or len(user) == 0:
        messagebox.showinfo(title="algo errado nao esta certo.", message="Voce não preencheu tudo, volte e verifique. ")
    else:
        try:
            # is_ok = messagebox.askokcancel(title=site, message=f"Deseja salvar as informações, usuario: {user}, e senha: {password}?")
            # if is_ok:
            # abre e le o arquivo json
            with open("data.json", "r") as data_file:

                # Reading old data
                arquivo = json.load(data_file)

                # updating old data with new data
                arquivo.update(new_data_dict)


        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data_dict, data_file, indent=4)

                print(new_data_dict)



        else:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(arquivo, data_file, indent=4)

                print(arquivo)


            #mongo(enviar)


        finally:
            messagebox.showinfo(title="Sucesso", message="Dados salvos com sucesso!!")
            website_entry.delete(0, END)
            password_entry.delete(0, END)
def search():
    if len(website_entry.get()) != 0:
        search_website = website_entry.get().lower()
        try:
            with open("data.json", "r") as data_file:
                arquivo = json.load(data_file)

        except FileNotFoundError:
            messagebox.showinfo(title="Erro", message="Arquivo não encontrado")

        else:
            if search_website in arquivo:
                messagebox.showinfo(title="Sucesso",
                                    message=f"para o site: {search_website}, o Usuario: {arquivo[search_website]['user']}, Senha: {arquivo[search_website]['password']}")
                pyperclip.copy(arquivo[search_website]['password'])

            else:
                messagebox.showinfo(title="Erro", message="Site não encontrado")

    else:
        messagebox.showinfo(title="Erro", message="Voce não preencheu o site")





# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=30,pady=30)

canvas = Canvas(height=300, width=310)
logo_img = PhotoImage(file="good.png")
canvas.create_image(123, 151 ,image=logo_img)
canvas.grid(row=0, column=0, rowspan=6)
# canvas.pack()

#labels
#
website_label = Label(text="Site",width=2)
website_label.grid( row=1, column=1)
username_label = Label(text="Username")
username_label.grid(row=2, column=1)
password_label = Label(text="password")
password_label.grid(row=3, column=1)
create_name = Label(text="by Marco Aurélio Menezes",width=20,font=("arial",7) )
create_name.grid( row=7, column=0)
#
# # Entries
website_entry = Entry(width=21)
website_entry.grid(row=1,column=2)
username_entry = Entry(width=35)
username_entry.grid(row=2,column=2,columnspan=2)
username_entry.insert(0,"adoteumdev@gmail.com")
password_entry = Entry(width=21) # , show="*"
password_entry.grid(row=3,column=2)

# Buttons
generator_button_password = Button(text="GENERATOR",command=generate_password)
generator_button_password.grid(row=3,column=3)

add_button = Button(text="Adicionar", width=30, command=save)
add_button.grid(row=4,column=2,columnspan=2)

search_button = Button(text="Buscar", width=10, command=search)
search_button.grid(row=1,column=3)

# r1 = Label(bg="red", width=43, height=17)
# r1.grid(row=0, column=0 )
# g1 = Label(bg="green", width=20, height=5)
# g1.grid(row=0, column=1)
# b1 = Label(bg="blue", width=48, height=5)
# b1.grid(row=0, column=2)
#
# r2 = Label(bg="red", width=43, height=3)
# r2.grid(row=2, column=0 )
# g2 = Label(bg="green", width=20, height=3)
# g2.grid(row=2, column=1)
# b2 = Label(bg="blue", width=48, height=3)
# b2.grid(row=2, column=2)
#
# r3 = Label(bg="red", width=43, height=3)
# r3.grid(row=3, column=0 )
# g3 = Label(bg="blue", width=20, height=3)
# g3.grid(row=3, column=1)
# b3 = Label(bg="green", width=48, height=3)
# b3.grid(row=3, column=2)
#
# r4 = Label(bg="purple", width=43, height=3)
# r4.grid(row=4, column=0 )
# g4 = Label(bg="green", width=20, height=3)
# g4.grid(row=4, column=1)
# b4 = Label(bg="blue", width=48, height=3)
# b4.grid(row=4, column=2)
#
# r5 = Label(bg="red", width=43, height=3)
# r5.grid(row=5, column=0 )
# g5 = Label(bg="blue", width=20, height=3)
# g5.grid(row=5, column=1)
# b5 = Label(bg="green", width=48, height=3)
# b5.grid(row=5, column=2)
# g = Label(bg="green", width=20, height=5)
# g.grid(row=1, column=1)
#
# b = Label(bg="blue", width=40, height=5)
# b.grid(row=2, column=0, columnspan=2)

# canvas.pack()



# canvas = Canvas(height=330, width=524)
# logo_img = PhotoImage(file="look.png")
# canvas.create_image(260, 160 ,image=logo_img)
# canvas.pack()


window.mainloop()

