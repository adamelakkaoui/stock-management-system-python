# Stock Management System – Python

Academic console application implementing CRUD operations for clients, products, orders, and suppliers with two interchangeable storage approaches: JSON-formatted text files and SQLite.

## Verified features

- Object-oriented `Client`, `Produit`, `Commande`, and `Fournisseur` entities.
- Create, display, update, and delete operations.
- Product stock checks and stock updates when orders are added.
- Order-total calculation.
- Hierarchical interactive console menus.
- Text-file and relational SQLite variants.

## Privacy and portfolio correction

The submitted text files and SQLite database contained populated contact/order examples and were excluded. This repository starts with empty JSON arrays and generates a local SQLite database on first use. The SQLite script previously launched its interactive menu on import; it now uses a `main()` guard so it can be imported and tested without blocking.

The portfolio copy also verifies every requested product before inserting an SQLite order and rolls back database errors, avoiding empty or partially written orders.

## Requirements and use

Python 3.10+; all dependencies are in the standard library.

```bash
python text_storage/stock_text.py
python sqlite_storage/stock_sqlite.py
python -m unittest discover -s tests -v
```

Run each version from its own directory so relative data paths remain local to that backend.

## Limitations

The interface is console-only. Input validation, authentication, concurrent access, and stock reconciliation when existing orders are edited or deleted remain limited. SQLite is intended for local use, while the text backend is JSON stored in `.txt` files rather than an unstructured line format.

## Authors

- Adam El Akkaoui
- Merizak Mehdi

## Academic artefacts

- [French academic report (PDF)](docs/academic-report-fr.pdf). No presentation or video was found. Public examples contain no original contact or inventory records.

## Testing and limitations

On Python 3.11, two temporary-storage tests passed for JSON-text stock reduction and accepted/rejected atomic SQLite orders; byte-compilation passed. Interactive menus, concurrent access and historical database migration were not tested. The portfolio copy makes SQLite order updates atomic.
