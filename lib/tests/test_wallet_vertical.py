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

        self.assertEqual(w.get_receiving_addresses()[0], 'GfDgK26xXn6ZiJUnzL5DRgwwV7q86E28cq')
        self.assertEqual(w.get_change_addresses()[0], 'GcHaQfge99xouitnB7gRJTta1KGfqFqwFq')

    @mock.patch.object(storage.WalletStorage, '_write')
    def test_electrum_seed_old(self, mock_write):
        seed_words = 'powerful random nobody notice nothing important anyway look away hidden message over'
        self.assertEqual(bitcoin.seed_type(seed_words), 'old')

        ks = keystore.from_seed(seed_words, '', False)

        self._check_seeded_keystore_sanity(ks)
        self.assertTrue(isinstance(ks, keystore.Old_KeyStore))

        self.assertEqual(ks.mpk, 'e9d4b7866dd1e91c862aebf62a49548c7dbf7bcc6e4b7b8c9da820c7737968df9c09d5a3e271dc814a29981f81b3faaf2737b551ef5dcc6189cf0f8252c442b3')

        w = self._create_standard_wallet(ks)

        self.assertEqual(w.get_receiving_addresses()[0], 'GY99eJTfgExu5LKjgHRxTsyBtb3qVeYLeU')
        self.assertEqual(w.get_change_addresses()[0], 'GcGRYwc3G6trmbRSRAVD5zfph2fcAxMBEJ')

    @mock.patch.object(storage.WalletStorage, '_write')
    def test_bip39_seed_bip44_standard(self, mock_write):
        seed_words = 'treat dwarf wealth gasp brass outside high rent blood crowd make initial'
        self.assertEqual(keystore.bip39_is_checksum_valid(seed_words), (True, True))

        ks = keystore.from_bip39_seed(seed_words, '', "m/44'/0'/0'")

        self.assertTrue(isinstance(ks, keystore.BIP32_KeyStore))

        self.assertEqual(ks.xpub, 'ToEA6n5FacYnui6DhQK3iYcscmHz5EEXBk2DUnASTzpejhxg33ApUuLzSdCHgWRud6xWQSUxDgHzPC8iwLiCTNg3ftdTbstzcYKQ6v6KJMqfQG1')

        w = self._create_standard_wallet(ks)

        self.assertEqual(w.get_receiving_addresses()[0], 'GPa2dy4zXzpvY6VBDYrbmLiJtK9JkXMbfm')
        self.assertEqual(w.get_change_addresses()[0], 'GZ711cyTf2RNbyQbG9UpJQLxKjyus57UkG')

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

        self.assertEqual(w.get_receiving_addresses()[0], 'bVFFc3ivKkH53swKo76aS8qggzFkrA5Ty6')
        self.assertEqual(w.get_change_addresses()[0], 'bFmoh3GFV7aY1r7qfGqJifGPoye6GKmYw5')

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

        self.assertEqual(w.get_receiving_addresses()[0], 'bGTSofKbsw1AtZWQAS3VMGM4mk1biTiZ9n')
        self.assertEqual(w.get_change_addresses()[0], 'bUVkPzFja6zP8UeVviJ69Av665pVpZSR9Q')

