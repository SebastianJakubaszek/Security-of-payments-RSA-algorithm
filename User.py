from socket import *
import random
from sympy import mod_inverse
from tkinter import *



class User:
    def __init__(self, master):
        self.button_polacz_z_bank = Button(master, text="Polacz z bank", command = lambda: self.polacz_z_bank(),height=2, width=25)
        self.button_wylosuj_S = Button(master, text="Wylosuj S", command = lambda: self.wylosuj_S(self.n),height=2, width=25)
        self.button_wylosuj_R = Button(master, text="Wylosuj R", command=lambda: self.wylosuj_R(self.n),height=2, width=25)
        self.button_utworz_monete = Button(master, text="Utworz monete", command = lambda: self.utworz_monete(self.e,self.n,self.S),height=2, width=25)
        self.button_zapakuj_monete = Button(master, text="Zapakuj Monete", command=lambda: self.zapakuj_monete(self.M, self.e, self.n, self.R),height=2, width=25)
        self.button_wyslij_zapakowana_monete = Button(master, text="Wyslij zapakowana monete", command=lambda: self.wyslij_zapakowana_monete(),height=2, width=25)
        self.button_sprawdz_podpisana_monete = Button(master, text="Sprawdz podpisana monete", command=lambda: self.sprawdz_monete(self.moneta_podpisana,self.M,self.e,self.n,self.R),height=2, width=25)
        self.button_polacz_z_sklep = Button(master, text="Polacz z sklep", command=lambda: self.polacz_z_sklep(), height=2,width=25)
        self.button_wyslij_podpisana_monete_do_sklep = Button(master, text="Wyslij podpisana monete do sklep", command=lambda: self.wyslij_podpisana_monete_do_sklep(), height=2,width=25)
        self.button_wyslij_S_do_sklepu = Button(master, text="Wyslij S do sklep",command=lambda: self.wyslij_S_do_sklep(),height=2,width=25)
        self.text = Text(master, height=25, width=43)
        self.text.config(state="disabled")
        self.button_polacz_z_bank.place(x=0,y=5)
        self.button_wylosuj_S.place(x=0,y=45)
        self.button_wylosuj_R.place(x=0,y=85)
        self.button_utworz_monete.place(x=0,y=125)
        self.button_zapakuj_monete.place(x=0,y=165)
        self.button_wyslij_zapakowana_monete.place(x=0,y=205)
        self.button_sprawdz_podpisana_monete.place(x=0,y=245)
        self.button_polacz_z_sklep.place(x=0,y=285)
        self.button_wyslij_podpisana_monete_do_sklep.place(x=0,y=325)
        self.button_wyslij_S_do_sklepu.place(x=0,y=365)
        self.text.place(x=190,y=0)


    def utworz_monete(self, e, n, S):
        e = str(e)
        ec = e[-1]
        self.M = pow(S, int(ec)) % n
        self.text.config(state="normal")
        self.text.insert(INSERT,"Utworzono monete: {} \n".format(self.M))
        self.text.config(state="disabled")

    def zapakuj_monete(self, M, e, n, R):
        self.W = pow(R, e)%n
        self.W = (int(M) * self.W) % n
        self.text.config(state="normal")
        self.text.insert(INSERT, "Zapakowana Moneta: {} \n".format(self.W))
        self.text.config(state="disabled")

    def sprawdz_monete(self,moneta_podpisana, Moneta, e, n,R):
        self.moneta_podpisana_bezkoperty = (int(moneta_podpisana) * mod_inverse(R, n)) % n
        M = pow(self.moneta_podpisana_bezkoperty, e) % n
        if (Moneta == M):
            self.text.config(state="normal")
            self.text.insert(INSERT, "Moneta zostala wlasciwie podpisana\n")
            self.text.config(state="disabled")
        else:
            self.text.config(state="normal")
            self.text.insert(INSERT, "Moneta nie zostala wlasciwie podpisana\n")
            self.text.config(state="disabled")

    def wylosuj_R(self,n):
        self.R = 0
        while (self.R == 0 or not (self.R < n)):
            self.R = random.randint(1, 50)
        self.text.config(state="normal")
        self.text.insert(INSERT, "Wylosowane R: {} \n".format(self.R))
        self.text.config(state="disabled")

    def wylosuj_S(self,n):
        self.S = 0;
        while (self.S == 0 or not (self.S < n)):
            self.S = random.randint(1, 50)
        self.text.config(state="normal")
        self.text.insert(INSERT, "Wylosowane S: {} \n".format(self.S))
        self.text.config(state="disabled")

    def polacz_z_bank(self):
        self.bank = socket(AF_INET, SOCK_STREAM)  
        self.bank.connect(('localhost', 8888))  
        self.bank.send("User".encode())
        klucze_otrzymane = self.bank.recv(1024).decode()
        klucze_otrzymane = klucze_otrzymane.split(",")
        self.e = int(klucze_otrzymane[0])
        self.n = int(klucze_otrzymane[1])
        self.text.config(state="normal")
        self.text.insert(INSERT, "Polaczono z bankiem\n")
        self.text.insert(INSERT, "Otrzymano klucz publiczny: {} \n".format(self.e))
        self.text.insert(INSERT, "Otrzymano liczbe n: {} \n".format(self.n))
        self.text.config(state="disabled")

    def polacz_z_sklep(self):
        self.sklep = socket(AF_INET, SOCK_STREAM) 
        self.sklep.connect(('localhost', 9999))  
        self.text.config(state="normal")
        self.text.insert(INSERT, "Polaczono z sklep\n")
        self.text.config(state="disabled")

    def wyslij_zapakowana_monete(self):
        kwota = random.randint(1,1000)
        wiadomosc = str(self.W)+","+str(kwota)
        self.bank.send(str(wiadomosc).encode())
        self.text.config(state="normal")
        self.text.insert(INSERT, "Wyslano zapakowana monete do bank\n")
        self.text.config(state="disabled")
        self.czekaj_na_odpowiedz()


    def czekaj_na_odpowiedz(self):
        self.moneta_podpisana=self.bank.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, "Otrzymano podpisana monete od bank: {} \n".format(self.moneta_podpisana))
        self.text.config(state="disabled")
        self.bank.close()
		
    def wyslij_podpisana_monete_do_sklep(self):
        self.sklep.send(str(self.moneta_podpisana_bezkoperty).encode())
        self.text.config(state="normal")
        self.text.insert(INSERT, "Wyslano podpisana monete do sklep\n")
        self.text.config(state="disabled")
        self.odpowiedz = self.sklep.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, "Otrzymano od sklep: {} \n".format(self.odpowiedz))
        self.text.config(state="disabled")

    def czekaj_na_odpowiedz2(self):
        self.odpowiedz = self.sklep.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, self.odpowiedz+"\n")
        self.text.config(state="disabled")

    def wyslij_S_do_sklep(self):
        self.sklep.send(str(self.S).encode())
        self.text.config(state="normal")
        self.text.insert(INSERT, "Wyslano S do sklep\n")
        self.text.config(state="disabled")
        self.czekaj_na_odpowiedz2()


root = Tk()
root.title("User")
root.geometry("550x420")
User= User(root)
root.mainloop()
