pragma solidity ^0.6.2;
pragma experimental ABIEncoderV2;

contract contractWill{
    
    address payable executor;
    address payable testator;
    mapping (address => uint) sentEther; //tracks how much ether is sent to each address.
    
    struct Beneficiary{
        address payable walletAddr;
        string name;
        string email;
        uint256 telNum;
        uint256 percentSplit;
        bool death;
    }
    mapping(address =>Beneficiary) beneficiaries;
    address[] public BeneficiaryAccts;
    
    struct Witness{
        address payable walletAddr;
        string name;
        string email;
        bool signed; //record if that witness have signed
    }
    mapping(address => Witness) witnesses;
    address[] public witnessAccts;
    string [] public reasonArray;
    
    struct Executor{
        address payable walletAddr;
        string name;
        bool activate;
    }
    mapping(address => Executor) executors;
    address [] public executorAccts;
    
    uint256 totalAsset;
    struct Asset{
        string name;
        uint256 value;
    }
    mapping(string => Asset) assets;
    string [] public assetArray;
    
    string[] public hashArray;
    
    constructor() public{
        testator = msg.sender;
    }
    
    modifier onlyExecutor(){
    //only after executor approves then contract executes 
        require(executors[msg.sender].walletAddr == msg.sender);
         _;
    }
    
    modifier onlyTestator(){
    require(msg.sender == testator);
    _;
    }
    
    modifier onlyWitness(){
        require(witnesses[msg.sender].walletAddr == msg.sender);
         _;
    }

    function storeETH(uint256 totalAmt) payable public { 
        //This function to allow smart contract to store eth
        require(msg.value == totalAmt);
    }
    
    function invest() external payable{
        //this function is to send ether to the contract
    }
    
    function getBalance() public view returns(uint256){
        //gets contract balance
        address self = address(this);
        uint256 balance = self.balance;
        return balance;
    }
    
    function send(address payable _addr,uint256 amount) public onlyTestator {
        require(amount>0);
       //transfer amount to _addr
	    _addr.transfer(amount); //in wei
        //_addr.transfer(amount * 1 ether);
        sentEther[_addr] += amount; //add a function to loop thr this mapping to see.
    }
    
    function setBeneficiary(
        address payable  _walletAddr,  
        string memory _name,
        string memory _email, 
        uint256 _telNum, 
        uint256  _percentSplit
        ) public onlyTestator{
        Beneficiary storage beneficiary = beneficiaries[_walletAddr];
        // note: _addr is the key to access these values below
        beneficiary.walletAddr = _walletAddr;
        beneficiary.name = _name;
        beneficiary.email = _email;
        beneficiary.telNum = _telNum;
        beneficiary.percentSplit=_percentSplit;
        beneficiary.death = false;
        
        BeneficiaryAccts.push(_walletAddr);
    }
     function getBeneficiaries() view public returns( address[] memory){
        return BeneficiaryAccts;
    }
    function getBeneficiary(address ins) view public returns(address payable, string memory , string memory , uint256 , uint256, bool ){
        return (beneficiaries[ins].walletAddr,beneficiaries[ins].name, beneficiaries[ins].email, beneficiaries[ins].telNum, beneficiaries[ins].percentSplit,beneficiaries[ins].death);
    }
    function beneficiaryDeath(address ins)public onlyTestator{
        beneficiaries[ins].death = true;
    }
    function updateBenefiaryValue(address ins, uint256 _percentSplit)public onlyTestator{
        beneficiaries[ins].percentSplit = _percentSplit;
    }
    
    function setWitness(
        address payable _walletAddr,
        string memory _name,
        string memory _email
        ) public onlyTestator{
        Witness storage witness = witnesses[_walletAddr];
        witness.walletAddr = _walletAddr;
        witness.name = _name;
        witness.email = _email;
        witness.signed = false;
        
        witnessAccts.push(_walletAddr);
    }
    function getWitnesses() view public returns(address[] memory){
        return witnessAccts;
    }
    function getWitness(address ins) view public returns(
        address payable, 
        string memory, 
        string memory,
        bool){
            return (witnesses[ins].walletAddr, witnesses[ins].name,witnesses[ins].email,witnesses[ins].signed);
    }
    function witnessRead(uint256 percentLeft,address ins, bool choice, string memory reason) public onlyWitness returns(bool){
        require(percentLeft==0);
        if(choice==true){
            //witness agree with contract
            witnesses[ins].signed = true;
            return(true);
        }else{
            //witness disagre
            setReason(reason);
            return(false);
        }
    }
    
    function setReason(string memory reason) public onlyWitness {
        reasonArray.push(reason);
    }
    function getReason() view public returns(string[] memory){
        return reasonArray;
    }
    
    function setExecutor(
        address payable _walletAddr,
        string memory _name
        )public onlyTestator{
            Executor storage executor = executors[_walletAddr];
            executor.walletAddr = _walletAddr;
            executor.name = _name;
            executor.activate = false;
            executorAccts.push(_walletAddr);
        }
    function getExecutors() view public returns (address [] memory){
        return executorAccts;
    }
    function getExecutor(address ins) view public returns(address payable, string memory,bool){
        return(executors[ins].walletAddr, executors[ins].name, executors[ins].activate);
    }
    function activateContract(address ins) public onlyExecutor{
        executors[ins].activate = true;
    }
    
    function setAsset(string memory _name, uint256 _value)public onlyTestator{
       Asset storage asset = assets[_name];
       asset.name = _name;
       asset.value = _value;
       assetArray.push(_name);
    }
    function getAssetsList() view public returns(string[] memory){
        return assetArray;
    }
    function getAsset(string memory _name) view public returns(string memory, uint256){
        return (assets[_name].name,assets[_name].value);
    }
    function updateAsset(string memory _name, uint256 _value) public onlyTestator{
        assets[_name].value = _value;
    }
    
    function getSentEther(address addr) view public returns(uint256 sentValue){
        return sentEther[addr];
    }
    
    function sendHash(string memory x) public {
        hashArray.push(x);
    }

    function getHash() public view returns (string[] memory ) {
         return hashArray;
     }
    
   function terminate(address payable addr)public onlyTestator{
       selfdestruct(addr);
   }
   
}