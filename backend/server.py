# examples/things.py

# Let's get this party started!
from wsgiref.simple_server import make_server
from falcon import Request, Response
import falcon
from web3 import Web3
import json
import patch_api
from carboncalc import CarbonCalculator, ChainExplorerConfig


PATCH_API_KEY = "key_test_406d0d4c03d8da034afb695155318569"
BASE_URL = "https://api.patch.io"
NFT_ADDR = "0xee6977502dD85a8eE1cdC81A6Cb9f6Ea541c5Ef6"
PUBLIC_KEY = "0x3ded79F5141f5c0aF23c6c7907A6E279160542FB"
PRIVATE_KEY = "0x59f3622b1ecd1a25f042d893fa6d101194c6722840f55771c131731f1a204e65"
ABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"imageURI","type":"string"}],"name":"formatTokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"carbonAmount","type":"uint256"}],"name":"safeMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"svg","type":"string"}],"name":"svgToImageURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
INFURA_URL = "https://polygon-mumbai.infura.io/v3/5e3d186095d04216ba93cd1c52a6ad61"
REDIRECT_URL = "https://checkout.patch.io/che_test_d1101c10f00dad1402f21ccc54f5619d?amount={amount}&metadata[address]={address}"
FRONTEND_SUCCESS_URL = None  # auto-redirects to certificate if None
FRONTEND_URL = "http://"
FALLBACK_URL = "https://google.com"  # TODO: replace with frontend url

KNOWN_ACCOUNTS = []


class EtherscanApiConfig:
    ETHERSCAN = {
        "apiKey": "RVXR4IXM4K7TKUI2H7XQBGHZDDBP393KFP",
        "baseUri": "api.etherscan.io",
    }  # dom
    POLYGONSCAN = {
        "apiKey": "V99R51EYZRATHEK6QK3T3ACPXHFCBMFCWF",
        "baseUri": "api.polygonscan.com",
    }  # rmfblqsrfthfxssbrk - password: rmfblqsrfthfxssbrk@bvhrk.com (throwaway)


# TODO: build erc721 contract, generate local privkey, set pubkey as owner


class SuccessCallbackResource:
    def on_get(self, req: Request, resp: Response):
        # TODO: Whitelist origin 80.113.211.254

        client = patch_api.ApiClient(api_key=PATCH_API_KEY)

        doc = req.stream.read(req.content_length or 0)
        print(f"Data: {doc}")
        print(f"Headers: {req.headers}")
        print(f"Params: {req.params}")

        target_addr: str = req.get_param("metadata[address]")
        if (
            target_addr is None
            or len(target_addr) != 42
            or not target_addr.startswith("0x")
        ):
            resp.status = falcon.HTTP_400
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "missing param: metadata[address]"
            return

        if target_addr in KNOWN_ACCOUNTS:
            resp.status = falcon.HTTP_403
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "This address has already claimed."
            return

        order_id = req.get_param("order_id")
        print(f"Got order id: {order_id}")
        if order_id is None:
            resp.status = falcon.HTTP_400
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "missing param: order_id"
            return

        order = client.orders.retrieve_order(id=order_id)
        print(f"Got order: {order}")
        order = order.data
        if order is None:
            resp.status = falcon.HTTP_400
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "patch api returned empty order"
            return

        test_addr = order.metadata.get("address")
        if test_addr is None or test_addr != target_addr:
            resp.status = falcon.HTTP_400
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "url vs address mismatch"
            return

        # prepare minting tx
        print(f"Preparing tx for {target_addr}")
        w3 = Web3(Web3.HTTPProvider(INFURA_URL))
        nonce = w3.eth.get_transaction_count(PUBLIC_KEY)
        contract_instance = w3.eth.contract(address=NFT_ADDR, abi=ABI)
        amount = int(order.mass_g / 1_000_000)  # in tons
        tx = contract_instance.functions.safeMint(
            w3.toChecksumAddress(target_addr), amount
        ).buildTransaction(
            {
                "chainId": 80001,
                "gas": 120_000,
                "maxFeePerGas": w3.toWei("2", "gwei"),
                "maxPriorityFeePerGas": w3.toWei("1", "gwei"),
                "nonce": nonce,
            }
        )

        # send mint tx
        print(f"Sending tx for {target_addr}")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        KNOWN_ACCOUNTS.append(target_addr)

        # redirect back to frontend
        print(f"Redirecting")
        registry_url = order.registry_url
        raise falcon.HTTPPermanentRedirect(
            location=FRONTEND_SUCCESS_URL or registry_url or FALLBACK_URL
        )


class FailureCallbackResource:
    def on_get(self, req: Request, resp: Response):
        doc = req.stream.read(req.content_length or 0)
        print(f"Data: {doc}")
        print(f"Headers: {req.headers}")
        print(f"Params: {req.params}")
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "failure"


class EstimationResource:
    def on_get(self, req: Request, resp: Response):
        target_address = req.get_param("address")
        if target_address is None:
            # TODO: redirect to regular frontend
            resp.status = falcon.HTTP_400
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "missing param: address"
            return

        calc = CarbonCalculator(chainConfig=ChainExplorerConfig.ETHERSCAN)
        total_gas, co2_amount, tx_count = calc.getCarbonFootprintForContractAddress(
            target_address
        )
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps(
            {
                "address": target_address,
                "amount": co2_amount,
                "totalGas": total_gas,
                "txCount": tx_count,
                "known": target_address in KNOWN_ACCOUNTS,
            }
        )


class RedirectResource:
    def on_get(self, req: Request, resp: Response):
        # validate address
        target_address = req.get_param("address")
        if target_address is None:
            # TODO: redirect to regular frontend
            resp.status = falcon.HTTP_400
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "missing param: address"
            return

        # calculate amount of addr
        calc = CarbonCalculator(chainConfig=ChainExplorerConfig.ETHERSCAN)
        total_gas, co2_amount, tx_count = calc.getCarbonFootprintForContractAddress(
            target_address
        )

        # return checkout url
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps(
            {"url": REDIRECT_URL.format(address=target_address, amount=co2_amount)}
        )


app = falcon.App(
    middleware=falcon.CORSMiddleware(allow_origins="*", allow_credentials="*")
)
app.add_route("/success", SuccessCallbackResource())
app.add_route("/failure", FailureCallbackResource())
app.add_route("/estimate", EstimationResource())
app.add_route("/", RedirectResource())

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")

        # Serve until process is killed
        httpd.serve_forever()
