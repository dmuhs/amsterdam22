import requests
import time


class ChainExplorerConfig:
    ETHERSCAN = {"apiKey": "RVXR4IXM4K7TKUI2H7XQBGHZDDBP393KFP", "baseUri": "api.etherscan.io"} # dom
    POLYGONSCAN = {"apiKey": "V99R51EYZRATHEK6QK3T3ACPXHFCBMFCWF", "baseUri": "api.polygonscan.com"} # rmfblqsrfthfxssbrk - password: rmfblqsrfthfxssbrk@bvhrk.com (throwaway)
    OPTIMISM = {"apiKey": "7WTXX7U4PUUBJ9SRNT62C2X1S7A8R3UWHT", "baseUri":"api-optimistic.etherscan.io"} # jeujuzawxslhxxsjce@nthrw.com user and pass


class CarbonCalculator:

    G_CO2_PER_GAS = 0.1809589427
    ENDPOINT = "https://{baseUri}/api?module=account&action=txlist&address={address}&startblock={startblock}&endblock={endblock}&page={page}&offset={offset}&sort={sort}&apikey={apikey}"
    HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36', # happy cloudflare
    }


    def __init__(self, chainConfig) -> None:
        self.api_key = chainConfig["apiKey"]
        self.baseUri = chainConfig["baseUri"]

    def getTotalGasFromAllContractTransactions(self, address, txFilter):
        url = self.ENDPOINT.format(
            baseUri=self.baseUri,
            address=address,
            startblock=0,
            endblock="latest",
            page=1,
            offset=10000,
            sort="desc",
            apikey=self.api_key,
        )

        resp = requests.get(url, headers=self.HEADERS)
        data = resp.json()
        if data.get("status") != "1" or data.get("message") != "OK":
            print("some shit happened")
            return 0, 0, 0

        if not data["result"]:
            print("addr doesn't seem to have txs")
            return 0, 0, 0

        total_gas = 0
        tx_count = 0
        for tx in data["result"]:
            if txFilter and not txFilter(tx):
                continue
            tx_count += 1
            total_gas += int(tx["gasUsed"])

        return total_gas, tx_count

    def getCarbonFootprintForContractAddress(self, address, txFilter=None):
        total_gas, tx_count = self.getTotalGasFromAllContractTransactions(
            address, txFilter
        )
        return total_gas, max(1_000_000, int(total_gas * self.G_CO2_PER_GAS)), tx_count


if __name__ == "__main__":
    cc = CarbonCalculator(ChainExplorerConfig.ETHERSCAN)
    print(
        cc.getCarbonFootprintForContractAddress(
            "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            lambda tx: int(tx["timeStamp"]) >= int(time.time()) - 60 * 60 * 24,
        )
    )  # carbon footprint for all TX in g
