import unittest
import requests

class TestApi(unittest.TestCase):
    def testRateEuro(self):
        self._test('http://localhost:44302/rate/euro', 200, {'euro': {'rate': 90.36}})

    def testRateUsdollar(self):
        self._test('http://localhost:44302/rate/usdollar', 200, {'usdollar': {'rate': 76.21}})

    def testRateTenge(self):
        self._test('http://localhost:44302/tenge', 404)

    def _test(self, url, responseCode, responseContent = None):
        response = requests.get(url)

        self.assertEqual(response.status_code, responseCode)

        if responseContent != None:
            self.assertEqual(response.json(), responseContent)


if __name__ == "__main__":
    unittest.main()
