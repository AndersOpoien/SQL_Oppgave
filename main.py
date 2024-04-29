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

#Lager en funksjon for å lage en helt ny clean database. 
def FunkLagDatabase(): 
    conn = sqlite3.connect('TomDatabase.db')
    conn.cursor()

    conn.commit()

#Lage en funksjon for å importere alle brukere ifra CSV filen. 
def FunkImporterCSV():
    conn = sqlite3.connect('Brukerdatabase.db') 
    c = conn.cursor()
#Try except
    try:
        with open('Brukerdatabase.csv', 'r') as file: #Åpner opp brukerdatabase filen
            reader = csv.reader(file)  #leser filen
            next(reader) #Hopper over en linje

            for row in reader: #For hver rad i csv filen legger den inn informasjon i brukere tabellen i databasen. 
                c.execute('''
                    INSERT INTO brukere(fname, ename, epost, tlf, postnummer)
                    VALUES(?, ?, ?, ?, ?)''', row) 

            conn.commit() #Committer sånn at det blir lagret. 
    except Exception as e: #Bruker messagebox til å vise en feilmelding hvis det oppstår et problem.
        messagebox.showerror("Feilmelding", "Importering av brukere feilet! Pass på og tøm databasen før du importerer.")

#Slett brukere, kobler meg til databasen.
def FunkSlettBrukere():
    conn = sqlite3.connect('Brukerdatabase.db') 
    c = conn.cursor()
    try:
        c.execute('''DELETE FROM brukere''') #Sletter brukere
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Feilmelding", "Sletting av brukere feilet!") #Messagebox hvis en feilmelding oppstår. 
    finally:
        conn.close()

#Sletter den tomme databasen, bruker os modulen til å slette filen. Bruker også messagebox til å vise error hvis det ikke fungerer.
#Noen ganger må man trykke 2 ganger på slett knappen for at den skal fungere. 
def FunkSlettTomDatabase():
    conn = sqlite3.connect('TomDatabase.db')
    conn.close()
    try:
        os.remove('TomDatabase.db')
    except (sqlite3.Error, FileNotFoundError, PermissionError) as e:
        messagebox.showerror("Feilmelding", "Sletting av tom database feilet! Pass på at den tomme databasen eksisterer ")

#GUI
def main():
#Lager vinduet
    window = customtkinter.CTk()
    window.title('Administrer brukerdatabase')
    window.geometry('250x300')

#Her er knappene, ganske selv forklart. Linker knappene til funksjonene jeg lagde tidligere. 
    varLeggTil = customtkinter.CTkLabel(window, text="Legg til").pack(pady=5)
    varLagDatabase = customtkinter.CTkButton(window, text="Lag en tom database", command=FunkLagDatabase).pack(pady=3)
    varImporterCSV = customtkinter.CTkButton(window, text="Importer brukere i hoved databasen", command=FunkImporterCSV).pack(pady=3)

    varFjern = customtkinter.CTkLabel(window, text="Fjern").pack(pady=5)
    varSlettBrukere = customtkinter.CTkButton(window, text="Slett brukere", fg_color="red", hover_color="maroon", command=FunkSlettBrukere).pack(pady=3)
    varSlettTomDatabase = customtkinter.CTkButton(window, text="Slett den tomme database", fg_color="red", hover_color="maroon", command=FunkSlettTomDatabase).pack(pady=3)

    window.mainloop() #Kjører vinduet. 

if __name__ == "__main__": #Bruker main til å kjøre programmet. 
    main()
