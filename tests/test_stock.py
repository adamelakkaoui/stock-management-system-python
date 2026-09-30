import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def charger_module(nom, chemin):
    specification = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class TestStockTexte(unittest.TestCase):
    def test_commande_met_a_jour_le_stock(self):
        with tempfile.TemporaryDirectory() as dossier:
            ancien_dossier = os.getcwd()
            os.chdir(dossier)
            try:
                module = charger_module(
                    "stock_text_test",
                    REPOSITORY_ROOT / "text_storage" / "stock_text.py",
                )
                module.init_json_files()
                fournisseur = module.Fournisseur("Supplier", "supplier@example.invalid", "000")
                fournisseur.ajouter_fournisseur()
                client = module.Client("Student", "student@example.invalid", "000", "Campus")
                client.ajouter_client()
                produit = module.Produit("Notebook", 20.0, 5, fournisseur.id)
                produit.ajouter_produit()
                commande = module.Commande(client.id)
                commande.ajouter_produit_commande(produit.id, 2)

                self.assertTrue(commande.ajouter_commande())
                produits = module.load_data(module.PRODUITS_FILE)
                self.assertEqual(produits[0]["quantite"], 3)
            finally:
                os.chdir(ancien_dossier)


class TestStockSQLite(unittest.TestCase):
    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.ancien_dossier = os.getcwd()
        os.chdir(self.dossier.name)
        self.module = charger_module(
            "stock_sqlite_test",
            REPOSITORY_ROOT / "sqlite_storage" / "stock_sqlite.py",
        )
        self.module.creer_tables()

    def tearDown(self):
        self.module.conn.close()
        os.chdir(self.ancien_dossier)
        self.dossier.cleanup()

    def test_commande_atomique_et_stock(self):
        fournisseur = self.module.Fournisseur("Supplier", "supplier@example.invalid", "000")
        fournisseur.ajouter_fournisseur()
        client = self.module.Client("Student", "student@example.invalid", "000", "Campus")
        client.ajouter_client()
        produit = self.module.Produit("Notebook", 20.0, 5, 1)
        produit.ajouter_produit()

        commande = self.module.Commande(1)
        commande.ajouter_produit_commande(1, 2)
        self.assertTrue(commande.ajouter_commande())
        self.assertEqual(self.module.Produit.verifier_stock(1), 3)

        impossible = self.module.Commande(1)
        impossible.ajouter_produit_commande(1, 4)
        self.assertFalse(impossible.ajouter_commande())
        self.module.cursor.execute("SELECT COUNT(*) FROM commandes")
        self.assertEqual(self.module.cursor.fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()
