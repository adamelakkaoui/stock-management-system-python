# Verification

Test environment: Python 3.11 on Windows.

`python -m unittest discover -s tests -v` completed successfully: 2 tests passed. The tests create temporary storage only and verify stock reduction in the JSON-text backend plus successful and rejected atomic orders in SQLite. Python byte-compilation also completed successfully.

Interactive menu input, concurrent use, and migrations of existing databases were not tested.
