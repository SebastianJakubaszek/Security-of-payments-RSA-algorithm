from socket import *
from Crypto.Util import number
import random
from tkinter import *

class Bank:
    def __init__(self,master):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind(('', 8888))
        self.s.listen()
        self.pieniadze_banku = 0
        self.button_nasluchuj = Button(master,text = "Nasluchuj", command = self.nasluchuj, height=2, width=25)
        self.button_wylosuj_klucze = Button(master,text = "Wylosuj klucze", command= self.generowanie_kluczy, height=2, width=25)
        self.button_wyslij_klucze = Button(master,text = "Wyslij klucze", command= self.wyslij_klucze, height=2, width=25)
        self.button_odbierz_zapakowana_monete = Button(master, text="Odbierz zapakowana monete", command=self.odbierz_zapakowana_monete, height=2, width=25)
        self.button_podpisz_monete = Button(master, text="Podpisz monete", command=self.podpisz_monete, height=2, width=25)
        self.button_wyslij_podpisana_monete = Button(master, text="Wyslij podpisana monete", command=self.wyslij_podpisana_monete, height=2, width=25)
        self.button_odbierz_monete_od_sklep = Button(master, text="Odbierz monete od sklep", command=self.odbierz_monete_od_sklep, height=2, width=25)
        self.button_podaj_S_do_sklep = Button(master, text="Wyslij żadanie o S do sklep", command=self.podaj_S_do_sklepu, height=2, width=25)
        self.button_odbierz_S = Button(master, text="Odbierz S", command=self.odbierz_S, height=2, width=25)
        self.button_sprawdz_monete = Button(master, text="Sprawdz monete", command=self.sprawdz_monete, height=2, width=25)
        self.text = Text(master, height=25, width=43)
        self.text.config(state="disabled")
        self.button_nasluchuj.place(x=0,y=5)
        self.button_wylosuj_klucze.place(x=0,y=45)
        self.button_wyslij_klucze.place(x=0,y=85)
        self.button_odbierz_zapakowana_monete.place(x=0,y=125)
        self.button_podpisz_monete.place(x=0,y=165)
        self.button_wyslij_podpisana_monete.place(x=0,y=205)
        self.button_odbierz_monete_od_sklep.place(x=0,y=245)
        self.button_podaj_S_do_sklep.place(x=0,y=285)
        self.button_odbierz_S.place(x=0,y=325)
        self.button_sprawdz_monete.place(x=0,y=365)
        self.text.place(x=190,y=0)
        self.stan_konta_sklepu = 0



    def generowanie_kluczy(self):
        i = random.randint(9, 10)
        p = number.getPrime(i, None)
        while (True):
            q = number.getPrime(i, None)
            if (q != p):
                break

        self.text.config(state="normal")
        self.text.insert(INSERT,"Wylosowano q = {} \n".format(q))
        self.text.insert(INSERT,"Wylosowano p = {} \n".format(p))
        o = (p - 1) * (q - 1)
        self.n = p * q

        for i in range(int(p / 2), self.n, 1):
            ax = i
            bx = o
            while (bx):
                t = bx
                bx = ax % bx
                ax = t
            if (ax == 1):
                self.e = i
                break
        liczba_modulo = self.n
        klucz_prywatny = number.inverse(self.e, o)
        self.d = klucz_prywatny
        klucz_publiczny = self.e
        self.text.insert(INSERT, "Klucz publiczny = {} \n".format(klucz_publiczny))
        self.text.insert(INSERT, "Klucz prywatny = {} \n".format(klucz_prywatny))
        self.text.insert(INSERT, "Liczba modulo = {} \n ".format(liczba_modulo))
        self.text.config(state="disabled")
        self.klucz_do_wyslania ="{},{}".format(klucz_publiczny,liczba_modulo)



    def wyslij_klucze(self):
        self.client.send(self.klucz_do_wyslania.encode())
        self.text.config(state="normal")
        self.text.insert(INSERT,"Wyslano klucze do usera\n")
        self.text.config(state="disabled")


    def nasluchuj(self):
        self.client, self.addr = self.s.accept()
        self.kto = self.client.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, "Polaczono z: {} \n".format(self.kto))
        self.text.config(state="disabled")

    def odbierz_zapakowana_monete(self):
        wiadomosc = self.client.recv(1024).decode().split(",")
        self.zapakowana_moneta = wiadomosc[0]
        self.kwota = wiadomosc [1]



    def podpisz_monete(self):
        self.podpisna_moneta =  pow(int(self.zapakowana_moneta), self.d) % self.n
        self.text.config(state="normal")
        self.text.insert(INSERT, "Podpisano monete\n")
        self.text.config(state="disabled")

    def wyslij_podpisana_monete(self):
        self.client.send(str(self.podpisna_moneta).encode())
        self.text.config(state="normal")
        self.text.insert(INSERT, "Wyslano podpisana monete\n")
        self.text.config(state="disabled")
        self.client.close()

    def odbierz_monete_od_sklep(self):
        self.moneta_od_sklepu = self.client.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, "Otrzymano monete od sklep: {} \n".format(self.moneta_od_sklepu))
        self.text.config(state="disabled")

    def podaj_S_do_sklepu(self):
        self.client.send("Podaj S".encode())
        self.text.config(state="normal")
        self.text.insert(INSERT, "Wyslano zadanie o S do sklep\n")
        self.text.config(state="disabled")

    def odbierz_S(self):
        self.S = self.client.recv(1024).decode()
        self.text.config(state="normal")
        self.text.insert(INSERT, "Odebrano S: {} \n".format(self.S))
        self.text.config(state="disabled")

    def sprawdz_monete(self):
        a = pow(int(self.S), int(str(self.e)[-1])) % self.n
        b = pow(int(self.moneta_od_sklepu), self.e) % self.n
        if(a==b):
            self.client.send("ok".encode())
            self.text.config(state="normal")
            self.text.insert(INSERT, "Transakcja zakceptowana\n")
            self.stan_konta_sklepu = self.stan_konta_sklepu + int(self.kwota)
            self.text.insert(INSERT, "Stan konta sklepu: {} \n".format(self.stan_konta_sklepu))
            self.text.config(state="disabled")
        else:
            self.client.send("zle".encode())
            self.text.config(state="normal")
            self.text.insert(INSERT, "Transakcja odrzucona\n")
            self.text.config(state="disabled")


root = Tk()
root.title("Bank")
root.geometry("550x420")
Bank= Bank(root)
root.mainloop()