import json
import os
from datetime import datetime

# Création du dossier data s'il n'existe pas
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Chemins des fichiers JSON
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.txt")
PRODUITS_FILE = os.path.join(DATA_DIR, "produits.txt")
COMMANDES_FILE = os.path.join(DATA_DIR, "commandes.txt")
FOURNISSEURS_FILE = os.path.join(DATA_DIR, "fournisseurs.txt")

# Initialisation des fichiers JSON s'ils n'existent pas
def init_json_files():
    files = {
        CLIENTS_FILE: [],
        PRODUITS_FILE: [],
        COMMANDES_FILE: [],
        FOURNISSEURS_FILE: []
    }
    for file_path, default_data in files.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=4)

# Fonctions utilitaires pour la manipulation des fichiers JSON
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class Client:
    def __init__(self, nom, email, telephone, adresse, id=None):
        self.id = id or self._generate_id()
        self.nom = nom
        self.email = email
        self.telephone = telephone
        self.adresse = adresse

    def _generate_id(self):
        clients = load_data(CLIENTS_FILE)
        return max([c['id'] for c in clients], default=0) + 1

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'email': self.email,
            'telephone': self.telephone,
            'adresse': self.adresse
        }

    def ajouter_client(self):
        clients = load_data(CLIENTS_FILE)
        clients.append(self.to_dict())
        save_data(CLIENTS_FILE, clients)

    @staticmethod
    def afficher_clients():
        clients = load_data(CLIENTS_FILE)
        print("\nListe des clients :")
        for client in clients:
            print(f"ID : {client['id']}, Nom : {client['nom']}, Email : {client['email']}, "
                  f"Téléphone : {client['telephone']}, Adresse : {client['adresse']}")

    @staticmethod
    def modifier_client(client_id, nom, email, telephone, adresse):
        clients = load_data(CLIENTS_FILE)
        for client in clients:
            if client['id'] == client_id:
                client.update({
                    'nom': nom,
                    'email': email,
                    'telephone': telephone,
                    'adresse': adresse
                })
                break
        save_data(CLIENTS_FILE, clients)

    @staticmethod
    def supprimer_compte(client_id):
        clients = load_data(CLIENTS_FILE)
        clients = [c for c in clients if c['id'] != client_id]
        save_data(CLIENTS_FILE, clients)


class Produit:
    def __init__(self, nom, prix, quantite, fournisseur_id, id=None):
        self.id = id or self._generate_id()
        self.nom = nom
        self.prix = prix
        self.quantite = quantite
        self.fournisseur_id = fournisseur_id

    def _generate_id(self):
        produits = load_data(PRODUITS_FILE)
        return max([p['id'] for p in produits], default=0) + 1

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prix': self.prix,
            'quantite': self.quantite,
            'fournisseur_id': self.fournisseur_id
        }

    def ajouter_produit(self):
        produits = load_data(PRODUITS_FILE)
        produits.append(self.to_dict())
        save_data(PRODUITS_FILE, produits)

    @staticmethod
    def afficher_produit():
        produits = load_data(PRODUITS_FILE)
        print("\nListe des produits :")
        for produit in produits:
            print(f"ID : {produit['id']}, Nom : {produit['nom']}, "
                  f"Prix : {produit['prix']} DH, Quantité : {produit['quantite']}, "
                  f"Fournisseur ID : {produit['fournisseur_id']}")

    @staticmethod
    def modifier_produit(produit_id, nom, prix, quantite, fournisseur_id):
        produits = load_data(PRODUITS_FILE)
        for produit in produits:
            if produit['id'] == produit_id:
                produit.update({
                    'nom': nom,
                    'prix': prix,
                    'quantite': quantite,
                    'fournisseur_id': fournisseur_id
                })
                break
        save_data(PRODUITS_FILE, produits)

    @staticmethod
    def supprimer_produit(produit_id):
        produits = load_data(PRODUITS_FILE)
        produits = [p for p in produits if p['id'] != produit_id]
        save_data(PRODUITS_FILE, produits)

    @staticmethod
    def verifier_stock(produit_id):
        produits = load_data(PRODUITS_FILE)
        for produit in produits:
            if produit['id'] == produit_id:
                return produit['quantite']
        return 0


class Commande:
    def __init__(self, id_client, date=None, id=None):
        self.id = id or self._generate_id()
        self.id_client = id_client
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.produits = []

    def _generate_id(self):
        commandes = load_data(COMMANDES_FILE)
        return max([c['id'] for c in commandes], default=0) + 1

    def to_dict(self):
        return {
            'id': self.id,
            'id_client': self.id_client,
            'date': self.date,
            'produits': self.produits
        }

    def ajouter_produit_commande(self, produit_id, quantite):
        self.produits.append({
            'produit_id': produit_id,
            'quantite': quantite
        })

    def ajouter_commande(self):
        # Vérifier le stock pour chaque produit
        for produit in self.produits:
            stock_actuel = Produit.verifier_stock(produit['produit_id'])
            if stock_actuel < produit['quantite']:
                print(f"Stock insuffisant pour le produit {produit['produit_id']}. "
                      f"Commande non ajoutée pour ce produit.")
                return False

        # Mettre à jour les stocks et sauvegarder la commande
        commandes = load_data(COMMANDES_FILE)
        commandes.append(self.to_dict())
        save_data(COMMANDES_FILE, commandes)

        # Mettre à jour les stocks
        produits = load_data(PRODUITS_FILE)
        for commande_produit in self.produits:
            for produit in produits:
                if produit['id'] == commande_produit['produit_id']:
                    produit['quantite'] -= commande_produit['quantite']
                    break
        save_data(PRODUITS_FILE, produits)
        return True

    @staticmethod
    def afficher_commandes():
        commandes = load_data(COMMANDES_FILE)
        clients = load_data(CLIENTS_FILE)
        produits = load_data(PRODUITS_FILE)

        print("\nListe des commandes :")
        for commande in commandes:
            # Trouver le client
            client_nom = "Client inconnu"
            for client in clients:
                if client['id'] == commande['id_client']:
                    client_nom = client['nom']
                    break

            # Calculer le montant total et obtenir les détails des produits
            montant_total = 0
            produits_details = []
            for commande_produit in commande['produits']:
                for produit in produits:
                    if produit['id'] == commande_produit['produit_id']:
                        montant_total += produit['prix'] * commande_produit['quantite']
                        produits_details.append(
                            f"{produit['nom']} (Quantité : {commande_produit['quantite']})"
                        )
                        break

            produits_str = ", ".join(produits_details)
            print(f"ID : {commande['id']}, Client : {client_nom}, "
                  f"Produits : {produits_str}, "
                  f"Montant Total : {montant_total} DH, "
                  f"Date : {commande['date']}")

    @staticmethod
    def modifier_commande(commande_id, nouveaux_produits):
        commandes = load_data(COMMANDES_FILE)
        for commande in commandes:
            if commande['id'] == commande_id:
                commande['produits'] = [
                    {'produit_id': prod_id, 'quantite': quantite}
                    for prod_id, quantite in nouveaux_produits
                ]
                break
        save_data(COMMANDES_FILE, commandes)

    @staticmethod
    def supprimer_commande(commande_id):
        commandes = load_data(COMMANDES_FILE)
        commandes = [c for c in commandes if c['id'] != commande_id]
        save_data(COMMANDES_FILE, commandes)


class Fournisseur:
    def __init__(self, nom, email, telephone, id=None):
        self.id = id or self._generate_id()
        self.nom = nom
        self.email = email
        self.telephone = telephone

    def _generate_id(self):
        fournisseurs = load_data(FOURNISSEURS_FILE)
        return max([f['id'] for f in fournisseurs], default=0) + 1

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'email': self.email,
            'telephone': self.telephone
        }

    def ajouter_fournisseur(self):
        fournisseurs = load_data(FOURNISSEURS_FILE)
        fournisseurs.append(self.to_dict())
        save_data(FOURNISSEURS_FILE, fournisseurs)

    @staticmethod
    def afficher_fournisseur():
        fournisseurs = load_data(FOURNISSEURS_FILE)
        print("\nListe des fournisseurs :")
        for fournisseur in fournisseurs:
            print(f"ID : {fournisseur['id']}, Nom : {fournisseur['nom']}, "
                  f"Email : {fournisseur['email']}, Téléphone : {fournisseur['telephone']}")

    @staticmethod
    def modifier_fournisseur(fournisseur_id, nom, email, telephone):
        fournisseurs = load_data(FOURNISSEURS_FILE)
        for fournisseur in fournisseurs:
            if fournisseur['id'] == fournisseur_id:
                fournisseur.update({
                    'nom': nom,
                    'email': email,
                    'telephone': telephone
                })
                break
        save_data(FOURNISSEURS_FILE, fournisseurs)

    @staticmethod
    def supprimer_fournisseur(fournisseur_id):
        fournisseurs = load_data(FOURNISSEURS_FILE)
        fournisseurs = [f for f in fournisseurs if f['id'] != fournisseur_id]
        save_data(FOURNISSEURS_FILE, fournisseurs)


# Les fonctions de menu restent pratiquement identiques,
# seule l'initialisation change

def menu_principal():
    # Initialiser les fichiers JSON
    init_json_files()

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
            print("Client ajouté avec succès!")
        elif choix == "2":
            Client.afficher_clients()
        elif choix == "3":
            Client.afficher_clients()
            try:
                client_id = int(input("ID du client à supprimer : "))
                Client.supprimer_compte(client_id)
                print("Client supprimé avec succès!")
            except ValueError:
                print("Erreur: L'ID doit être un nombre.")
        elif choix == "4":
            Client.afficher_clients()
            try:
                client_id = int(input("ID du client à modifier : "))
                nom = input("Nouveau nom : ")
                email = input("Nouvel email : ")
                telephone = input("Nouveau téléphone : ")
                adresse = input("Nouvelle adresse : ")
                Client.modifier_client(client_id, nom, email, telephone, adresse)
                print("Client modifié avec succès!")
            except ValueError:
                print("Erreur: L'ID doit être un nombre.")
        elif choix == "5":
            break
        else:
            print("Option invalide, veuillez réessayer.")

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
            try:
                nom = input("Nom du produit : ")
                prix = float(input("Prix : "))
                quantite = int(input("Quantité : "))
                Fournisseur.afficher_fournisseur()
                fournisseur_id = int(input("ID du fournisseur : "))
                produit = Produit(nom, prix, quantite, fournisseur_id)
                produit.ajouter_produit()
                print("Produit ajouté avec succès!")
            except ValueError:
                print("Erreur: Prix et quantité doivent être des nombres.")
        elif choix == "2":
            Produit.afficher_produit()
        elif choix == "3":
            Produit.afficher_produit()
            try:
                produit_id = int(input("ID du produit à supprimer : "))
                Produit.supprimer_produit(produit_id)
                print("Produit supprimé avec succès!")
            except ValueError:
                print("Erreur: L'ID doit être un nombre.")
        elif choix == "4":
            Produit.afficher_produit()
            try:
                produit_id = int(input("ID du produit à modifier : "))
                nom = input("Nouveau nom : ")
                prix = float(input("Nouveau prix : "))
                quantite = int(input("Nouvelle quantité : "))
                Fournisseur.afficher_fournisseur()
                fournisseur_id = int(input("Nouveau ID fournisseur : "))
                Produit.modifier_produit(produit_id, nom, prix, quantite, fournisseur_id)
                print("Produit modifié avec succès!")
            except ValueError:
                print("Erreur: Prix, quantité et ID fournisseur doivent être des nombres.")
        elif choix == "5":
            break
        else:
            print("Option invalide, veuillez réessayer.")

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
            try:
                # Afficher les clients disponibles
                Client.afficher_clients()
                client_id = int(input("ID du client : "))

                # Créer une nouvelle commande
                commande = Commande(client_id)

                while True:
                    # Afficher les produits disponibles
                    Produit.afficher_produit()
                    produit_id = int(input("ID du produit à ajouter : "))
                    quantite = int(input("Quantité : "))

                    # Vérifier le stock
                    stock_disponible = Produit.verifier_stock(produit_id)
                    if stock_disponible >= quantite:
                        commande.ajouter_produit_commande(produit_id, quantite)
                        print("Produit ajouté à la commande!")
                    else:
                        print(f"Stock insuffisant. Stock disponible : {stock_disponible}")

                    continuer = input("Ajouter un autre produit ? (oui/non) : ")
                    if continuer.lower() != 'oui':
                        break

                if commande.ajouter_commande():
                    print("Commande ajoutée avec succès!")
                else:
                    print("Erreur lors de l'ajout de la commande.")

            except ValueError:
                print("Erreur: Les IDs et quantités doivent être des nombres.")

        elif choix == "2":
            Commande.afficher_commandes()

        elif choix == "3":
            Commande.afficher_commandes()
            try:
                commande_id = int(input("ID de la commande à supprimer : "))
                Commande.supprimer_commande(commande_id)
                print("Commande supprimée avec succès!")
            except ValueError:
                print("Erreur: L'ID doit être un nombre.")

        elif choix == "4":
            Commande.afficher_commandes()
            try:
                commande_id = int(input("ID de la commande à modifier : "))
                produits = []

                while True:
                    Produit.afficher_produit()
                    produit_id = int(input("ID du produit à ajouter/modifier : "))
                    quantite = int(input("Quantité : "))
                    produits.append((produit_id, quantite))

                    continuer = input("Ajouter un autre produit ? (oui/non) : ")
                    if continuer.lower() != 'oui':
                        break

                Commande.modifier_commande(commande_id, produits)
                print("Commande modifiée avec succès!")
            except ValueError:
                print("Erreur: Les IDs et quantités doivent être des nombres.")

        elif choix == "5":
            break
        else:
            print("Option invalide, veuillez réessayer.")

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
            print("Fournisseur ajouté avec succès!")

        elif choix == "2":
            Fournisseur.afficher_fournisseur()

        elif choix == "3":
            Fournisseur.afficher_fournisseur()
            try:
                fournisseur_id = int(input("ID du fournisseur à supprimer : "))
                Fournisseur.supprimer_fournisseur(fournisseur_id)
                print("Fournisseur supprimé avec succès!")
            except ValueError:
                print("Erreur: L'ID doit être un nombre.")

        elif choix == "4":
            Fournisseur.afficher_fournisseur()
            try:
                fournisseur_id = int(input("ID du fournisseur à modifier : "))
                nom = input("Nouveau nom : ")
                email = input("Nouvel email : ")
                telephone = input("Nouveau téléphone : ")
                Fournisseur.modifier_fournisseur(fournisseur_id, nom, email, telephone)
                print("Fournisseur modifié avec succès!")
            except ValueError:
                print("Erreur: L'ID doit être un nombre.")

        elif choix == "5":
            break
        else:
            print("Option invalide, veuillez réessayer.")

# Pour lancer l'application
if __name__ == "__main__":
    menu_principal()