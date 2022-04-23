import requests
import sys


API_KEY = "RVXR4IXM4K7TKUI2H7XQBGHZDDBP393KFP"
ENDPOINT = "https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={startblock}&endblock={endblock}&page={page}&offset={offset}&sort={sort}&apikey={apikey}"

results = 0

for page in range(1, 10):
    resp = requests.get(
        ENDPOINT.format(
            address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            startblock=0,
            endblock=999999999,
            page=page,
            offset=10000,
            sort="asc",
            apikey=API_KEY,
        )
    )

    data = resp.json()
    if data["status"] != "1" or data["message"] != "OK":
        print("Bad things happened")
        print(data)
        sys.exit()
    if data["result"] == []:
        print("Done")
        sys.exit()
    results += len(data["result"])
    print(f"result now at {results}")
