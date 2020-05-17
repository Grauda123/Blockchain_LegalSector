# Blockchain in legal/estate planning fraternity

This project aims at building capabilities in blockchain by exploring and prototyping some compelling use cases, e.g. in the legal/estate planning fraternity, with crypto-wills and smart contract.
There are 4 actors in the crypto-will, namely Testator, Witness, Executor and Beneficiary

### Prerequisites

Install Google chrome
*https://www.google.com/chrome/*

Install Python version 3.6.4
1.	Download Python (Windows x86-64 web-based installer)
from *https://www.python.org/downloads/release/python-364/*
2.	Run the exe file and check ‘add Python 3.6 to PATH’ in the installer prompt
3.	Select ‘Install Now’

Install Pycharm version 2019 community
1.	Download Pycharm from *https://www.jetbrains.com/pycharm/download/#section=windows*
2.	Run the exe file and select install

Install Virtual Environment for Pycharm
1.	Copy the folder ‘flask_todo’ to desktop and open it (the project) with pycharm
2.	Add python interpreter in Pycharm ( File>Settings>Project:flask_todo>Project Interpreter>  > Add Python interpreter > Virtualenv Environment > New environment>Apply)
3.  A venv directory would be created
4.  Activate the virtual environment using 
```
.\venv\Scripts\activate
```

Install Visual Studio Build Tools
1.	Download and install Visual Studio build tools (Build Tools for Visual Studio 2019) from
*https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017*
2.  After downloading, in the Visual Studio Installer prompt, click on the modify button and download “C++ build tools”

Creating a Solidity Smart Contract
1.	To create or edit a Solidity smart contract, go to the following URL:
* *https://remix.ethereum.org/*
* Note: the smart contract is tied to the browser/machine.
2.	The smart contract in the Crypto-Will Application is in the following file:
*	~\flask_todo\codes\solFiles\contractWill.sol
3.	A smart contract has to be deployed in a blockchain network to capture contract interactions (transactions on the blockchain).
4.	In this project, we will use the Crypto-Will application to deploy the smart contract to the ropsten blockchain network. 

EtherScan
1.	To view all transactions in the blockchain network,
*	 Go to *https://ropsten.etherscan.io/*
*	Note:  Check that etherscan is on the ropsten network
*	Copy and paste the Contract address created from the Crypto-Will Application home page to the search bar of the ropsten etherscan website.

Metamask, MyEtherWallet chrome extension
1.	Metamask and MyEtherWallet are used as our multi-platform Ether wallets. To use them, we need to add their chrome extensions to the chrome browser in the host machine. 
Note: Adding chrome extension inside the VM might not work.
2.	Download and add the Metamask chrome extension for testator from the following URL: *https://metamask.io/*
3.	Download and add the MyEtherWallet chrome extension for the Beneficiaries, witnesses and executors from the following URL: 
*https://www.myetherwallet.com/*
4.	Use the chrome extension for the following: 
*	To add the Beneficiaries, witnesses and executors wallets to the extension.
*	To change the network of all wallets to Ropsten Test Network.

Get personal information from MyInfo API
1.	The personal information of the users will be retrieved from MyInfo website.
2.	Go to *https://www.ndi-api.gov.sg/library/trusted-data/myinfo/resources-personas*
3.	Click on ‘Test Profiles Download’ to download the personal information.

Install Google Authenticator mobile app
1.	Google Authenticator mobile app is used to authenticate the user using OTP.
2.	Go to play store or app store
3.	Search for Google Authenticator
4.	Download the app in your phone and open the app
5.	Press the add button in the app and select ‘Scan a barcode’
6.	Go to *https://pyotp.readthedocs.io/en/latest/*
7.	Scan the barcode in the website

## Running the tests
Run the Crypto-Will Application with
```
python app.py
```
In this project, app.py and deploy.py are the 2 main python files.
*	deploy.py file contains python functions to interface with solidity methods.
*	app.py file contains Flask app routing (to associate URL to python function)

The first page will be displayed in *127.0.0.5000/*

The sequence of action is

* Log in with NRIC
* Retrieve and Verify myInfo details
* Enter OTP

**Testator**
* Add asset (Name, Value in SGD which will be converted to ether)
* Add beneficiary1 (Wallet Addr, Name, email, Phone num, percentage split)
* Add beneficiary2
* Add witness (Wallet Addr, Name, email)
* Add executor(Wallet Addr, Name)

**Witness**
* Sign contract (Using Wallet Addr, Name, Key)
(Check json will created in ~\jsonFiles\will.json)
* Verfiy signature (with hash produced from signing)

**Executor**
* Submit Death Certificate
(Testator's Name:Sam Yee, Death Cerficiation No.220427, Picture of Death cert)
* Activate Contract (with Executor's wallet Addr and private key)
(Ether sent from testator wallet account to contract address to various beneficiaries.)

**Beneficiary**
* Check myEtherWallet for received ether

#### Additional Functions
* Add multiple actors (eg: witness, beneficiary, executors)
* View Assets, Beneficiary, Executors, Witness
* Witness disagrees with contract, Able to add reason
* Terminate Will
* Logout

## Project Platform

Platform Used | Description
------------ | -------------
Python (v3.6.4)	| Stable version for web3.py to interface with Solidity
Pycharm (v2019.2)|Create application including UI and computation to reduce gas
Solidity, Remix|	Create smart contract template
EtherScan	|View transactions on blockchain
Metamask, MyEtherWallet	|Create multi-platform ethereum wallets
MyInfo API	|National Digital Identity (NDI) to authenticate the users
Google Authentication	|Provide OTP and 2FA
Json	|Create the will

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details


