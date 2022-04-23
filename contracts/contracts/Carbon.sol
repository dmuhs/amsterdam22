// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "./Base64.sol";

contract Carbon is ERC721, Ownable {
    using Counters for Counters.Counter;
    using Strings for uint256;

    Counters.Counter private _tokenIdCounter;
    mapping(uint256 => uint256) carbonCompensated;

    constructor() ERC721("Carbon", "CRB") {}

    function safeMint(address to, uint256 carbonAmount) public onlyOwner {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        carbonCompensated[tokenId] = carbonAmount;
        _safeMint(to, tokenId);
    }

    function tokenAmount() public view returns (uint256) {
        return _tokenIdCounter.current();
    }

    function formatSvg(uint256 tokenId) private view returns (string memory) {
        string
            memory head = '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" xml:space="preserve"><path fill="#14fa09" transform="translate(200 200)" d="M-200-200H200V200H-200z"/><svg viewBox="-13 -12 40 40" xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.4"><path d="M8 12 3 9l5 7 4.9-7-5 3zM8 0 3.1 8.1l5 3 4.8-3L8 0z" fill="#010101"/></svg><text font-family="Alegreya" font-size="30" font-weight="600" transform="translate(200 48.8)"><tspan x="-136.2" y="9.4">YOU COMPENSATED</tspan></text><text font-family="Alegreya" font-size="30" font-weight="500" transform="translate(200 354)"><tspan x="-80" y="10.4">';
        string memory tail = " T Co2 !</tspan></text></svg>";
        string memory carbon = carbonCompensated[tokenId].toString();
        return string(abi.encodePacked(head, carbon, tail));
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override
        returns (string memory)
    {
        require(
            _exists(tokenId),
            "ERC721Metadata: URI query for nonexistent token"
        );
        string memory imageURI = svgToImageURI(formatSvg(tokenId));
        string memory _tokenURI = formatTokenURI(imageURI);
        return _tokenURI;
    }

    function svgToImageURI(string memory svg)
        public
        pure
        returns (string memory)
    {
        string memory baseURL = "data:image/svg+xml;base64,";
        string memory svgBase64Encoded = Base64.encode(
            bytes(string(abi.encodePacked(svg)))
        );
        return string(abi.encodePacked(baseURL, svgBase64Encoded));
    }

    function formatTokenURI(string memory imageURI)
        public
        pure
        returns (string memory)
    {
        string memory baseURL = "data:application/json;base64,";
        return
            string(
                abi.encodePacked(
                    baseURL,
                    Base64.encode(
                        bytes(
                            abi.encodePacked(
                                '{"name": "Carbon NFT", ',
                                '"description": "Thank you for the planet !", ',
                                '"attributes":"", ',
                                '"image": "',
                                imageURI,
                                '"}'
                            )
                        )
                    )
                )
            );
    }
}
