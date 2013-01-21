# -*- coding: utf-8 -*-

"""
Le module banque propose des comptes bancaires avec historiques.

Un client ouvre un compte bancaire. ::

  >>> storage = OperationStorage()
  >>> account = Account(storage)

Un compte est par défaut à 0. ::

  >>> account.balance()
  0

Un client crédite son compte. ::

  >>> account.credit(10)
  >>> account.balance()
  10

  >>> account.credit(5)
  >>> account.balance()
  15
  
Un client peut débiter un compte.

  >>> account.debit(5)
  >>> account.balance()
  10


Un client demande l'historique de son compte. ::

  >>> account.history()
  [10, 5, -5]
"""


__date__ = 'Mon Jan 14 09:12:01 2013'



class Account(object):
    """Compte bancaire avec historique des opérations."""

    def __init__(self, storage):
        self.operations = storage

    def balance(self):
        """Retourne la balance courante du compte."""
        return sum(self.operations.select())

    def history(self):
        """Retourne une copie de l'historique des opérations."""
        return list(self.operations)  # return a copy of the list

    def credit(self, amount):
        """Crédite le compte du montant passé en paramètre.

        ValueError est levée si le montant est négatif.
        """
        self._negative_amount_raises_value_error(amount)
        self.operations.insert(amount)

    def debit(self, amount):
        """Débite le compte du montant passé en paramètre.

        ValueError est levée si le montant est négatif.
        """
        self._negative_amount_raises_value_error(amount)
        balance = self.balance()
        if amount > balance:
            raise ValueError(
                "amount {0} should be lower than balance {1}".format(amount, balance))
        self.operations.insert(-amount)

    def _negative_amount_raises_value_error(self, amount):
        if amount < 0:
            raise ValueError(
                "amount should be positive, received: {0}".format(amount))


# eof
