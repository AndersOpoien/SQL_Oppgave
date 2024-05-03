#Importere moduler
import csv
import sqlite3
import customtkinter
import os
import messagebox

conn = sqlite3.connect('Brukerdatabase.db') #Lager en helt tom database som jeg kaller for Brukerdatabase
c = conn.cursor()

# Lager en tabell i databasen som jeg kaller for brukere, så legger jeg inn fname, ename, epost, tlf, og posnommer kolonner.
#Varchar for å begrense antall ord som kan være i feltet.
#Integer sånn at man bare kan skrive tall.
# Primary key på tlf siden tlf nummer er unikt. 
c.execute('''
        CREATE TABLE IF NOT EXISTS brukere (
            fname VARCHAR(25),
            ename VARCHAR(30),
            epost VARCHAR(50),
            tlf INTEGER PRIMARY KEY, 
            postnummer INTEGER
        )
    ''')

conn.commit()

#Lager en for postens database
c.execute('''
        CREATE TABLE IF NOT EXISTS postnummer (
            Postnummer PRIMARY KEY,
            Poststed,
            Kommunenummer,
            Kommunenavn, 
            Kategori
        )
    ''')

conn.commit()

#Lager en funksjon for å lage en helt ny clean database. 
def FunkLagDatabase(): 
    conn = sqlite3.connect('TomDatabase.db')
    conn.cursor()

    conn.commit()

#Lage en funksjon for å importere alle brukere ifra CSV filen. 
def FunkImporterCSV():
    conn = sqlite3.connect('Brukerdatabase.db') 
    c = conn.cursor()
    try:
        with open('Brukerdatabase.csv', 'r') as csvfil: #Åpner opp brukerdatabase filen
            lescsv = csv.reader(csvfil)  
            next(lescsv) 

            for row in lescsv: 

                c.execute('''
                    INSERT INTO brukere(
                          fname, 
                          ename, 
                          epost, 
                          tlf, 
                          postnummer
                          )
                    VALUES(?, ?, ?, ?, ?)''', row)

            conn.commit() 
            #Her joiner jeg sammen brukere tabellen og postnummer tabellen.
            #Her velger jeg hva jeg skal ha med, jeg tar med alt men utelukker  postnummer.Postnummer for å ikke få duplicates.
            c.execute('''
                SELECT
                    brukere.fname,
                    brukere.ename,
                    brukere.epost,
                    brukere.tlf,
                    brukere.postnummer,
                    postnummer.Poststed,
                    postnummer.Kommunenummer,
                    postnummer.Kommunenavn,
                    postnummer.Kategori
                FROM brukere 
                JOIN postnummer ON postnummer.Postnummer = brukere.postnummer
                ''') #Joiner brukere tabellen med postnummer tabellen hvis bruker.postnummer har samme verdi som postnummer.Postnummer kolonnen. 
            
            resultat = c.fetchall() #Lagrer resultatet i en variabel.

            for result in resultat:
                print(result) #Printer ut resultatet. 

    except Exception as e:
        print(f"An error occurred: {e}")

#Importerer  postnummer
def FunkImporterPostCSV():
    conn = sqlite3.connect('Brukerdatabase.db') 
    c = conn.cursor()
#Try except
    try:
        with open('Postnummerregister-Excel.csv', 'r') as csvfil: #Åpner opp postnummer filen
            lescsv = csv.reader(csvfil)  #leser filen
            next(lescsv) #Hopper over en linje

            for row in lescsv: #For hver rad i csv filen legger den inn informasjon i postnummer tabellen i databasen. 
                c.execute('''
                    INSERT INTO postnummer(
                          Postnummer,
                          Poststed,
                          Kommunenummer,
                          Kommunenavn,
                          Kategori
                          )
                    VALUES(?, ?, ?, ?, ?)''', row) 

            conn.commit() #Committer sånn at det blir lagret. 
    except Exception as e: #Bruker messagebox til å vise en feilmelding hvis det oppstår et problem.
        messagebox.showerror("Feilmelding", "Importering av postnummer feilet! ")

#Slett brukere, kobler meg til databasen.
def FunkSlettBrukere():
    conn = sqlite3.connect('Brukerdatabase.db') 
    c = conn.cursor()
    try:
        c.execute('''DELETE FROM brukere''') #Sletter brukere
        conn.commit()
    except sqlite3.Error:
        messagebox.showerror("Feilmelding", "Sletting av brukere feilet!") #Messagebox hvis en feilmelding oppstår. 
    finally:
        conn.close()

#Slett postnummer, kobler meg til databasen.
def FunkSlettPost():
    conn = sqlite3.connect('Brukerdatabase.db') 
    c = conn.cursor()
    try:
        c.execute('''DELETE FROM postnummer''') #Sletter postnummer
        conn.commit()
    except sqlite3.Error:
        messagebox.showerror("Feilmelding", "Sletting av postnummere feilet!") #Messagebox hvis en feilmelding oppstår. 
    finally:
        conn.close()

#GUI
def main():
#Lager vinduet
    window = customtkinter.CTk()
    window.title('Administrer brukerdatabase')
    window.geometry('350x300')

#Her er knappene, ganske selv forklart. Linker knappene til funksjonene jeg lagde tidligere. 
    varLeggTil = customtkinter.CTkLabel(window, text="Legg til her", font=("Arial", 20)).pack(pady=5)
    varLagDatabase = customtkinter.CTkButton(window, text="Lag en tom database", width=250, command=FunkLagDatabase).pack(pady=3)
    varImporterCSV = customtkinter.CTkButton(window, text="Importer brukere i hoved databasen", width=250, command=FunkImporterCSV).pack(pady=3)
    varImporterPostCSV = customtkinter.CTkButton(window, text="Importer postnummer i hoved databasen",  width=250,command=FunkImporterPostCSV).pack(pady=3)

    varFjern = customtkinter.CTkLabel(window, text="Fjern her", font=("Arial", 20)).pack(pady=5)
    varSlettBrukere = customtkinter.CTkButton(window, text="Slett brukere", fg_color="red", hover_color="maroon", width=250, command=FunkSlettBrukere).pack(pady=3)
    varSlettPost = customtkinter.CTkButton(window, text="Slett postnummere", fg_color="red", hover_color="maroon", width=250, command=FunkSlettPost).pack(pady=3)


    customtkinter.set_appearance_mode("dark")  #Setter fargene på vinduet til dark mode.
    
    window.mainloop() #Kjører vinduet. 

if __name__ == "__main__": #Bruker main til å kjøre programmet. 
    main()
