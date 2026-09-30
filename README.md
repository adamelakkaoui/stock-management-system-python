# Stock Management System – Python

Academic console application implementing CRUD operations for clients, products, orders and suppliers with two storage approaches: JSON-formatted text files and SQLite.

## Verified features

- Object-oriented `Client`, `Produit`, `Commande` and `Fournisseur` entities.
- Create, display, update and delete operations.
- Product-stock checks and stock updates when an order is added.
- Order-total calculation and hierarchical console menus.
- Independent JSON-text and relational SQLite variants.

## Privacy and portfolio corrections

The submitted text files and SQLite database contained populated contact/order examples and were excluded. The public text backend starts from four empty JSON arrays. The SQLite database is generated locally and ignored by Git.

The SQLite script now has a `main()` guard, verifies all requested products before inserting an order, and rolls back database errors to avoid empty or partially written orders.

## Requirements and use

Python 3.10+ is sufficient; both implementations use only the standard library. Run each application **from its own backend directory**, because both scripts resolve their writable paths from the current working directory.

Text backend:

```bash
cd text_storage
python stock_text.py
```

This reads and writes `text_storage/data/{clients,produits,commandes,fournisseurs}.txt`.

SQLite backend, from the repository root in a separate terminal:

```bash
cd sqlite_storage
python stock_sqlite.py
```

This creates `sqlite_storage/gestion.db`, which is excluded by `.gitignore`.

Run the automated checks from the repository root:

```bash
python -m unittest discover -s tests -v
```

## Academic artefacts

- [French academic report (PDF)](docs/academic-report-fr.pdf).

No project presentation or video was found.

## Testing and limitations

Both menu applications were launched from a clean temporary copy and exited normally. The text variant kept its four files under `text_storage/data/`; the SQLite variant created only `sqlite_storage/gestion.db`. No generated database or test data was copied back to the repository. On Python 3.11, both existing temporary-storage tests passed, covering JSON-text stock reduction and accepted/rejected atomic SQLite orders.

The interface remains console-only. Input validation, authentication, concurrent access, migration of historical databases and stock reconciliation after editing or deleting existing orders were not tested.

## Authors

- Adam El Akkaoui
- Merizak Mehdi
