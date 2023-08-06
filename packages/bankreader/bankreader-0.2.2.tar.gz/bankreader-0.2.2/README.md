# bankreader

A light bank statement reader/parser. The project is oriented towards Romanian banks statements.
Input for the reader is the `already exported data` from your bank of choice, the library will not support web interaction with bank APIs (if existing). At least not in the foreseeable future.

The project is still new and may suffer API modifications.

Currently there is support only for the *Romanian Raiffeisen .xls statements*.

### Example

```python
from bankreader.romania import RaiffeisenStatement
import os

statement_xls_path = os.path.join('test', 'statements', 'Extras_de_cont_12345678_20012018_31012018.xls')

statement = RaiffeisenStatement(xls_path=statement_xls_path)

print(statement.account_number)
print(statement.client.iban)
print(statement.client.client_address)

for transaction in statement.transactions:
    print(transaction.amount)
    print(transaction.description)
    print(transaction.is_income)
```

Other examples can be seen in the tests.