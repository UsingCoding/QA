import unittest
import json
import requests

class TestApi(unittest.TestCase):
    def setUp(self):
        with open("config/config.json", "r") as configFile:
            self.config = json.load(configFile)

    def _testProductsList(self):
        productsList = self._getAllProducts()

        for product in productsList:
            self.assertTrue('id' in product)
            self.assertTrue('category_id' in product)
            self.assertTrue('title' in product)
            self.assertTrue('alias' in product)
            self.assertTrue('content' in product)
            self.assertTrue('price' in product)
            self.assertTrue('old_price' in product)
            self.assertTrue('status' in product)
            self.assertTrue('keywords' in product)
            self.assertTrue('description' in product)
            self.assertTrue('img' in product)
            self.assertTrue('hit' in product)
            self.assertTrue('cat' in product)



    def _testCreateProduct(self):

        url = self.config['add_product_url']

        for testData in self.config['creare_product_tests_data']:

            productFromConfig = testData['product']

            response = requests.post(url, json=productFromConfig)

            self.assertEqual(response.status_code, 200)

            if testData['response_code'] != 200:
                continue

            print(response.content)

            content = response.json()

            self.assertTrue('id' in content)

            addedProductId = content['id']

            print(addedProductId)

            productsList = self._getAllProducts()

            productInList = None

            for product in productsList:
                if int(product['id']) == addedProductId:
                    productInList = product
                    break


            self.assertNotEqual(productInList, None, "Added product not found")

            self._compareProducts(productFromConfig, productInList)

            self._deleteProduct(str(addedProductId))


    def _testProductsWithDuplicatesAliases(self):
        for testData in self.config['aliasing_tests_data']:

            firstlyAddedProductId = self._addProduct(testData['product'])

            print('Firstly added product id: ' + str(firstlyAddedProductId))

            # create same product twice to ensure that postfix will be added to alias
            addedProductId = self._addProduct(testData['product'])

            print('Secondly added product id: ' + str(addedProductId))

            productsList = self._getAllProducts()

            productInList = None

            for product in productsList:
                if int(product['id']) == addedProductId:
                    productInList = product
                    break

            self.assertNotEqual(productInList, None, "Added product not found")

            self.assertTrue(productInList['alias'].endswith(testData['alias_postfix']))

            self._deleteProduct(str(firstlyAddedProductId))
            self._deleteProduct(str(addedProductId))

    def _testDeleteProducts(self):

        for testData in self.config['delete_product_test_data']:
            if 'with_adding_new_product' in testData and testData['with_adding_new_product']:

                addedProductId = self._addProduct(testData['product'])

                self._deleteProduct(str(addedProductId))
                continue

            self._deleteProduct(testData['id'])

    def testEditProduct(self):
        url = self.config['edit_product_url']

        for testData in self.config['edit_product_test_data']:
            productId = self._addProduct(testData['product'])

            changedProductData = testData['changed_data']

            response = requests.post(url, json={'id': productId, **changedProductData})

            self.assertEqual(response.status_code, 200)

            print(response.content)

            product = self._findProductById(productId)

            self.assertNotEqual(product, None, 'Failed to find modified product')

            self._compareProducts(changedProductData, product)

    def _getAllProducts(self):
        url = self.config['get_all_products_url']

        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

        return response.json()

    def _findProductById(self, id):
        productsList = self._getAllProducts()

        for product in productsList:
            if int(product['id']) == id:
                return product

        return None

    def _addProduct(self, product):
        url = self.config['add_product_url']

        response = requests.post(url, json=product)

        self.assertEqual(response.status_code, 200)

        content = response.json()

        self.assertTrue('id' in content)

        return content['id']

    def _deleteProduct(self, id):
        url = self.config['delete_product_url'].replace('{ID}', id)

        print('Url to delete product: ' + url)

        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

    def _compareProducts(self, productFromConfig, productFromApi):

        self.assertEqual(productFromConfig['title'], productFromApi['title'])
        self.assertEqual(productFromConfig['category_id'], productFromApi['category_id'])

        if 'content' in productFromConfig:
            self.assertEqual(productFromConfig['content'], productFromApi['content'])

        self.assertEqual(productFromConfig['price'], productFromApi['price'])
        self.assertEqual(productFromConfig['old_price'], productFromApi['old_price'])

        if 'keywords' in productFromConfig:
            self.assertEqual(productFromConfig['keywords'], productFromApi['keywords'])

        if 'description' in productFromConfig:
            self.assertEqual(productFromConfig['description'], productFromApi['description'])

        if 'hit' in productFromConfig:
            self.assertEqual('1' if productFromConfig['hit'] != '1' and productFromConfig['hit'] != '0' else productFromConfig['hit'] , productFromApi['hit'])
        else:
            self.assertEqual(productFromApi['hit'], '0')

        if 'status' in productFromConfig:
            self.assertEqual('1' if productFromConfig['status'] != '1' and productFromConfig['status'] != '0' else productFromConfig['status'] , productFromApi['status'])
        else:
            self.assertEqual(productFromApi['status'], '1')




if __name__ == "__main__":
    unittest.main()
