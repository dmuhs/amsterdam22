import requests


class CarbonCalculator:
    G_CO2_PER_GAS = 0.1809589427
    ENDPOINT = "https://{baseUri}/api?module=account&action=txlist&address={address}&startblock={startblock}&endblock={endblock}&page={page}&offset={offset}&sort={sort}&apikey={apikey}"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",  # happy cloudflare
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
            logger.info("data provider error")
            return 0, 0, 0

        if not data["result"]:
            logger.info("addr doesn't seem to have txs")
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
