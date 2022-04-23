# examples/things.py

# Let's get this party started!
from wsgiref.simple_server import make_server
from falcon import Request, Response
import falcon
from web3py import Web3

PATCH_API_KEY = "key_test_406d0d4c03d8da034afb695155318569"
BASE_URL = "https://api.patch.io"
NFT_ADDR = "0x63C93aC0D99EB331b3c0711b5F06721745b73eec"
PUBLIC_KEY = "0x2ca0649D6F544bFF02f3917E2419693d094166D2"
PRIVATE_KEY = "49e81553780e86df5e537ae647e63126bf8384204284b3491c20825a72129771"
ABI = ""
INFURA_URL = ""
# TODO: build erc721 contract, generate local privkey, set pubkey as owner

class SuccessCallbackResource:
    def on_get(self, req: Request, resp: Response):
        # TODO: Whitelist origin 80.113.211.254

        doc = req.stream.read(req.content_length or 0)
        print(f"Data: {doc}")
        print(f"Headers: {req.headers}")
        print(f"Params: {req.params}")

        # extract param "metadata[address]"
        target_addr: str = req.get_param("metadata[address]")
        if len(target_addr) != 42 and not target_addr.startswith("0x"):
            resp.status = falcon.HTTP_400
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "check the logs you bad boi"
            return

        # TODO: check patch api whether order paid

        # TODO: mint nft to target addr
        w3 = Web3(Web3.HTTPProvider(INFURA_URL))
        contract_instance = w3.eth.contract(address=NFT_ADDR, abi=ABI)
        contract_instance.functions.safeMint(target_addr).transact()

        # TODO: redirect back to frontend
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "success"


class FailureCallbackResource:
    def on_get(self, req: Request, resp: Response):
        doc = req.stream.read(req.content_length or 0)
        print(f"Data: {doc}")
        print(f"Headers: {req.headers}")
        print(f"Params: {req.params}")
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "failure"


app = falcon.App()
app.add_route('/success', SuccessCallbackResource())
app.add_route('/failure', FailureCallbackResource())


if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()
