import requests
import time



class CarbonCalculator(object):
    
    KG_CO2_PER_GAS = 0.0001809589427
    ENDPOINT = "https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={startblock}&endblock={endblock}&page={page}&offset={offset}&sort={sort}&apikey={apikey}"

    def __init__(self, apiKey) -> None:
        self.apiKey = apiKey
        self.session = requests.Session()
        
    def getTotalGasFromAllContractTransactions(self, address, txFilter):
        totalGasUsed = 0
        results = 0
        for page in range(1, 10):
            url = self.ENDPOINT.format(
                address=address,
                startblock=0,
                endblock='latest',
                page=page,
                offset=10000,
                sort="desc",
                apikey=self.apiKey
            )
            #print(url)
            resp = requests.get(url)
            data = resp.json()
            if data["status"] != "1" or data["message"] != "OK":
                #raise Exception("Bad things happened", data)
                return totalGasUsed
            if data["result"] == []:
                return totalGasUsed 
            results += len(data["result"])
            print(f"result now at {results}")
            for tx in data["result"]:
                if txFilter and not txFilter(tx):
                    continue
                totalGasUsed += int(tx["gasUsed"])


    """
    returns KG CO2 Contract Gas Footprint
    """
    def getCarbonFootprintForContractAddress(self, address, txFilter=None): 
        return self.getTotalGasFromAllContractTransactions(address, txFilter) * self.KG_CO2_PER_GAS


def test():
    cc = CarbonCalculator("RVXR4IXM4K7TKUI2H7XQBGHZDDBP393KFP")
    print(cc.getCarbonFootprintForContractAddress("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", lambda tx: int(tx["timeStamp"])>=int(time.time()) - 60*60*24 )) # carbon footprint for all TX

if __name__ == "__main__":
    test()
