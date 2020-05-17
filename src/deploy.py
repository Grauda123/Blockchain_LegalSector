import json
import hashlib
from web3 import Web3, HTTPProvider
from solcx import compile_source
from eth_keys import keys,datatypes
import random
import time


#config
PRC_ADDRESS = 'https://ropsten.infura.io/v3/2ae82295fc8c4f69815be6623202263b'
CONTRACTWILL_SOL = './solFiles/contractWill.sol'
CONTRACT_NAME = 'contractWill'
#### Metamask address testator
WALLET_ADDRESS = "0xA29139bbE6f6a1e602900Eb75Ff19448959E089e"
WALLET_PRIVATE_KEY="263DBE181C44AD5DBC4E1512C661B59D11CA5A945B9F5622D9FEBC1E4C49B0A9"
#### MEW address
#WALLET_ADDRESS = "0x291A678D5AB168b24B456737EaCca785668e9d2E"
#WALLET_PRIVATE_KEY="1aaa653261e01bd262eb0956797a6d0e1b1724697633ea981d12a39a9ff8f634"

#instantiate web3 object
w3 = Web3(HTTPProvider(PRC_ADDRESS, request_kwargs={'timeout':120}))
acct = w3.eth.account.privateKeyToAccount(WALLET_PRIVATE_KEY)


def compile_contract(contract_source_file, contractName=None):
    """
    Reads file, compiles, returns contract name and interface
    """
    with open(contract_source_file, "r") as f:
        contract_source_code = f.read()
    compiled_sol = compile_source(contract_source_code) # Compiled source code
    if not contractName:
        contractName = list(compiled_sol.keys())[0]
        contract_interface = compiled_sol[contractName]
    else:
        contract_interface = compiled_sol['<stdin>:' + contractName]        
    return contractName, contract_interface

def deploy_contract(acct, contract_interface, contract_args=None):
    """
    deploys contract using self-signed tx, waits for receipt, returns address
    """
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    constructed = contract.constructor() if not contract_args else contract.constructor(*contract_args)
    tx = constructed.buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 3000000, #added this and the gas price to test if transaction can be deployed original dh
        'gasPrice': w3.toWei('40', 'gwei'),
    })
    print('acct.address is {}'.format(acct.address))
    print ("Signing and sending raw tx ...")
    signed = acct.signTransaction(tx)
    #print('signed is {}'.format(signed))
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    print ("tx_hash = {} waiting for receipt ...".format(tx_hash.hex()))
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=120)
    #print('deploy contract tx_receipt is {}'.format(tx_receipt))
    print('')
    contractAddress = tx_receipt["contractAddress"]
    print ("Receipt accepted. gasUsed={gasUsed} contractAddress={contractAddress}".format(**tx_receipt))
    return contractAddress

def send_to_payable(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,amount_in_ether):
    construct_txn = contract.functions.invest().buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce':w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
        'value': w3.toWei(amount_in_ether, 'ether'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn,WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('check is {}'.format(check))

def setBeneficiary(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY, BeneficiaryWalletAddr,name, email, telNum, percentSplit):
    # onlyTestator
    print('Entering setBenefiicary')
    construct_txn = contract.functions.setBeneficiary(BeneficiaryWalletAddr,name,email,telNum,percentSplit).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    #print('After build transaction')
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    #print('after sign transaction')
    #print('signed transaction is {}'.format(signed_txn))
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('setBeneficiary method successful, is {}'.format(check))


def getBeneficiaries(contract,BeneficariesArray):
    print('Entering getBeneficiaries method')
    #print('BeneficiaresArray is {}'.format(BeneficariesArray))
    listofAddress = []
    if('listofAddress') in locals():
        print('listofAddress is in locals')
    elif('listofAddress') in globals():
        print('in globals')
    else:
        print('not defined')
    try:
        listOfAddress = contract.functions.getBeneficiaries().call()
    except Exception as e:
        print(e)
    print('getBeneficiaries called')
    print('value returned from getBeneficiaries is: {}'.format(listOfAddress))
    for i in listOfAddress:
        walletAddr,name,email,telNum,percentSplit,death =contract.functions.getBeneficiary(i).call()
        array = []
        array.append(walletAddr)
        array.append(name)
        array.append(email)
        array.append(telNum)
        array.append(percentSplit)
        array.append(death)
        BeneficariesArray.append(array)
    return BeneficariesArray

def getBeneficiary(contract,BeneficiaryWalletAddr):
    benWalletAddr,name,email,telNum,percentSplit,death = contract.functions.getBeneficiary(BeneficiaryWalletAddr).call()
    return percentSplit

def beneficiaryDeath(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,BeneficiaryWalletAddr):
    #onlyTestator
    construct_txn = contract.functions.beneficaryDeath(BeneficiaryWalletAddr).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('beneficiaryDeath method successful, is {}'.format(check))

def updateBeneficiaryPercent(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,BeneficiaryWalletAddr,percentSplit):
    # onlyTestator
    construct_txn = contract.functions.updateBeneficiaryValue(BeneficiaryWalletAddr,percentSplit).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('updateBeneficiaryPercent method successful, is {}'.format(check))

def setWitness(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,WitnessWalletAddr,name,email):
    # onlyTestator
    construct_txn = contract.functions.setWitness(WitnessWalletAddr,name,email).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('setWitness method successful, is {}'.format(check))

def getWitnesses(contract,witnessesArray):
    listOfAddress = contract.functions.getWitnesses().call()
    #print('value returned from getWitnesses is: {}'.format(listOfAddress))
    for i in listOfAddress:
        walletAddr,name,email,signed =contract.functions.getWitness(i).call()
        array = []
        array.append(walletAddr)
        array.append(name)
        array.append(email)
        array.append(signed)
        witnessesArray.append(array)
    return witnessesArray

def signing(privkey, messageToSign):
    privkey = privkey.lstrip("0x")
    privateKeyinbytes = keys.PrivateKey(bytes.fromhex(str(privkey)))
    MsgEncode = messageToSign.encode()
    signature = privateKeyinbytes.sign_msg(bytes(MsgEncode))
    return signature
def VerifySignature(publicKey, signature, privkey, messageToSign):
    privkey = privkey.lstrip("0x")
    privateKeyinbytes = keys.PrivateKey(bytes.fromhex(str(privkey)))
    publicKey = privateKeyinbytes.public_key
    MsgEncode = messageToSign.encode()
    verifyMessage = signature.verify_msg(MsgEncode, privateKeyinbytes.public_key)
    verifyPubandPriKey = (signature.recover_public_key_from_msg(bytes(MsgEncode)) == privateKeyinbytes.public_key)
    return verifyMessage, verifyPubandPriKey, privKey

def witnessRead(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,percentLeft,WitnessWalletAddr,choice,reason):
    try:
        # onlyWitness
        print("Entering witnessRead")
        construct_txn = contract.functions.witnessRead(percentLeft, WitnessWalletAddr, choice, reason).buildTransaction(
            {
                'from': WALLET_ADDRESS,
                'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
                'gas': 2000000,
                'gasPrice': w3.toWei('30', 'gwei'),
            })
        signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
        #print('signed_txn is {}'.format(signed_txn))
        ##get the r and s values -> 1st 64 bytes of the signature
        #print('r value is {}'.format(signed_txn.r))
        #print('s value is {}'.format(signed_txn.s))
        #print('v value is {}'.format(signed_txn.v))
        # rawTransaction -> RLP encoded signed Transaction
        #print('rawTransaction used to recover the addr is {}'.format(signed_txn.rawTransaction))
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
        check = w3.eth.waitForTransactionReceipt(txn_hash)
        print('witnessRead method successful, is {}'.format(check))
    except Exception as exception:
        print("exception in witnessRead is {}".format(exception))


def verifyIdentity(rawTransaction,WitnessArray):
    # loop through witness array, if acc match witness address, return witness name -> witness name has signed.
    accountUsed = w3.eth.account.recoverTransaction(rawTransaction)
    print("accountUsed is {}".format(accountUsed))
    for x in range(len(WitnessArray)):
        if(accountUsed == WitnessArray[x][0]):
            return WitnessArray[x][1]

def getDisagreeReason(contract,ReasonsArray):
    ReasonsArray = contract.functions.getReason().call()
    return ReasonsArray

def setExecutor(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,ExecutorWalletAddr,name):
    #onlyTestator
    construct_txn = contract.functions.setExecutor(ExecutorWalletAddr,name).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('setExecutor method successful, is {}'.format(check))

def getExecutors(contract,ExecutorsArray):
    print("Entering getExecutors")
    listOfExecutors = contract.functions.getExecutors().call()
    print('value returned from getAssetsList is: {}'.format(listOfExecutors))
    for i in listOfExecutors:
        ExecutorWalletAddr,name,activate = contract.functions.getExecutor(i).call()
        array = []
        array.append(ExecutorWalletAddr)
        array.append(name)
        array.append(activate)
        ExecutorsArray.append(array)
    return ExecutorsArray

def ExecutorActivateContract(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,ExecutorWalletAddr):
    # onlyExecutor
    print("Entering ExecutorActivateContract")
    construct_txn = contract.functions.activateContract(ExecutorWalletAddr).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('ExecutorActivateContract method successful, is {}'.format(check))

def distributeEther(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,BeneficiaryWalletAddr,amountToReceive):
    # onlyTestator
    print('\nAmount to be sent is {}'.format(amountToReceive))
    construct_txn = contract.functions.send(BeneficiaryWalletAddr,amountToReceive).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('distributeEther method successful, is {}'.format(check))

def setAsset(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,AssetName,AssetValue):
    construct_txn = contract.functions.setAsset(AssetName,AssetValue).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('distributeEther method successful, is {}'.format(check))
def getAssets(contract,AssetsArray):
    listOfAssets = contract.functions.getAssetsList().call()
    print('value returned from getAssetsList is: {}'.format(listOfAssets))
    for i in listOfAssets:
        assetName, assetValue = contract.functions.getAsset(i).call()
        array = []
        array.append(assetName)
        array.append(assetValue)
        AssetsArray.append(array)
    return AssetsArray
### old writeJson function, incorrect json format
# def writeJsonWill(BeneficariesArray,WitnessArray,ExecutorsArray):
#     # "w" to write, "a" to append
#     with open("jsonFiles/will.json", "w") as write_file:
#         json.dump("Beneficiary:", write_file)
#         write_file.write('\n')
#         for x in BeneficariesArray:
#             print(x)
#             json.dump(x, write_file, indent=2)
#             write_file.write('\n')
#         json.dump("Executors:", write_file)
#         write_file.write('\n')
#
#         for x in ExecutorsArray:
#             print(x)
#             json.dump(x, write_file, indent=2)
#             write_file.write('\n')
#
#         json.dump("Witness:",write_file)
#         write_file.write('\n')
#         for x in WitnessArray:
#             print(x)
#             json.dump(x,write_file, indent=2)
#             write_file.write('\n')
#
#         json.dump("Signatures:", write_file)
#         write_file.write('\n')
#         #signatures should be in dictionary as key value pairs
###
def writeJsonWill(BeneficariesArray,WitnessArray,ExecutorsArray):
    peopleArray=[]

    BeneficiaryValuesDict = {}
    BeneficiaryDict = {}
    BeneficiaryMainDict = {}

    for i in range(len(BeneficariesArray)):
        BeneficiaryValuesDict["walletAddr"] = BeneficariesArray[i][0]
        BeneficiaryValuesDict["name"] = BeneficariesArray[i][1]
        print(BeneficiaryValuesDict["name"])
        name = BeneficariesArray[i][1]
        BeneficiaryValuesDict["email"] = BeneficariesArray[i][2]
        BeneficiaryValuesDict["telNum"] = BeneficariesArray[i][3]
        BeneficiaryValuesDict["percentSplit"] = BeneficariesArray[i][4]
        BeneficiaryDict[name] = BeneficiaryValuesDict
    #print(BeneficiaryValuesDict)
    #print("BeneficiaryDict is ", BeneficiaryDict)
    BeneficiaryMainDict["Beneficiary"]=BeneficiaryDict
    print(BeneficiaryMainDict)
    peopleArray.append(BeneficiaryMainDict)


    WitnessValuesDict = {}
    WitnessDict = {}
    WitnessMainDict = {}
    for i in range(len(WitnessArray)):
        WitnessValuesDict["walletAddr"] = WitnessArray[i][0]
        WitnessValuesDict["name"] = WitnessArray[i][1]
        name = WitnessArray[i][1]
        print(name)
        WitnessValuesDict["email"] = WitnessArray[i][2]
        WitnessValuesDict["signed"] = WitnessArray[i][3]
        WitnessDict[name] = WitnessValuesDict
    #print(WitnessValuesDict)
    #print("WitnessDict is ", WitnessDict)
    WitnessMainDict["Witness"]=WitnessDict
    print(WitnessMainDict)
    peopleArray.append(WitnessMainDict)

    ExecutorValuesDict = {}
    ExecutorDict = {}
    ExecutorMainDict = {}
    for i in range(len(ExecutorsArray)):
        ExecutorValuesDict["walletAddr"] = ExecutorsArray[i][0]
        ExecutorValuesDict["name"] = ExecutorsArray[i][1]
        name = ExecutorsArray[i][1]
        print(name)
        ExecutorValuesDict["activated"] = ExecutorsArray[i][2]

        ExecutorDict[name] = ExecutorValuesDict
    #print(ExecutorValuesDict)
    #print("ExecutorsArray is ", ExecutorDict)
    ExecutorMainDict["Executor"]=ExecutorDict
    print(ExecutorMainDict)
    peopleArray.append(ExecutorMainDict)

    with open("jsonFiles/will.json", "w") as write_file:
        json.dump(peopleArray, write_file)

def addSigtoWill(name,signature):
    peopleArray=[]
    signatureDictCheck=None
    with open("jsonFiles/will.json", "r") as f:
        peopleArray=json.load(f)
    #print("peopleArray is",peopleArray)
    #chec if signature dictionary exists
    for people in peopleArray:
        #print("people is ",people)
        for mainKey in people:
            #print("mainKey is",mainKey)
            #print(type(mainKey))
            if "Signature" in mainKey:
                #print("Signature present in mainkey")
                signatureDictCheck=True
                #print()
            else:
                signatureDictCheck=False
    if signatureDictCheck==True:
        # append to signature
        print('signature is alr present')
        signDict = {}
        signDict[name] = signature
        #print("signDict is ",signDict)
        peopleArray[3]["Signature"].update(signDict)
        #print("peopleArray after updating is ",peopleArray)
        with open("jsonFiles/will.json", "w") as write_file:
            json.dump(peopleArray, write_file)
    else:
        # signature dict not inside
        print("signature dict not inside")
        signatureDict = {}
        signatureMainDict = {}
        signatureDict[name] = signature
        signatureMainDict["Signature"] = signatureDict
        peopleArray.append(signatureMainDict)
        print("peopleArray after updating is ",peopleArray)
        with open("jsonFiles/will.json", "w") as write_file:
            json.dump(peopleArray, write_file)



def signing(privkey, messageToSign):
    privkey = privkey.lstrip("0x")
    privateKeyinbytes = keys.PrivateKey(bytes.fromhex(str(privkey)))
    MsgEncode = messageToSign.encode()
    signature = privateKeyinbytes.sign_msg(bytes(MsgEncode))
    return signature

def VerifySignature( signature, privkey, messageToSign):
    #print('Entering verify signature')
    signature = signature.lstrip("0x")
    privkey = privkey.lstrip("0x")
    #print('signature after stripping is ', signature)
    privateKeyinbytes = keys.PrivateKey(bytes.fromhex(str(privkey)))
    MsgEncode = messageToSign.encode()
    Sig=datatypes.Signature(bytes.fromhex(str(signature)))
    #print("Sig is",type(Sig))
    verifyMessage = Sig.verify_msg(MsgEncode, privateKeyinbytes.public_key)
    #print('exiting VerifySignature')
    return verifyMessage
def sendHash(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,hash):
    # onlyTestator
    construct_txn = contract.functions.sendHash(hash).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    #print('sendHash method successful, is {}'.format(check))
    print("sendHash method successful")

def getHash(contract):
    willHashArray = contract.functions.getHash().call()
    print('Hash of jsonWill is {}'.format(willHashArray))
    return willHashArray

def calculateHash():
    sha256_hash = hashlib.sha256()
    with open("jsonFiles/will.json", "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        contractFileHash = sha256_hash.hexdigest()
    return contractFileHash

def terminateContract(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,testatorWalletAddr):
    # onlyTestator
    construct_txn = contract.functions.terminate(testatorWalletAddr).buildTransaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS),
        'gas': 2000000,
        'gasPrice': w3.toWei('30', 'gwei'),
    })
    signed_txn = w3.eth.account.signTransaction(construct_txn, WALLET_PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
    check = w3.eth.waitForTransactionReceipt(txn_hash)
    print('terminateContract method successful, is {}'.format(check))

###    Calling the functions

# ####compiling contract to get abi
# contract_name, contract_interface = compile_contract(CONTRACTWILL_SOL,CONTRACT_NAME)
# ####deploying contract
# contract,contract_address = deploy_contract(acct, contract_interface)
# print('contract address = {}'.format(contract_address))

##create contract object
#contract = w3.eth.contract(address=contract_address, abi=contract_interface['abi']);

# all_functions = contract.all_functions()
# print('all functions in contract is {}'.format(all_functions))
# print('')

# setBeneficiary(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,"0x291A678D5AB168b24B456737EaCca785668e9d2E","beneficiary1","beneficiary1@yahoo.com",87253546,60)
# setBeneficiary(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,w3.toChecksumAddress("0x9dce01d0c46664840c2a4bfcab891da7ef0c7a08"),"beneficiary2","josh@yahoo.com",81234586,40)
#
# BeneficariesArray = []
# BeneficariesArray = getBeneficiaries(contract,BeneficariesArray)
# print("BeneficiariesArray is {}".format(BeneficariesArray))
# numOfBeneficiaries = len(BeneficariesArray)
#
# setWitness(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,w3.toChecksumAddress("0xa0b9bd956781f6d809c9b512168e814a986cc7d2"),"witness1","witness1@yahoo.com")
# #setWitness(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,w3.toChecksumAddress("0x97822b15f3990573db7445405a06c132566d07e1"),"witness2","witness2@yahoo.com")
# WitnessArray = []
# WitnessArray = getWitnesses(contract,WitnessArray)
# print("witnessArray is {}".format(WitnessArray))
#
# setExecutor(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,w3.toChecksumAddress("0x9a08ee39abc294804db5cc8058a049e219696566"),"executor1")
# setExecutor(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,w3.toChecksumAddress("0x99d8d926d5e1302640bbeb0868923a1938c8fd5e"),"executor2")
# ExecutorsArray= []
# ExecutorsArray = getExecutors(contract,ExecutorsArray)
# print("ExecutorsArray is {}".format(ExecutorsArray))
# ### beneficiary dies
# counter=0
# beneficiaryDeath(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,w3.toChecksumAddress("0x9dce01d0c46664840c2a4bfcab891da7ef0c7a08"))
# counter = counter +1
# beneficiaryDead = counter
# beneficiariesLeft = numOfBeneficiaries - beneficiaryDead
# percentSplit=0
# percentSplit += getBeneficiary(contract,"0x9dce01d0c46664840c2a4bfcab891da7ef0c7a08")
# percentToReceive = percentSplit/beneficiariesLeft
# for i in range(len(BeneficariesArray)):
#         print(BeneficariesArray[i])
#         if(BeneficariesArray[i][5]== "false"):
#             newPercentSplit = BeneficariesArray[i][4] + percentSplit
#             BeneficiaryWalletAddr = BeneficariesArray[i][0]
#             updateBeneficiaryPercent(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,BeneficiaryWalletAddr,newPercentSplit)
# BeneficariesArray = []
# BeneficariesArray = getBeneficiaries(contract,BeneficariesArray)
# print("BeneficiariesArray is {}".format(BeneficariesArray))
###witness sign
#getWitness, getBeneficiary, getExecutor and source code of the solidity file add to a json file
# with open("jsonFiles/will.json","a") as write_file:
#     json.dump("Witness:",write_file)
#     write_file.write('\n')
#     for x in WitnessArray:
#         print(x)
#         json.dump(x,write_file, indent=2)
#         write_file.write('\n')
#all witness hv to sign
# rawTransaction1 = witnessRead(contract,w3.toChecksumAddress("0xa0b9bd956781f6d809c9b512168e814a986cc7d2"),"0x6d60ce60a7748fb068da6b5edc7327d19a2c42b8e06bf20afeb0d99b4ed8e5cb",0,w3.toChecksumAddress("0xa0b9bd956781f6d809c9b512168e814a986cc7d2"),True,"")
#rawTransaction2 = witnessRead(contract,w3.toChecksumAddress("0x97822b15f3990573db7445405a06c132566d07e1"),"0x7b02c27e9c1afe2a39ae600cade8fb807314124a7411aa866c31138301dd5447",0,w3.toChecksumAddress("0x97822b15f3990573db7445405a06c132566d07e1"),False,"Beneficiary too little")
#
# with open("jsonFiles/will.json","a") as write_file:
#     json.dump("Verification:",write_file)
#     write_file.write('\n')
#     json.dump(w3.toJSON(rawTransaction1),write_file)

# name = verifyIdentity(rawTransaction1,WitnessArray)
# print('name is {}'.format(name))
# if(name == None):
#     print('Signature is not valid')
# else:
#     print('Signature belongs to {}'.format(name))

####check if all witness has signed -> pass the array to html and check the looping in html

# #### testator dies
# # executor activates
# ExecutorActivateContract(contract,w3.toChecksumAddress("0x9a08ee39abc294804db5cc8058a049e219696566"),"0x427297a347d033ef1ed81ab9042a6a34801efbdd6c5566b198e25fde032a8a23",w3.toChecksumAddress("0x9a08ee39abc294804db5cc8058a049e219696566"))
# #loop through and see if there is at least 1 activate=true, if present, send ether
#

###### send hash after testator signed
# BeneficiariesArray = [["0x291A678D5AB168b24B456737EaCca785668e9d2E", "ThisisMEWAddressWallet@yahoo.com", 87875647, 30], ["0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E", "Testing@gmail.com", 81234565, 60]]
# ExecutorsArray = [["0x9a08ee39abc294804db5cc8058a049e219696566","executor1",False],["0x99d8d926d5e1302640bbeb0868923a1938c8fd5e","executor2",False]]
# WitnessArray = [['0xA0B9Bd956781f6d809C9B512168e814a986Cc7d2', 'witness1', 'witness1@yahoo.com', False], ['0x97822B15f3990573dB7445405A06C132566d07E1', 'witness2', 'witness2@yahoo.com', False]]
# writeJsonWill(BeneficiariesArray,WitnessArray,ExecutorsArray)
# contractFileHash = calculateHash()
# print('contractFileHash from calculateHash function is {}'.format(contractFileHash))
# sendHash(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,contractFileHash)
# willHash = getHash(contract)
# #print('willHash is {}'.format(willHash))
# if(contractFileHash == willHash):
#     print('Hashes are the same, valid contract')
# else:
#     print('Hashes does not match, contract might have been modified')




# amount_in_ether = 0.05
# send_to_payable(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY, amount_in_ether)
#
# wei_amount = w3.eth.getBalance(contract_address)
# eth_amount = w3.fromWei(wei_amount,'ether')
# print('Current contract value is {}'.format(eth_amount))
#
# BeneficiaryWalletAddr = "0x291A678D5AB168b24B456737EaCca785668e9d2E"
# email="ThisisMEWAddressWallet@yahoo.com"
# telNum=87875647
# percentSplit=30
# setBeneficiary(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,BeneficiaryWalletAddr,email,telNum,percentSplit)
#
# ###check for remaining percentage left after setting benefiicaries
# BeneficiariesArray = []
# BeneficiariesArray=getBeneficiaries(contract,BeneficiariesArray)
# print('\nBeneficiariesArray is {}'.format(BeneficiariesArray))
# remainingPercent=100
# for i in range(len(BeneficiariesArray)):
#         percent = BeneficiariesArray[i][3]
#         print(percent)
#         remainingPercent -= percent
# print('remaining percentage is {}'.format(remainingPercent))


# totalAsset = eth_amount
# print('totalAsset is {}'.format(totalAsset))
# for i in range(len(BeneficiariesArray)):
#         BenAddr = BeneficiariesArray[i][0]
#         percent = BeneficiariesArray[i][3]
#         amountToReceive = (percent*totalAsset)/100
#         print(BenAddr, percent,amountToReceive)
#         amountToReceive = w3.toWei(amountToReceive, 'ether')
#         print('passing {} to distributeEther function'.format(amountToReceive))
#         distributeEther(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,BenAddr,amountToReceive)
