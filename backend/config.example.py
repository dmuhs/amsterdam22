PATCH_API_KEY = "key_test_"
BASE_URL = "https://api.patch.io"
NFT_ADDR = "0x"
PUBLIC_KEY = "0x"
PRIVATE_KEY = "0x"
ABI = ""
INFURA_URL = "https://"
REDIRECT_URL = "https://checkout.patch.io/che_test_"
FRONTEND_SUCCESS_URL = None  # auto-redirects to certificate if None
FRONTEND_URL = "http://"
FALLBACK_URL = "https://google.com"  # TODO: replace with frontend url


class ChainExplorerConfig:
    ETHERSCAN = {
        "apiKey": "",
        "baseUri": "api.etherscan.io",
    }
    POLYGONSCAN = {
        "apiKey": "",
        "baseUri": "api.polygonscan.com",
    }
    OPTIMISM = {
        "apiKey": "",
        "baseUri": "api-optimistic.etherscan.io",
    }
