pragma solidity ^0.4.25;
import "./Ownable.sol";

contract Testament is Ownable{
    
    struct Document{
        // store document on ipfs. the IPFS store doc and return a hash address to get file from the network
        // for the secure reason, we must encrypt the IPFS address, reccomend use hashvalue of document to encrypt
        string ipfsAddress;
        
        //hash value 
        string hashValue;
    }
    
    // Map document creator to document
    mapping(address=>Document) documents;
    // list of creators
    address[] creators;

/* constructor */

    constructor() public{
        //contractOwner = msg.sender;
    }

/* functions */

    // Create DieWill
    function createDocument (string memory _ipfsAddress, string memory _hashValue) public payable{
        require(msg.value >= 1);
        address sender = msg.sender;
        Document memory doc;
        doc.ipfsAddress = _ipfsAddress;
        doc.hashValue = _hashValue;
        documents[sender] = doc;
        
        // push to creators array
        creators.push(sender);
        
        //address(this).balance += msg.value;
        uint value = msg.value;
        owner().transfer(value);
    }
    
    // get diewill 
    function getDocument(address _creatorAddress) public view returns (string memory ipfsAddress, string memory hashValue){
        //check if sender ar creator document
        uint arrlen = creators.length;
        int counter =0;
        for(uint16 i=0; i<arrlen; i++){
            if(_creatorAddress == creators[i])
                counter++;
        }
        
        require (counter != 0);
        Document memory doc = documents[_creatorAddress];
        return (doc.ipfsAddress, doc.hashValue);
    }
    
}