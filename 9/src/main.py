import unittest
import json
import requests

class TestApi(unittest.TestCase):
    def setUp(self):
        with open("config/config.json", "r") as configFile:
            self.config = json.load(configFile)

    def testProductsList(self):
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



    def testCreateProduct(self):

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


            self.assertNotEqual(productInList, None)

            self._compareProducts(productFromConfig, productInList)

            self._deleteProduct(str(addedProductId))



    def _getAllProducts(self):
        url = self.config['get_all_products_url']

        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

        return response.json()

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
