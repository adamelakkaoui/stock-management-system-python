# Stock Management System – Python

Academic console application implementing CRUD operations for clients, products, orders and suppliers with two storage approaches: JSON-formatted text files and SQLite.

## Features

- Object-oriented `Client`, `Produit`, `Commande` and `Fournisseur` entities.
- Create, display, update and delete operations.
- Product-stock checks and stock updates when an order is added.
- Order-total calculation and hierarchical console menus.
- Independent JSON-text and relational SQLite variants.

## Storage design

The application is implemented in two versions that expose the same management operations:

- **Text-file version:** persistent storage using text files for clients, products, orders and suppliers.
- **SQLite3 version:** relational storage using a local SQLite database.

Both versions manage the same four entities and provide Create, Read, Update and Delete operations through a console menu.

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

This creates `sqlite_storage/gestion.db`.

## Academic artefacts

- [French academic report (PDF)](docs/academic-report-fr.pdf).

## Tests, limitations and perspectives

The report documents unit tests for the `Client`, `Produit`, `Commande` and `Fournisseur` classes, data-management tests for addition, display, modification and deletion, stock tests to verify quantity updates and prevent orders beyond available stock, and persistence tests for both SQLite3 and text-file storage.

The limitations identified in the report are the rudimentary nature of text-file storage, the console-only interface, limited error handling, the absence of user access rights, and SQLite3's limitations for large-scale or concurrent multi-user use.

The proposed improvements include a graphical interface, authentication and roles, stronger exception handling, migration toward MySQL or PostgreSQL for larger deployments, and additional functions such as exports, stock alerts and sales/order statistics.

## Authors

- Adam El Akkaoui
- Merizak Mehdi
