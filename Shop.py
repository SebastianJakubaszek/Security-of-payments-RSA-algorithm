from socket import *
from tkinter import *

class Sklep:
    def __init__(self,master):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind(('', 9999))
        self.s.listen()
        self.button_nasluchuj = Button(master,text="Nasluchuj",command=self.nasluchuj,height=2, width=25)
        self.button_odbierz_monete = Button(master, text="Odbierz moneta", command=self.odbierz_monete,height=2, width=25)
        self.button_polacz_z_bank = Button(master, text="Polacz z bank", command=self.polacz_z_bank, height=2, width=25)
        self.button_wyslij_monete_do_banku = Button(master, text="Wyslij monete do banku", command=self.wyslij_monete_do_bank, height=2, width=25)
        self.button_podaj_S_user = Button(master, text="Podaj S user", command=self.podaj_S_user, height=2, width=25)
        self.button_wyslij_S_do_bank = Button(master, text="Wyslij S do bank", command=self.wyslij_S_do_bank, height=2, width=25)
        self.text = Text(master, height=15, width=35)
        self.text.config(state="disabled")
        self.button_nasluchuj.place(x=0,y=5)
        self.button_odbierz_monete.place(x=0,y=45)
        self.button_polacz_z_bank.place(x=0,y=85)
        self.button_wyslij_monete_do_banku.place(x=0,y=125)
        self.button_podaj_S_user.place(x=0,y=165)
        self.button_wyslij_S_do_bank.place(x=0,y=205)
        self.text.place(x=190,y=0)

    def nasluchuj(self):
        self.client, self.addr = self.s.accept()
        self.text.config(state="normal")
        self.text.insert(INSERT,"Polaczano z User\n")
        self.text.config(state="disabled")

    def odbierz_monete(self):
        self.moneta = self.client.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, "Odebrano monete: {} \n".format(self.moneta))
        self.text.config(state="disabled")

    def polacz_z_bank(self):
        self.bank = socket(AF_INET, SOCK_STREAM)
        self.bank.connect(('localhost', 8888))
        self.bank.send("Sklep".encode())
        self.text.config(state="normal")
        self.text.insert(INSERT, "Polaczano z Bank \n")
        self.text.config(state="disabled")

    def wyslij_monete_do_bank(self):
        self.bank.send(self.moneta.encode())
        self.text.config(state="normal")
        self.text.insert(INSERT,"Wyslano monete do Bank: {} \n".format(self.moneta))
        self.text.config(state="disabled")
        self.odpowiedz = self.bank.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, "Odpowiedz od banku: {} \n".format(self.odpowiedz))
        self.text.config(state="disabled")



    def podaj_S_user(self):
        self.client.send("Podaj S".encode())
        self.text.config(state="normal")
        self.text.insert(INSERT, "Wyslano do User: {} \n".format(self.odpowiedz))
        self.text.config(state="disabled")
        self.S = self.client.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, "S od User: {} \n".format(self.S))
        self.text.config(state="disabled")

    def wyslij_S_do_bank(self):
        self.bank.send(self.S.encode())
        self.text.config(state="normal")
        self.text.insert(INSERT, "Wyslano do Bank S: {} \n".format(self.S))
        self.text.config(state="disabled")
        self.odpowiedz = self.bank.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, "Otrzymano od Banku {} \n".format(self.odpowiedz))
        self.text.config(state="disabled")
        if(self.odpowiedz=="ok"):
            self.client.send("Transakcja zaakceptowana".encode())
        else:
            self.client.send("Transakcja nie zaakceptowana".encode())






root = Tk()
root.title("Sklep")
root.geometry("500x250")
sklep = Sklep(root)
root.mainloop()
