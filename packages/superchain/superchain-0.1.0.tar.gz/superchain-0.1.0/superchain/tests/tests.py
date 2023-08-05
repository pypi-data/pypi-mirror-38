import unittest

from superchain.chain import chain


class ChainTest(unittest.TestCase):
    def setUp(self):
        self.keys = ['app', 'jobs', 'model']
        self.values = [1, 2, 3]

    def tearDown(self):
        pass

    def test_create_chain_when_no_args(self):
        chain_one = chain()
        self.assertEqual(None, chain_one.getkeys())

    def test_create_chain_when_keys_is_strs(self):
        chain_one = chain('app', 'jobs', 'model')
        self.assertEqual(self.keys, chain_one.getkeys())

    def test_create_chain_when_keys_is_list(self):
        chain_one = chain(['app', 'jobs', 'model'])
        self.assertEqual(self.keys, chain_one.getkeys())

    def test_create_chain_when_keys_is_tuple(self):
        chain_one = chain(('app', 'jobs', 'model'))
        self.assertEqual(self.keys, chain_one.getkeys())

    # def test_create_chain_when_keys_is_illegal(self):
    #     try:
    #         chain_one = chain({'app', 'jobs', 'model'})
    #     except Exception as exc:
    #         print(str(exc))
    #         self.assertEqual('args must be a list or tuple of types', chain_one.getkeys())


if __name__ == '__main__':
    unittest.main()
