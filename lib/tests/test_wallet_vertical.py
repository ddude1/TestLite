import unittest
from unittest import mock

import lib.bitcoin as bitcoin
import lib.keystore as keystore
import lib.storage as storage
import lib.wallet as wallet


# TODO: 2fa
class TestWalletKeystoreAddressIntegrity(unittest.TestCase):

    gap_limit = 1  # make tests run faster

    def _check_seeded_keystore_sanity(self, ks):
        self.assertTrue (ks.is_deterministic())
        self.assertFalse(ks.is_watching_only())
        self.assertFalse(ks.can_import())
        self.assertTrue (ks.has_seed())

    def _check_xpub_keystore_sanity(self, ks):
        self.assertTrue (ks.is_deterministic())
        self.assertTrue (ks.is_watching_only())
        self.assertFalse(ks.can_import())
        self.assertFalse(ks.has_seed())

    def _create_standard_wallet(self, ks):
        store = storage.WalletStorage('if_this_exists_mocking_failed_648151893')
        store.put('keystore', ks.dump())
        store.put('gap_limit', self.gap_limit)
        w = wallet.Standard_Wallet(store)
        w.synchronize()
        return w

    def _create_multisig_wallet(self, ks1, ks2):
        store = storage.WalletStorage('if_this_exists_mocking_failed_648151893')
        multisig_type = "%dof%d" % (2, 2)
        store.put('wallet_type', multisig_type)
        store.put('x%d/' % 1, ks1.dump())
        store.put('x%d/' % 2, ks2.dump())
        store.put('gap_limit', self.gap_limit)
        w = wallet.Multisig_Wallet(store)
        w.synchronize()
        return w

    @mock.patch.object(storage.WalletStorage, '_write')
    def test_electrum_seed_standard(self, mock_write):
        seed_words = 'cycle rocket west magnet parrot shuffle foot correct salt library feed song'
        self.assertEqual(bitcoin.seed_type(seed_words), 'standard')

        ks = keystore.from_seed(seed_words, '', False)

        self._check_seeded_keystore_sanity(ks)
        self.assertTrue(isinstance(ks, keystore.BIP32_KeyStore))

        self.assertEqual(ks.xpub, 'ToEA6epvY6iUs9r4Qi3wRqytDNaGbuq2niqnQVN3Tck7RPPm9oHWLmXCFRC9vPdQ7tjBad6BERPFFDfzh3X48LDpeosf65CRBQsyXUzJpcpNygU')

        w = self._create_standard_wallet(ks)

        self.assertEqual(w.get_receiving_addresses()[0], 'XYizk38coTEyyLdztrQ1NL23mnN2PJtdmE')
        self.assertEqual(w.get_change_addresses()[0], 'XVntqgiJQq7EAm3z5e1DF6xgHyoa4wmEod')

    @mock.patch.object(storage.WalletStorage, '_write')
    def test_electrum_seed_old(self, mock_write):
        seed_words = 'powerful random nobody notice nothing important anyway look away hidden message over'
        self.assertEqual(bitcoin.seed_type(seed_words), 'old')

        ks = keystore.from_seed(seed_words, '', False)

        self._check_seeded_keystore_sanity(ks)
        self.assertTrue(isinstance(ks, keystore.Old_KeyStore))

        self.assertEqual(ks.mpk, 'e9d4b7866dd1e91c862aebf62a49548c7dbf7bcc6e4b7b8c9da820c7737968df9c09d5a3e271dc814a29981f81b3faaf2737b551ef5dcc6189cf0f8252c442b3')

        w = self._create_standard_wallet(ks)

        self.assertEqual(w.get_receiving_addresses()[0], 'XReU5KVKwv7KLNUwaokkQX3JBFajsfqF6R')
        self.assertEqual(w.get_change_addresses()[0], 'XVmjyxdhXn3H2daeKgp12djvyhCWX9kF24')

    @mock.patch.object(storage.WalletStorage, '_write')
    def test_bip39_seed_bip44_standard(self, mock_write):
        seed_words = 'treat dwarf wealth gasp brass outside high rent blood crowd make initial'
        self.assertEqual(keystore.bip39_is_checksum_valid(seed_words), (True, True))

        ks = keystore.from_bip39_seed(seed_words, '', "m/44'/0'/0'")

        self.assertTrue(isinstance(ks, keystore.BIP32_KeyStore))

        self.assertEqual(ks.xpub, 'ToEA6n5FacYnui6DhQK3iYcscmHz5EEXBk2DUnASTzpejhxg33ApUuLzSdCHgWRud6xWQSUxDgHzPC8iwLiCTNg3ftdTbstzcYKQ6v6KJMqfQG1')

        w = self._create_standard_wallet(ks)

        self.assertEqual(w.get_receiving_addresses()[0], 'XH5M4z6eofyLo8eP85BPhynRAygD62RkrT')
        self.assertEqual(w.get_change_addresses()[0], 'XScKSe17vhZns1ZoAfocF3R4cQWpAM38fd')

    @mock.patch.object(storage.WalletStorage, '_write')
    def test_electrum_multisig_seed_standard(self, mock_write):
        seed_words = 'blast uniform dragon fiscal ensure vast young utility dinosaur abandon rookie sure'
        self.assertEqual(bitcoin.seed_type(seed_words), 'standard')

        ks1 = keystore.from_seed(seed_words, '', True)
        self._check_seeded_keystore_sanity(ks1)
        self.assertTrue(isinstance(ks1, keystore.BIP32_KeyStore))
        self.assertEqual(ks1.xpub, 'ToEA6epvY6iUs9r4RZUe2Ng5EvEVMEztmfxnJHNDie3uhb373XD7gD7c5HGcfFZX5mCxnMGM3knhJJVdD2YHgxAs6Ztc2VJYwU6aD1x5CsoH2Qf')

        ks2 = keystore.from_xpub('ToEA6ij48MPyPqZFWsNtjbpbBMnwFrsn4uSnsH95RV5ppgt2ZEFkk1p52jEFjnnAydSV5rmmmYEBmatiqpHEv5LJVFuXysFXeP2zUqimuCd1So2')
        self._check_xpub_keystore_sanity(ks2)
        self.assertTrue(isinstance(ks2, keystore.BIP32_KeyStore))

        w = self._create_multisig_wallet(ks1, ks2)

        self.assertEqual(w.get_receiving_addresses()[0], '8XbqdmkckfENFqbX9znDwjbyXBzZFR68bA')
        self.assertEqual(w.get_change_addresses()[0], '8J8PimHwv2XqDon32AWxEG2geBNtcBrJ6H')

    @mock.patch.object(storage.WalletStorage, '_write')
    def test_bip39_multisig_seed_bip45_standard(self, mock_write):
        seed_words = 'treat dwarf wealth gasp brass outside high rent blood crowd make initial'
        self.assertEqual(keystore.bip39_is_checksum_valid(seed_words), (True, True))

        ks1 = keystore.from_bip39_seed(seed_words, '', "m/45'/0")
        self.assertTrue(isinstance(ks1, keystore.BIP32_KeyStore))
        self.assertEqual(ks1.xpub, 'ToEA6in9EDqryvMFHjxvhQLV6QsvD2HLJAb1Jo9BMLDV8GBu6gbhp73hGKvdMssjKTpKYPAcTTDqe2eVckxnSSreqz1VrvYe6LdrpT6AdPd3AvC')

        ks2 = keystore.from_xpub('ToEA6ij48MPyPqZFWsNtjbpbBMnwFrsn4uSnsH95RV5ppgt2ZEFkk1p52jEFjnnAydSV5rmmmYEBmatiqpHEv5LJVFuXysFXeP2zUqimuCd1So2')
        self._check_xpub_keystore_sanity(ks2)
        self.assertTrue(isinstance(ks2, keystore.BIP32_KeyStore))

        w = self._create_multisig_wallet(ks1, ks2)

        self.assertEqual(w.get_receiving_addresses()[0], '8Jp2qPMJJqxU6XAbXKj8rs7MbwkQ31hkze')
        self.assertEqual(w.get_change_addresses()[0], '8WrLRiHS11wgLSJhHbyjemgNvHZJD3UN35')

