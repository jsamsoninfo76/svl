# -*- coding: utf-8 -*-

"""
Test le module bank.
"""

import unittest

from bank import Account


from mockito import mock
from mockito import when
from mockito import verify


__date__ = 'Mon Jan 21 09:30:39 2013'


class TestJohnOuvreUnCompte(unittest.TestCase):
    
    def test_un_nouveau_compte_a_un_solde_de_0(self):
        """un nouveau compte a un solde de 0"""
        storage = mock()
        when(storage).select().thenReturn([])
        account = Account(storage)
        balance = account.balance()
        self.assertEquals(0, balance)


class TestJohnConsulteSonCompte(unittest.TestCase):

    def test_le_solde_est_correctement_calcule(self):
        """le solde est correctement calcule"""
        storage = mock()
        when(storage).select().thenReturn([10, -5])
        account = Account(storage)
        balance = account.balance()
        self.assertEquals(5, balance)


class TestJohnDebiteSonCompte(unittest.TestCase):
    
    def setUp(self):
        self.storage = mock()
        self.account = Account(self.storage)
    
    def test_debit_ajoute_une_operation_negative_a_l_historique(self):
        """debit ajoute une operation negative a l historique"""
        when(self.storage).select().thenReturn([10])
        amount = 5
        self.account.debit(amount)
        verify(self.storage).insert(-amount)

    def test_un_montant_negatif_leve_une_exception(self):
        """un montant negatif leve une exception"""
        when(self.storage).select().thenReturn([1])
        negative_amount = -1
        self.assertRaises(ValueError, self.account.debit, negative_amount)

    def test_debit_avec_montant_superieur_au_solde_leve_une_exception(self):
        """debit avec montant superieur au solde leve une exception"""
        when(self.storage).select().thenReturn([5])
        too_big_amount = 10
        self.assertRaises(ValueError, self.account.debit, too_big_amount)


class TestJohnCrediteSonCompte(unittest.TestCase):

    def setUp(self):
        self.storage = mock()
        self.account = Account(self.storage)
    
    def test_credit_ajoute_une_operation_a_l_historique(self):
        """credit ajoute une operation a l historique"""
        amount = 10
        self.account.credit(amount)
        verify(self.storage).insert(amount)

    def test_un_montant_negatif_leve_une_exception(self):
        """un montant negatif leve une exception"""
        montant_negatif = -1
        self.assertRaises(ValueError, self.account.credit, montant_negatif)


class TestJohnCrediteMadelaine(unittest.TestCase):

    def setUp(self):
        self.accountJohn = mock() 
        self.accountMadelaine = mock()
        self.trans = Transfert(self.storage)

    def test_debitJohn(self):
        """verifie si le debit a bien ete effectue"""
        amount = 10
        self.trans.transfert(self, accountJohn, accountMadelaine, amount)
	verify(self.storage).debit(amount)
    
    def test_creditMadelaine(self):
        """verifie si le credit a bien ete effectue"""
        amount = 10
        self.trans.transfert(self, accountJohn, accountMadelaine, amount)
	verify(self.storage).credit(amount)
    
    def test_balance_Compte_John(self, amount):
        when(accountJohn).debit(amount).thenRaise(ValueError)
        self.assertRaises(ValueError, self.trans.transfert(self, accountJohn, accountMadelaine, amount))

    def test_un_montant_negatif_leve_une_exception(self):
        """un montant negatif leve une exception"""
        amount = -1
        self.assertRaises(ValueError, self.trans.transfert(self, accountJohn, accountMadelaine, amount))

# eof
