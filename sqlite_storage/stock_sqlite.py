import sqlite3
from datetime import datetime

# Connexion à la base de données SQLite
conn = sqlite3.connect('gestion.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# Création des tables si elles n'existent pas
def creer_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT,
                        email TEXT,
                        telephone TEXT,
                        adresse TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS produits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT,
                        prix REAL,
                        quantite INTEGER,
                        fournisseur_id INTEGER,
                        FOREIGN KEY(fournisseur_id) REFERENCES fournisseurs(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS commandes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_client INTEGER,
                        date TEXT,
                        FOREIGN KEY(id_client) REFERENCES clients(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS produits_commandes (
                        commande_id INTEGER,
                        produit_id INTEGER,
                        quantite INTEGER,
                        PRIMARY KEY(commande_id, produit_id),
                        FOREIGN KEY(commande_id) REFERENCES commandes(id),
                        FOREIGN KEY(produit_id) REFERENCES produits(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS fournisseurs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT,
                        email TEXT,
                        telephone TEXT
                    )''')

# Classe Client
class Client:
    def __init__(self, nom, email, telephone, adresse, id=None):
        self.id = id
        self.nom = nom
        self.email = email
        self.telephone = telephone
        self.adresse = adresse

    def ajouter_client(self):
        cursor.execute('''INSERT INTO clients (nom, email, telephone, adresse)
                          VALUES (?, ?, ?, ?)''', (self.nom, self.email, self.telephone, self.adresse))
        conn.commit()

    @staticmethod
    def afficher_clients():
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        print("\nListe des clients :")
        for client in clients:
            print(f"ID : {client[0]}, Nom : {client[1]}, Email : {client[2]}, Téléphone : {client[3]}, Adresse : {client[4]}")

    @staticmethod
    def modifier_client(client_id, nom, email, telephone, adresse):
        cursor.execute('''UPDATE clients SET nom = ?, email = ?, telephone = ?, adresse = ? WHERE id = ?''',
                       (nom, email, telephone, adresse, client_id))
        conn.commit()

    @staticmethod
    def supprimer_compte(client_id):
        cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        conn.commit()

# Classe Produit
class Produit:
    def __init__(self, nom, prix, quantite, fournisseur_id, id=None):
        self.id = id
        self.nom = nom
        self.prix = prix
        self.quantite = quantite
        self.fournisseur_id = fournisseur_id

    def ajouter_produit(self):
        cursor.execute('''INSERT INTO produits (nom, prix, quantite, fournisseur_id)
                          VALUES (?, ?, ?, ?)''', (self.nom, self.prix, self.quantite, self.fournisseur_id))
        conn.commit()

    @staticmethod
    def afficher_produit():
        cursor.execute("SELECT * FROM produits")
        produits = cursor.fetchall()
        print("\nListe des produits :")
        for produit in produits:
            print(f"ID : {produit[0]}, Nom : {produit[1]}, Prix : {produit[2]} DH, Quantité : {produit[3]}, Fournisseur ID : {produit[4]}")

    @staticmethod
    def modifier_produit(produit_id, nom, prix, quantite, fournisseur_id):
        cursor.execute('''UPDATE produits SET nom = ?, prix = ?, quantite = ?, fournisseur_id = ? WHERE id = ?''',
                       (nom, prix, quantite, fournisseur_id, produit_id))
        conn.commit()

    @staticmethod
    def supprimer_produit(produit_id):
        cursor.execute("DELETE FROM produits WHERE id = ?", (produit_id,))
        conn.commit()

    @staticmethod
    def verifier_stock(produit_id):
        cursor.execute("SELECT quantite FROM produits WHERE id = ?", (produit_id,))
        quantite = cursor.fetchone()
        return quantite[0] if quantite else 0

# Classe Commande
class Commande:
    def __init__(self, id_client, date=None, id=None):
        self.id = id
        self.id_client = id_client
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.produits = []

    def ajouter_commande(self):
        # Vérifier toute la commande avant d'écrire afin d'éviter une commande
        # vide ou partielle lorsque le stock d'un produit est insuffisant.
        for produit_id, quantite in self.produits:
            stock_actuel = Produit.verifier_stock(produit_id)
            if stock_actuel < quantite:
                print(f"Stock insuffisant pour le produit {produit_id}. Commande non ajoutée.")
                return False

        try:
            cursor.execute('''INSERT INTO commandes (id_client, date) VALUES (?, ?)''',
                           (self.id_client, self.date))
            self.id = cursor.lastrowid  # Récupérer l'ID de la commande après insertion

            for produit_id, quantite in self.produits:
                cursor.execute('''INSERT INTO produits_commandes (commande_id, produit_id, quantite) 
                                  VALUES (?, ?, ?)''', (self.id, produit_id, quantite))
                cursor.execute('''UPDATE produits SET quantite = quantite - ? WHERE id = ?''', (quantite, produit_id))
            conn.commit()
            return True
        except sqlite3.Error:
            conn.rollback()
            self.id = None
            raise

    """def ajouter_commande(self):
        cursor.execute('''INSERT INTO commandes (id_client, date) VALUES (?, ?)''', (self.id_client, self.date))
        conn.commit()
        self.id = cursor.lastrowid  # Récupérer l'ID de la commande après insertion
        for produit_id, quantite in self.produits:
            cursor.execute('''INSERT INTO produits_commandes (commande_id, produit_id, quantite) 
                              VALUES (?, ?, ?)''', (self.id, produit_id, quantite))
        conn.commit()"""

    def ajouter_produit_commande(self, produit_id, quantite):
        self.produits.append((produit_id, quantite))

    @staticmethod
    def afficher_commandes():
        cursor.execute("SELECT * FROM commandes")
        commandes = cursor.fetchall()
        print("\nListe des commandes :")
        for commande in commandes:
            client_id = commande[1]
            cursor.execute("SELECT nom FROM clients WHERE id = ?", (client_id,))
            client = cursor.fetchone()
            montant_total = Commande.calculer_montant_total(commande[0])  # Calcul du montant total

            cursor.execute('''SELECT produits.nom, produits_commandes.quantite
                              FROM produits
                              JOIN produits_commandes ON produits.id = produits_commandes.produit_id
                              WHERE produits_commandes.commande_id = ?''', (commande[0],))
            produits_details = cursor.fetchall()

            produits_str = ", ".join([f"{nom} (Quantité : {quantite})" for nom, quantite in produits_details])
            print( f"ID : {commande[0]}, Client : {client[0]}, Produits : {produits_str}, Montant Total : {montant_total} DH, Date : {commande[2]}")

    @staticmethod
    def calculer_montant_total(commande_id):
        cursor.execute('''SELECT produits.prix, produits_commandes.quantite
                          FROM produits
                          JOIN produits_commandes ON produits.id = produits_commandes.produit_id
                          WHERE produits_commandes.commande_id = ?''', (commande_id,))
        items = cursor.fetchall()
        total = sum(prix * quantite for prix, quantite in items)
        return total

    @staticmethod
    def modifier_commande(commande_id, produits):
        cursor.execute("DELETE FROM produits_commandes WHERE commande_id = ?", (commande_id,))
        for produit_id, quantite in produits:
            cursor.execute('''INSERT INTO produits_commandes (commande_id, produit_id, quantite) 
                              VALUES (?, ?, ?)''', (commande_id, produit_id, quantite))
        conn.commit()

    @staticmethod
    def supprimer_commande(commande_id):
        cursor.execute("DELETE FROM produits_commandes WHERE commande_id = ?", (commande_id,))
        cursor.execute("DELETE FROM commandes WHERE id = ?", (commande_id,))
        conn.commit()



# Classe Fournisseur
class Fournisseur:
    def __init__(self, nom, email, telephone, id=None):
        self.id = id
        self.nom = nom
        self.email = email
        self.telephone = telephone

    def ajouter_fournisseur(self):
        cursor.execute('''INSERT INTO fournisseurs (nom, email, telephone)
                          VALUES (?, ?, ?)''', (self.nom, self.email, self.telephone))
        conn.commit()

    @staticmethod
    def afficher_fournisseur():
        cursor.execute("SELECT * FROM fournisseurs")
        fournisseurs = cursor.fetchall()
        print("\nListe des fournisseurs :")
        for fournisseur in fournisseurs:
            print(f"ID : {fournisseur[0]}, Nom : {fournisseur[1]}, Email : {fournisseur[2]}, Téléphone : {fournisseur[3]}")

    @staticmethod
    def modifier_fournisseur(fournisseur_id, nom, email, telephone):
        cursor.execute('''UPDATE fournisseurs SET nom = ?, email = ?, telephone = ? WHERE id = ?''',
                       (nom, email, telephone, fournisseur_id))
        conn.commit()

    @staticmethod
    def supprimer_fournisseur(fournisseur_id):
        cursor.execute("DELETE FROM fournisseurs WHERE id = ?", (fournisseur_id,))
        conn.commit()

# Menu principal
def menu_principal():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Gestion des clients")
        print("2. Gestion des produits")
        print("3. Gestion des commandes")
        print("4. Gestion des fournisseurs")
        print("5. Quitter")
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            menu_clients()
        elif choix == "2":
            menu_produits()
        elif choix == "3":
            menu_commandes()
        elif choix == "4":
            menu_fournisseurs()
        elif choix == "5":
            print("Au revoir!")
            break
        else:
            print("Option invalide, veuillez réessayer.")

# Menu Clients
def menu_clients():
    while True:
        print("\n=== Gestion des clients ===")
        print("1. Ajouter un client")
        print("2. Afficher les clients")
        print("3. Supprimer un client")
        print("4. Modifier un client")
        print("5. Retour au menu principal")
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            nom = input("Nom : ")
            email = input("Email : ")
            telephone = input("Téléphone : ")
            adresse = input("Adresse : ")
            client = Client(nom, email, telephone, adresse)
            client.ajouter_client()
        elif choix == "2":
            Client.afficher_clients()
        elif choix == "3":
            Client.afficher_clients()
            client_id = int(input("ID du client à supprimer : "))
            Client.supprimer_compte(client_id)
        elif choix == "4":
            Client.afficher_clients()
            client_id = int(input("ID du client à modifier : "))
            nom = input("Nouveau nom : ")
            email = input("Nouveau email : ")
            telephone = input("Nouveau téléphone : ")
            adresse = input("Nouvelle adresse : ")
            Client.modifier_client(client_id, nom, email, telephone, adresse)
        elif choix == "5":
            break
        else:
            print("Option invalide, veuillez réessayer.")

# Menu Produits
def menu_produits():
    while True:
        print("\n=== Gestion des produits ===")
        print("1. Ajouter un produit")
        print("2. Afficher les produits")
        print("3. Supprimer un produit")
        print("4. Modifier un produit")
        print("5. Retour au menu principal")
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            nom = input("Nom du produit : ")
            prix = float(input("Prix : "))
            quantite = int(input("Quantité : "))
            fournisseur_id = int(input("ID du fournisseur : "))
            produit = Produit(nom, prix, quantite, fournisseur_id)
            produit.ajouter_produit()
        elif choix == "2":
            Produit.afficher_produit()
        elif choix == "3":
            Produit.afficher_produit()
            produit_id = int(input("ID du produit à supprimer : "))
            Produit.supprimer_produit(produit_id)
        elif choix == "4":
            Produit.afficher_produit()
            produit_id = int(input("ID du produit à modifier : "))
            nom = input("Nouveau nom : ")
            prix = float(input("Nouveau prix : "))
            quantite = int(input("Nouvelle quantité : "))
            fournisseur_id = int(input("Nouveau fournisseur : "))
            Produit.modifier_produit(produit_id, nom, prix, quantite, fournisseur_id)
        elif choix == "5":
            break
        else:
            print("Option invalide, veuillez réessayer.")

# Menu Commandes
def menu_commandes():
    while True:
        print("\n=== Gestion des commandes ===")
        print("1. Ajouter une commande")
        print("2. Afficher les commandes")
        print("3. Supprimer une commande")
        print("4. Modifier une commande")
        print("5. Retour au menu principal")
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            # Afficher les clients et les produits avant de créer la commande
            Client.afficher_clients()
            client_id = int(input("ID du client : "))

            # Afficher les produits avant de commencer à ajouter à la commande
            Produit.afficher_produit()
            commande = Commande(client_id)
            while True:
                produit_id = int(input("ID du produit à ajouter : "))
                quantite = int(input("Quantité : "))
                if Produit.verifier_stock(produit_id) >= quantite:
                    commande.ajouter_produit_commande(produit_id, quantite)
                else:
                    print("Stock insuffisant pour ce produit.")
                continuer = input("Ajouter un autre produit ? (oui/non) : ")
                if continuer.lower() != 'oui':
                    break
            commande.ajouter_commande()
        elif choix == "2":
            Commande.afficher_commandes()
        elif choix == "3":
            Commande.afficher_commandes()
            commande_id = int(input("ID de la commande à supprimer : "))
            Commande.supprimer_commande(commande_id)
        elif choix == "4":
            Commande.afficher_commandes()
            commande_id = int(input("ID de la commande à modifier : "))
            produits = []
            while True:
                produit_id = int(input("ID du produit à ajouter/modifier : "))
                quantite = int(input("Quantité : "))
                produits.append((produit_id, quantite))
                continuer = input("Ajouter un autre produit ? (oui/non) : ")
                if continuer.lower() != 'oui':
                    break
            Commande.modifier_commande(commande_id, produits)
        elif choix == "5":
            break
        else:
            print("Option invalide, veuillez réessayer.")


# Menu Fournisseurs
def menu_fournisseurs():
    while True:
        print("\n=== Gestion des fournisseurs ===")
        print("1. Ajouter un fournisseur")
        print("2. Afficher les fournisseurs")
        print("3. Supprimer un fournisseur")
        print("4. Modifier un fournisseur")
        print("5. Retour au menu principal")
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            nom = input("Nom du fournisseur : ")
            email = input("Email : ")
            telephone = input("Téléphone : ")
            fournisseur = Fournisseur(nom, email, telephone)
            fournisseur.ajouter_fournisseur()
        elif choix == "2":
            Fournisseur.afficher_fournisseur()
        elif choix == "3":
            Fournisseur.afficher_fournisseur()
            fournisseur_id = int(input("ID du fournisseur à supprimer : "))
            Fournisseur.supprimer_fournisseur(fournisseur_id)
        elif choix == "4":
            Fournisseur.afficher_fournisseur()
            fournisseur_id = int(input("ID du fournisseur à modifier : "))
            nom = input("Nouveau nom : ")
            email = input("Nouvel email : ")
            telephone = input("Nouveau téléphone : ")
            Fournisseur.modifier_fournisseur(fournisseur_id, nom, email, telephone)
        elif choix == "5":
            break
        else:
            print("Option invalide, veuillez réessayer.")

def main():
    """Initialise la base puis lance le menu interactif."""
    creer_tables()
    try:
        menu_principal()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
