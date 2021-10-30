import unittest

from playsh.store import Store


class StoreTest(unittest.TestCase):
    def test_store_and_retrive(self):
        # given
        store = Store()
        value_to_store = 1234

        # when
        store["my-variable"] = value_to_store
        value_retrived = store["my-variable"]

        # then
        self.assertEqual(value_retrived, value_to_store)

    def test_iterate(self):
        # given
        store = Store()
        items_to_store = {"name1": 123, "name2": 42, "name3": 6612}
        for name, value in items_to_store.items():
            store[name] = value

        # when
        items_retrived = dict()
        for name, value in store:
            items_retrived[name] = value

        # then
        self.assertEqual(items_to_store, items_retrived)


if __name__ == "__main__":
    unittest.main()
