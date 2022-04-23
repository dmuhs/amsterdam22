from falcon import Request, Response
import falcon
from web3 import Web3
import json
import patch_api
from carboncalc import CarbonCalculator
import config


KNOWN_ACCOUNTS = []


class SuccessCallbackResource:
    def on_get(self, req: Request, resp: Response):
        # TODO: Whitelist origin 80.113.211.254

        client = patch_api.ApiClient(api_key=config.PATCH_API_KEY)

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
        w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))
        nonce = w3.eth.get_transaction_count(config.PUBLIC_KEY)
        contract_instance = w3.eth.contract(address=config.NFT_ADDR, abi=config.ABI)
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
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=config.PRIVATE_KEY)
        w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        KNOWN_ACCOUNTS.append(target_addr)

        # redirect back to frontend
        print(f"Redirecting")
        registry_url = order.registry_url
        raise falcon.HTTPPermanentRedirect(
            location=config.FRONTEND_SUCCESS_URL or registry_url or config.FALLBACK_URL
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

        calc = CarbonCalculator(chainConfig=config.ChainExplorerConfig.ETHERSCAN)
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
        calc = CarbonCalculator(chainConfig=config.ChainExplorerConfig.ETHERSCAN)
        total_gas, co2_amount, tx_count = calc.getCarbonFootprintForContractAddress(
            target_address
        )

        # return checkout url
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps(
            {
                "url": config.REDIRECT_URL.format(
                    address=target_address, amount=co2_amount
                )
            }
        )
