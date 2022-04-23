# examples/things.py

# Let's get this party started!
from wsgiref.simple_server import make_server
from falcon import Request, Response
import falcon

PATCH_API_KEY = "key_test_406d0d4c03d8da034afb695155318569"
BASE_URL = "https://api.patch.io"
NFT_ADDR = ""
PUBLIC_KEY = "0x2ca0649D6F544bFF02f3917E2419693d094166D2"
PRIVATE_KEY = "49e81553780e86df5e537ae647e63126bf8384204284b3491c20825a72129771"

# TODO: build erc721 contract, generate local privkey, set pubkey as owner

class SuccessCallbackResource:
    def on_get(self, req: Request, resp: Response):
        # TODO: Whitelist origin 80.113.211.254

        doc = req.stream.read(req.content_length or 0)
        print(f"Data: {doc}")
        print(f"Headers: {req.headers}")
        print(f"Params: {req.params}")
        # TODO: extract param "metadata[address]" and store

        # TODO: check patch api whether order paid

        # TODO: assemble tx to mint nft

        # TODO: submit to infura

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
