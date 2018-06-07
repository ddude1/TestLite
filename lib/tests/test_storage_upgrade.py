import shutil
import tempfile

from lib.storage import WalletStorage
from lib.wallet import Wallet

from lib.tests.test_wallet import WalletTestCase


# TODO add other wallet types: 2fa, xpub-only
# TODO hw wallet with client version 2.6.x (single-, and multiacc)
class TestStorageUpgrade(WalletTestCase):

    def test_upgrade_from_client_1_9_8_seeded(self):
        wallet_str = "{'addr_history':{'177hEYTccmuYH8u68pYfaLteTxwJrVgvJj':[],'15V7MsQK2vjF5aEXLVG11qi2eZPZsXdnYc':[],'1DgrwN2JCDZ6uPMSvSz8dPeUtaxLxWM2kf':[],'1H3mPXHFzA8UbvhQVabcDjYw3CPb3djvxs':[],'1DjtUCcQwwzA3GSPA7Kd79PMnri7tLDPYC':[],'1PGEgaPG1XJqmuSj68GouotWeYkCtwo4wm':[],'1PAgpPxnL42Hp3cWxmSfdChPqqGiM8g7zj':[],'1HocPduHmQUJerpdaLG8DnmxvnDCVQwWsa':[]},'accounts_expanded':{},'master_public_key':'756d1fe6ded28d43d4fea902a9695feb785447514d6e6c3bdf369f7c3432fdde4409e4efbffbcf10084d57c5a98d1f34d20ac1f133bdb64fa02abf4f7bde1dfb','use_encryption':False,'seed':'2605aafe50a45bdf2eb155302437e678','accounts':{0:{0:['1DjtUCcQwwzA3GSPA7Kd79PMnri7tLDPYC','1PAgpPxnL42Hp3cWxmSfdChPqqGiM8g7zj','177hEYTccmuYH8u68pYfaLteTxwJrVgvJj','1PGEgaPG1XJqmuSj68GouotWeYkCtwo4wm','15V7MsQK2vjF5aEXLVG11qi2eZPZsXdnYc'],1:['1H3mPXHFzA8UbvhQVabcDjYw3CPb3djvxs','1HocPduHmQUJerpdaLG8DnmxvnDCVQwWsa','1DgrwN2JCDZ6uPMSvSz8dPeUtaxLxWM2kf']}},'seed_version':4}"
        self._upgrade_storage(wallet_str)

    
    # TODO pre-2.0 mixed wallets are not split currently
    #def test_upgrade_from_client_1_9_8_mixed(self):
    #    wallet_str = "{'addr_history':{'15V7MsQK2vjF5aEXLVG11qi2eZPZsXdnYc':[],'177hEYTccmuYH8u68pYfaLteTxwJrVgvJj':[],'1DjtUCcQwwzA3GSPA7Kd79PMnri7tLDPYC':[],'1PGEgaPG1XJqmuSj68GouotWeYkCtwo4wm':[],'1PAgpPxnL42Hp3cWxmSfdChPqqGiM8g7zj':[],'1DgrwN2JCDZ6uPMSvSz8dPeUtaxLxWM2kf':[],'1H3mPXHFzA8UbvhQVabcDjYw3CPb3djvxs':[],'1HocPduHmQUJerpdaLG8DnmxvnDCVQwWsa':[]},'accounts_expanded':{},'master_public_key':'756d1fe6ded28d43d4fea902a9695feb785447514d6e6c3bdf369f7c3432fdde4409e4efbffbcf10084d57c5a98d1f34d20ac1f133bdb64fa02abf4f7bde1dfb','use_encryption':False,'seed':'2605aafe50a45bdf2eb155302437e678','accounts':{0:{0:['1DjtUCcQwwzA3GSPA7Kd79PMnri7tLDPYC','1PAgpPxnL42Hp3cWxmSfdChPqqGiM8g7zj','177hEYTccmuYH8u68pYfaLteTxwJrVgvJj','1PGEgaPG1XJqmuSj68GouotWeYkCtwo4wm','15V7MsQK2vjF5aEXLVG11qi2eZPZsXdnYc'],1:['1H3mPXHFzA8UbvhQVabcDjYw3CPb3djvxs','1HocPduHmQUJerpdaLG8DnmxvnDCVQwWsa','1DgrwN2JCDZ6uPMSvSz8dPeUtaxLxWM2kf'],'mpk':'756d1fe6ded28d43d4fea902a9695feb785447514d6e6c3bdf369f7c3432fdde4409e4efbffbcf10084d57c5a98d1f34d20ac1f133bdb64fa02abf4f7bde1dfb'}},'imported_keys':{'15CyDgLffJsJgQrhcyooFH4gnVDG82pUrA':'5JyVyXU1LiRXATvRTQvR9Kp8Rx1X84j2x49iGkjSsXipydtByUq','1Exet2BhHsFxKTwhnfdsBMkPYLGvobxuW6':'L3Gi6EQLvYw8gEEUckmqawkevfj9s8hxoQDFveQJGZHTfyWnbk1U','1364Js2VG66BwRdkaoxAaFtdPb1eQgn8Dr':'L2sED74axVXC4H8szBJ4rQJrkfem7UMc6usLCPUoEWxDCFGUaGUM'},'seed_version':4}"
    #    self._upgrade_storage(wallet_str, accounts=2)

    def test_upgrade_from_client_2_0_4_seeded(self):
        wallet_str = '{"accounts":{"0":{"change":["03d8e267e8de7769b52a8727585b3c44b4e148b86b2c90e3393f78a75bd6aab83f","03f09b3562bec870b4eb8626c20d449ee85ef17ea896a6a82b454e092eef91b296","02df953880df9284715e8199254edcf3708c635adc92a90dbf97fbd64d1eb88a36"],"receiving":["02cd4d73d5e335dafbf5c9338f88ceea3d7511ab0f9b8910745ac940ff40913a30","0243ed44278a178101e0fb14d36b68e6e13d00fe3434edb56e4504ea6f5db2e467","0367c0aa3681ec3635078f79f8c78aa339f19e38d9e1c9e2853e30e66ade02cac3","0237d0fe142cff9d254a3bdd3254f0d5f72676b0099ba799764a993a0d0ba80111","020a899fd417527b3929c8f625c93b45392244bab69ff91b582ed131977d5cd91e","039e84264920c716909b88700ef380336612f48237b70179d0b523784de28101f7","03125452df109a51be51fe21e71c3a4b0bba900c9c0b8d29b4ee2927b51f570848","0291fa554217090bab96eeff63e1c6fdec37358ed597d18fa32c60c02a48878c8c","030b6354a4365bab55e86269fb76241fd69716f02090ead389e1fce13d474aa569","023dcba431d8887ab63595f0df1e978e4a5f1c3aac6670e43d03956448a229f740","0332a61cbe04fe027033369ce7569b860c24462878bdd8c0332c22a3f5fdcc1790","021249480422d93dba2aafcd4575e6f630c4e3a2a832dd8a15f884e1052b6836e4","02516e91dede15d3a15dd648591bb92e107b3a53d5bc34b286ab389ce1af3130aa","02e1da3dddd81fa6e4895816da9d4b8ab076d6ea8034b1175169c0f247f002f4cf","0390ef1e3fdbe137767f8b5abad0088b105eee8c39e075305545d405be3154757a","03fca30eb33c6e1ffa071d204ccae3060680856ae9b93f31f13dd11455e67ee85d","034f6efdbbe1bfa06b32db97f16ff3a0dd6cf92769e8d9795c465ff76d2fbcb794","021e2901009954f23d2bf3429d4a531c8ca3f68e9598687ef816f20da08ff53848","02d3ccf598939ff7919ee23d828d229f85e3e58842582bf054491c59c8b974aa6e","03a1daffa39f42c1aaae24b859773a170905c6ee8a6dab8c1bfbfc93f09b88f4db"],"xpub":"xpub661MyMwAqRbcFsrzES8RWNiD7RxDqT4p8NjvTY9mLi8xdphQ9x1TiY8GnqCpQx4LqJBdcGeXrsAa2b2G7ZcjJcest9wHcqYfTqXmQja6vfV"}},"accounts_expanded":{},"master_private_keys":{"x/":"xprv9s21ZrQH143K3PnX8QbR9EmUZQ7jRzLxm9pKf9k9nNbym2NFcQhDAjonwZ39jtWLYp6qk5UHotj13p2y7w1ZhhvvyV5eCcaPUrKofs9CXQ9"},"master_public_keys":{"x/":"xpub661MyMwAqRbcFsrzES8RWNiD7RxDqT4p8NjvTY9mLi8xdphQ9x1TiY8GnqCpQx4LqJBdcGeXrsAa2b2G7ZcjJcest9wHcqYfTqXmQja6vfV"},"seed":"seven direct thunder glare prevent please fatal blush buzz artefact gate vendor above","seed_version":11,"use_encryption":false,"wallet_type":"standard"}'
        self._upgrade_storage(wallet_str)

    def test_upgrade_from_client_2_0_4_importedkeys(self):
        wallet_str = '{"accounts":{"/x":{"imported":{"1364Js2VG66BwRdkaoxAaFtdPb1eQgn8Dr":["0344b1588589958b0bcab03435061539e9bcf54677c104904044e4f8901f4ebdf5","L2sED74axVXC4H8szBJ4rQJrkfem7UMc6usLCPUoEWxDCFGUaGUM"],"15CyDgLffJsJgQrhcyooFH4gnVDG82pUrA":["04575f52b82f159fa649d2a4c353eb7435f30206f0a6cb9674fbd659f45082c37d559ffd19bea9c0d3b7dcc07a7b79f4cffb76026d5d4dff35341efe99056e22d2","5JyVyXU1LiRXATvRTQvR9Kp8Rx1X84j2x49iGkjSsXipydtByUq"],"1Exet2BhHsFxKTwhnfdsBMkPYLGvobxuW6":["0389508c13999d08ffae0f434a085f4185922d64765c0bff2f66e36ad7f745cc5f","L3Gi6EQLvYw8gEEUckmqawkevfj9s8hxoQDFveQJGZHTfyWnbk1U"]}}},"accounts_expanded":{},"use_encryption":false,"wallet_type":"imported"}'
        self._upgrade_storage(wallet_str)

    def test_upgrade_from_client_2_0_4_watchaddresses(self):
        wallet_str = '{"accounts":{"/x":{"imported":{"1DgrwN2JCDZ6uPMSvSz8dPeUtaxLxWM2kf":[null,null],"1H3mPXHFzA8UbvhQVabcDjYw3CPb3djvxs":[null,null],"1HocPduHmQUJerpdaLG8DnmxvnDCVQwWsa":[null,null]}}},"accounts_expanded":{},"wallet_type":"imported"}'
        self._upgrade_storage(wallet_str)


##########

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from lib.plugins import Plugins
        from lib.simple_config import SimpleConfig

        cls.electrum_path = tempfile.mkdtemp()
        config = SimpleConfig({'electrum_path': cls.electrum_path})

        gui_name = 'cmdline'
        # TODO it's probably wasteful to load all plugins... only need Trezor
        Plugins(config, True, gui_name)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(cls.electrum_path)

    def _upgrade_storage(self, wallet_json, accounts=1):
        storage = self._load_storage_from_json_string(wallet_json, manual_upgrades=True)

        if accounts == 1:
            self.assertFalse(storage.requires_split())
            if storage.requires_upgrade():
                storage.upgrade()
                self._sanity_check_upgraded_storage(storage)
        else:
            self.assertTrue(storage.requires_split())
            new_paths = storage.split_accounts()
            self.assertEqual(accounts, len(new_paths))
            for new_path in new_paths:
                new_storage = WalletStorage(new_path, manual_upgrades=False)
                self._sanity_check_upgraded_storage(new_storage)

    def _sanity_check_upgraded_storage(self, storage):
        self.assertFalse(storage.requires_split())
        self.assertFalse(storage.requires_upgrade())
        w = Wallet(storage)

    def _load_storage_from_json_string(self, wallet_json, manual_upgrades=True):
        with open(self.wallet_path, "w") as f:
            f.write(wallet_json)
        storage = WalletStorage(self.wallet_path, manual_upgrades=manual_upgrades)
        return storage
