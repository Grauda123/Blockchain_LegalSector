from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

import requests
import sqlite3
import pyotp
from web3 import HTTPProvider, Web3
import os.path
# from deploy import getBeneficiaries, setBeneficiary, distributeEther, setExecutor, getWitnesses, setWitness, \
#     writeJsonWill, witnessRead, getDisagreeReason, compile_contract, deploy_contract, send_to_payable
import deploy
from deploy import *

HTOP = pyotp.HOTP("JASWY3DPEHPK3PXP")
# Create the application instance
app = Flask(__name__)
app.secret_key = "BlockChain"

#/// represents relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

''''@app.route("/OTPVerify", methods=["GET","POST"])
def OTPVerify():
    error = None
    if request.method == "POST":
        req = request.form
        HTOP = pyotp.HOTP("JASWY3DPEHPK3PXP")
        i = 3
        a = (HTOP.at(i))
        b = (HTOP.at(i+1))
        c = (HTOP.at(i+2))
        print(a)
        if req["otp"] == a:
            Asset,sgd,etherValue,totalAsset = convert()
            return render_template('show_asset.html', Asset=Asset,sgd=sgd, etherValue=etherValue,totalAsset=totalAsset)

        if req["otp"] == b:
            Asset, sgd, etherValue, totalAsset = convert()
            return render_template('show_asset.html', Asset=Asset, sgd=sgd, etherValue=etherValue,
                                   totalAsset=totalAsset)

        if req["otp"] == c:
            Asset,sgd,etherValue,totalAsset = convert()
            return render_template('show_asset.html', Asset=Asset,sgd=sgd, etherValue=etherValue,totalAsset=totalAsset)

        else:
            errorMsg = "Wrong OTP. Please enter again"
            print(error)
            return render_template('OTP.html', error=error, errorMsg=errorMsg)'''

# class Asset(db.Model):
#     id=db.Column(db.Integer, primary_key=True) 
#     name = db.Column(db.String(50))
#     value=db.Column(db.Integer)	

# def __repr__(self):
#     return "<name: {} value:{}>".format(self.name,self.value)

####config
PRC_ADDRESS = 'https://ropsten.infura.io/v3/2ae82295fc8c4f69815be6623202263b'
CONTRACTWILL_SOL = './solFiles/contractWill.sol'
CONTRACT_NAME = 'contractWill'
## Metamask address
WALLET_ADDRESS = "0xA29139bbE6f6a1e602900Eb75Ff19448959E089e"
WALLET_PRIVATE_KEY="263DBE181C44AD5DBC4E1512C661B59D11CA5A945B9F5622D9FEBC1E4C49B0A9"
## MEW address
#WALLET_ADDRESS = "0x291A678D5AB168b24B456737EaCca785668e9d2E"
#WALLET_PRIVATE_KEY="1aaa653261e01bd262eb0956797a6d0e1b1724697633ea981d12a39a9ff8f634"

##instantiate web3 object
w3 = Web3(HTTPProvider(PRC_ADDRESS, request_kwargs={'timeout':120}))
acct = w3.eth.account.privateKeyToAccount(WALLET_PRIVATE_KEY)
####

def convert():
    etherValue = []
    connection = sqlite3.connect('example.db')
    conn = connection.cursor()
    totalAsset = 0
    #### CONVERSION FROM 1 ETH to SGD
    url = "https://bravenewcoin-v1.p.rapidapi.com/convert"
    querystring = {"qty": "1", "from": "eth", "to": "sgd"}
    headers = {
        'x-rapidapi-host': "bravenewcoin-v1.p.rapidapi.com",
        'x-rapidapi-key': "2a00648a6cmsh855e1a922dfba21p116afcjsnb919016d1f20"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.text)
    dict = response.json()
    sgd = dict['to_quantity']
    print('sgd is {}'.format(sgd))
    ####

    #### calculate ether of the Asset
    # Asset=Asset.query.all()
    # for x in Asset:
    # 	print(x.name, x.value)
    # 	value = float(x.value)/sgd
    # 	etherValue.append(value)
    conn.execute("SELECT * from asset")
    Asset = conn.fetchall()
    print(Asset)
    for x in Asset:
        print(x[0], x[1])
        value = float(x[1]) / sgd
        etherValue.append(value)

    for x in etherValue:
        totalAsset += x;

    conn.close()
    print('etherValue is {}'.format(etherValue))
    print('totalAsset is {}'.format(totalAsset))
    ####
    return Asset,sgd, etherValue,totalAsset


@app.route("/")
def GetNRIC():
    return render_template("GetNRIC.html")

@app.route('/logout')
def logout():
	session.pop('user', None)
	return render_template('GetNRIC.html')

@app.route("/confirm", methods=["GET","POST"])
def confirm():
    if request.method == "POST":
        req = request.form.to_dict()
        uinfin = req["uinfin"]
        role = req["role"]
        response = requests.get('https://sandbox.api.myinfo.gov.sg/com/v3/person-sample/' + uinfin)
        y = response.json()
        name = str(y['name']['value'])
        email = str(y['email']['value'])
        MobileNum = str(y['mobileno']['nbr']['value'])
        session['user'] = role
        return render_template("Confirm.html", name=name, email=email, MobileNum=MobileNum, uinfin=uinfin)

@app.route("/otp", methods=["GET","POST"])
def OTP():
    errorMsg="None"
    return render_template("OTP.html",errorMsg=errorMsg)

@app.route("/OTPVerify", methods=["GET","POST"])
def OTPVerify():
    error = None
    if request.method == "POST":
        req = request.form
        HTOP = pyotp.HOTP("JASWY3DPEHPK3PXP")
        i = 7
        a = (HTOP.at(i))
        b = (HTOP.at(i+1))
        c = (HTOP.at(i+2))
        d = (HTOP.at(i+3))
        print(a)
        if req["otp"] == a:
            return render_template('home.html')

        if req["otp"] == b:
            return render_template('home.html')

        if req["otp"] == c:
            return render_template('home.html')

        if req["otp"] == d:
            return render_template('home.html')

        else:
            errorMsg = "Wrong OTP. Please enter again."
            print(error)
            return render_template('OTP.html', error=error, errorMsg=errorMsg)

@app.route('/home',methods=['Get','POST'])
def home():
    hashArray=[]
    try:
        wei_amount = w3.eth.getBalance(contract_address)
        eth_amount = w3.fromWei(wei_amount, 'ether')
        result = None

        hashArray=getHash(contract)
        if request.method == 'POST':
            req = request.form
            print('req is {}'.format(req))
            try:
                signature = req['signature']
                privKey = req['privKey']
                willHash = req['willHash']
                verifyMessage = VerifySignature(signature, privKey, willHash)
                if (verifyMessage == True):
                    #result='Signature is legit'
                    #print(result)
                    result=True
                    print(result)
                else:
                    #result= 'Signature does not match! Document might have been modified or check that same key is used when signing'
                    #print(result)
                    result=False
                    print(result)
                return render_template("home.html",result=result)
            except Exception as excep:
                print('post data in home something wrong')
                print(excep)
    except Exception as ex:
        print('home something wrong')
        print(ex)
    finally:
        print("hashArray in home is",hashArray)
        return render_template('home.html',contract_address=contract_address,eth_amount=eth_amount,hashArray=hashArray,result=result)
    #return render_template('home.html')

@app.route('/addAsset')
def addAsset():
    try:
        return render_template('addAsset.html')
    except Exception as e:
        print('error in addAsset')
        print(e)
        #return render_template('error_page.html')

@app.route('/showAsset', methods = ['GET', 'POST'])
def show_asset():
    # Todo: To add/get asset to/from blockchain
    try:
      if request.method == 'POST':
        req = request.form
        print('req is {}'.format(req))
        AssetName = req['AssetName']
        AssetValue = req['AssetValue']
        try:
           #add asset to database
            conn = sqlite3.connect('example.db')
            c = conn.cursor()
            c.execute("INSERT INTO asset VALUES(?,?)",(AssetName,AssetValue))
            conn.commit()
            conn.close()
        except Exception as ex:
            print('error occurred in when adding asset to DB')
            print('ex is {}'.format(ex))

    finally:
        #getAsset function
        Asset, sgd, etherValue, totalAsset = convert()
        return render_template('show_asset.html', Asset=Asset, sgd=sgd, etherValue=etherValue, totalAsset=totalAsset)

@app.route('/contract')
def contract():
    try:
        con = sqlite3.connect('example.db')
        c = con.cursor()
        c.execute("SELECT COUNT(*) from beneficiary")
        num = c.fetchone()
        Bnum=num[0]

        c.execute("SELECT * from beneficiary")
        Blist=c.fetchall()
        con.close()
        return render_template('contract.html', Bnum=Bnum, Blist=Blist)
    except con.Error as err:
        return render_template('error_page.html')

@app.route('/addBeneficiary')
def addBeneficiary():
    try:
        return render_template('addBeneficiary.html')
    except Exception as e:
        print('error in addBeneficiary')
        print(e)
        #return render_template('error_page.html')

def testCallFunction(contract, WALLET_ADDRESS, WALLET_PRIVATE_KEY, BeneficiaryWalletAddr, email, telNum, percentSplit):
    print('Looping through testCallFunction')
    print('contract is {}'.format(contract))
    print('wallet addr is {}'.format(WALLET_ADDRESS))
    print('wallet private key is {}'.format(WALLET_PRIVATE_KEY))
    print('beneficiaryWalletAddr is {}'.format(BeneficiaryWalletAddr))
    print('email is {}'.format(email))
    print('telNum is {}'.format(telNum))
    print('percentsplit is {}'.format(percentSplit))
    print('end of testCallFunction')

@app.route('/beneficiary', methods = ['GET', 'POST'])
def beneficiary():
    # todo: When beneficiary dies, split his percentage to the other beneficiaries
    # ## Store in Database
    # try:
    #     conn = sqlite3.connect('example.db')
    #     c = conn.cursor()
    #     c.execute("INSERT INTO beneficiary VALUES(?,?,?,?)",(addr,email,telNum,percent))
    #     conn.commit()
    #     conn.close()
    #     return render_template('beneficiary.html')
    # except conn.Error as err:
    #     return render_template('error_page.html')
    BeneficiariesArray = []
    remainingPercent = 100
    remainingPercent = 100
    try:
      if request.method == 'POST':
        req = request.form
        print('req is {}'.format(req))
        #testCallFunction(contract, WALLET_ADDRESS, WALLET_PRIVATE_KEY, BeneficiaryWalletAddr, email, telNum, percentSplit)
        try:
            addr = req['addr']
            name=req['name']
            email = req['email']
            telNum = req['telNum']
            percent = req['percent']
            BeneficiaryWalletAddr = addr
            email = email
            telNum = int(telNum)
            percentSplit = int(percent)
            print('\n Calling setBeneficiary method ')
            print('contract is {}'.format(contract))
            print('\n wallet addr is {}'.format(WALLET_ADDRESS))
            print('wallet private key is {}'.format(WALLET_PRIVATE_KEY))
            print('beneficiaryWalletAddr is {}'.format(BeneficiaryWalletAddr))
            print('email is {}'.format(email))
            print('telNum is {}'.format(telNum))
            print('percentsplit is {}'.format(percentSplit))

            setBeneficiary(contract, WALLET_ADDRESS, WALLET_PRIVATE_KEY, w3.toChecksumAddress(BeneficiaryWalletAddr),name, email, telNum, percentSplit)
        except Exception as ex:
            print('error occurred in setBeneficiary method')
            print('ex is {}'.format(ex))

        print('addr is {}'.format(addr))
        print('remaining percent is {}'.format(remainingPercent))
        # return render_template('beneficiary.html', remainingPercent=remainingPercent,
        #                        BeneficiariesArray= BeneficiariesArray, addr=addr,
        #                     email=email,telNum=telNum,percent=percent)
        # try:
        #     # bool = req[]
        #     # if bool == true:
        #     # beneficiaryDead + 1, call beneficiaryDeath
        #     # requireSign bool stored in session -> need sign
        #     # if bool == false:
        #     # beneficiaryDead + 1, call beneficiaryDeath
        #
        # except Exception as excep:
        #     print('error occurred in method')
        #     print('ex is {}'.format(excep))
    finally:
        ###check for remaining percentage left after setting benefiicaries
        print('calling getBeneficiaries()')
        BeneficiariesArray = getBeneficiaries(contract, BeneficiariesArray)
        print('\nBeneficiariesArray is {}'.format(BeneficiariesArray))

        for i in range(len(BeneficiariesArray)):
            percent = BeneficiariesArray[i][4]
            print(percent)
            remainingPercent -= percent
            print('remaining percentage is {}'.format(remainingPercent))
        return render_template('beneficiary.html', remainingPercent=remainingPercent,
                               BeneficiariesArray=BeneficiariesArray)

@app.route('/activate')
def activateContract():
    return render_template('activate.html')

@app.route('/send', methods = ['GET', 'POST'])
def send():
   #Get the current conversion by calling conversion method again
    Asset, sgd, etherValue, totalAsset = convert()
    wei_amount = w3.eth.getBalance(contract_address)
    eth_amount = w3.fromWei(wei_amount, 'ether')
    BeneficiariesArray = []

    if request.method == 'POST':
        req = request.form
        walletAddr = req['addr']
        privKey= req['privKey']

        ExecutorActivateContract(contract,w3.toChecksumAddress(walletAddr),privKey,w3.toChecksumAddress(walletAddr))
        amount_in_ether = totalAsset
        try:
            print('sending to contract {}'.format(amount_in_ether))
            send_to_payable(contract, WALLET_ADDRESS, WALLET_PRIVATE_KEY, amount_in_ether)
            wei_amount = w3.eth.getBalance(contract_address)
            eth_amount = w3.fromWei(wei_amount, 'ether')
            print('Current contract value is {}'.format(eth_amount))
        except Exception as ex:
            print(ex)
            #return render_template('error_page.html')
        try:
             BeneficiariesArray = getBeneficiaries(contract, BeneficiariesArray)
             print('\nBeneficiariesArray is {}'.format(BeneficiariesArray))
             print('totalAsset is {}'.format(totalAsset))
             for i in range(len(BeneficiariesArray)):
                BenAddr = BeneficiariesArray[i][0]
                percent = BeneficiariesArray[i][4]
                amountToReceive = (percent * totalAsset) / 100
                print(BenAddr, percent, amountToReceive)
                amountToReceive = w3.toWei(amountToReceive, 'ether')
                print('passing {} wei to distributeEther function'.format(amountToReceive))
                distributeEther(contract, WALLET_ADDRESS, WALLET_PRIVATE_KEY, BenAddr, amountToReceive)
                print('Ether has been split')
        except Exception as ex:
            print(ex)
            #return render_template('error_page.html')

    return render_template('send.html',totalAsset=totalAsset, eth_amount=eth_amount)

@app.route('/DeathConfirm', methods=["GET","POST"])
def DeathConfirm():
    # Get the current conversion by calling conversion method again
    Asset, sgd, etherValue, totalAsset = convert()
    eth_amount = 0
    BeneficiariesArray = []
    error = None
    if request.method == "POST":
        req = request.form
        if req["TestatorName"] == "Sam Yee" and req["CertNo"] == "220427":
            verify = "true"
            return render_template('activate.html')
        else:
            errorMsg = " Unsuccessfully verified. Please enter again."
            print(error)
            return render_template('DeathCertVerify.html', error=error, errorMsg=errorMsg)

@app.route('/DeathCertVerify')
def DeathCertVerify():
    return render_template('DeathCertVerify.html')

@app.route('/addExecutors')
def addExecutors():
    try:
        return render_template('addExecutors.html')
    except Exception as e:
        print('error in addExecutors')
        print(e)
        #return render_template('error_page.html')
@app.route('/getExecutors', methods = ['GET', 'POST'])
def getExecutors():
    try:
        if request.method == 'POST':
            req = request.form
            print('req is {}'.format(req))
            try:
                addr = req['addr']
                name = req['name']
                print('addr is {}'.format(addr))
                print('name is {}'.format(name))
                setExecutor(contract, WALLET_ADDRESS, WALLET_PRIVATE_KEY,w3.toChecksumAddress(addr),name)
            except Exception as ex:
                print('error occurred in setExecutors method')
                print('ex is {}'.format(ex))
    finally:
        ExecutorsArray= []
        ExecutorsArray = deploy.getExecutors(contract,ExecutorsArray)
        #ExecutorsArray = getExecutors()
        print("ExecutorsArray is {}".format(ExecutorsArray))
        return render_template('getExecutors.html',ExecutorsArray=ExecutorsArray)
@app.route('/addWitness')
def addWitness():
    try:
        return render_template('addWitness.html')
    except Exception as e:
        print('error in addWitness')
        print(e)
        #return render_template('error_page.html')
@app.route('/getWitness', methods = ['GET', 'POST'])
def getWitness():
    try:
        if request.method == 'POST':
            req = request.form
            print('req is {}'.format(req))
            try:
                addr = req['addr']
                name = req['name']
                email = req['email']
                print('addr is {}'.format(addr))
                print('name is {}'.format(name))
                print('email is {}'.format(email))
                setWitness(contract, WALLET_ADDRESS, WALLET_PRIVATE_KEY,w3.toChecksumAddress(addr),name,email)
            except Exception as ex:
                print('error occurred in setWitness method')
                print('ex is {}'.format(ex))
    finally:
        WitnessArray = []
        WitnessArray = getWitnesses(contract, WitnessArray)
        print("witnessArray is {}".format(WitnessArray))
        return render_template('getWitness.html',WitnessArray=WitnessArray)

@app.route('/createWillFile')
def createWill():
    try:
        BeneficiariesArray=[]
        WitnessArray=[]
        ExecutorsArray=[]
        BeneficiariesArray = getBeneficiaries(contract, BeneficiariesArray)
        print("BeneficiariesArray retrieved in createWillFile is ",BeneficiariesArray)
        WitnessArray = getWitnesses(contract, WitnessArray)
        print("WitnessArray retrieved in createWillFile is ",WitnessArray)
        ExecutorsArray = deploy.getExecutors(contract, ExecutorsArray)
        print("ExecutorsArray retrieved in createWillFile is ",ExecutorsArray)
        # BeneficiariesArray = [
        #     ["0x291A678D5AB168b24B456737EaCca785668e9d2E", "beneficiary1", "beneficiary1@yahoo.com", 87253546, 60],
        #     ["0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E", "beneficiary2", "josh@yahoo.com", 81234586, 40]]
        # ExecutorsArray = [["0x9a08ee39abc294804db5cc8058a049e219696566", "executor1", False],
        #                   ["0x99d8d926d5e1302640bbeb0868923a1938c8fd5e", "executor2", False]]
        # WitnessArray = [['0xA0B9Bd956781f6d809C9B512168e814a986Cc7d2', 'witness1', 'witness1@yahoo.com', False],
        #                 ['0x97822B15f3990573dB7445405A06C132566d07E1', 'witness2', 'witness2@yahoo.com', False]]
        try:
            if os.path.exists("jsonFiles/will.json"):
                print("json will file already exists")
                #retrieve signature from will, rewrite to update writetoJsonWill and add signature

                # After witness sign, cannot update file anymore!!
                # Delete will.json each time want run!!!
            else:
                writeJsonWill(BeneficiariesArray, WitnessArray, ExecutorsArray)
            # add original Hash to blockchain
            readable_hash = calculateHash()
            print("readable_hash from createWillFile is",readable_hash)
            sendHash(contract, WALLET_ADDRESS, WALLET_PRIVATE_KEY, readable_hash)
        except Exception as excep:
            print('error in trying to writefile and sendHash')
            # display the file in html
        with open("jsonFiles/will.json", 'r') as read_file:
            content = json.load(read_file)

        #content = str(content)
        # content = "<br />".join(content.split("\n"))
        #content = content.replace('\\n', '<br>')
        #content = content.replace('\', \'', '<br>')

        print("type is ", type(content))
        print('content is {}'.format(content))
        return render_template('createWillFile.html', content=content)
    except Exception as ex:
        print("error occurred in createWillFile")
        print('ex is {}'.format(ex))


@app.route('/witnessMiddle', methods=['GET', 'POST'])
def witnessMiddle():
    try:
        if request.method == 'POST':
            req = request.form
            print('req is {}'.format(req))
            try:
                addr = req['addr']
                name=req['name']
                privKey = req['pk']
                choice = req['answer']
                reason = req['comment']
                print("choice is {}".format(choice))
                if (choice == "True"):
                    print('witness has agreed with contract')
                    # witness sign
                    #get hash of file
                    readable_hash = calculateHash()
                    print('readable_hash is {}'.format(readable_hash))
                    hashArray = getHash(contract)
                    print('hashArray is {}'.format(hashArray))
                    print("hashArray[-1] is",hashArray[-1])
                    if readable_hash == hashArray[-1]:
                        print('readable_hash = last element of array')
                        signature = signing(privKey, readable_hash)
                        signature=str(signature)
                        #add signature to will file
                        addSigtoWill(name,signature)
                        readable_hash = calculateHash()
                        print("readable_hash to send in WitnessMiddle is ",readable_hash)
                        #sendHash to b.c
                        sendHash(contract,WALLET_ADDRESS,WALLET_PRIVATE_KEY,readable_hash)
                        #add verify function to home page
                        witnessRead(contract, w3.toChecksumAddress(addr), privKey, 0, w3.toChecksumAddress(addr), True, "")
                        # after sign return back to home
                        hashArray = getHash(contract)
                        wei_amount = w3.eth.getBalance(contract_address)
                        eth_amount = w3.fromWei(wei_amount, 'ether')
                        result=None
                        #return render_template('home.html', contract_address=contract_address, eth_amount=eth_amount,hashArray=hashArray, result=result)
                        return redirect(url_for('home',contract_address=contract_address, eth_amount=eth_amount,hashArray=hashArray, result=result))

                    else:
                        #signature does not match
                        error= 'Signature does not match! Document might have been modified or check that same key is used when signing'
                        return render_template('createWillFile.html',error=error)
                if (choice == "False"):
                    print('witness disagree with contract')
                    # set witness reason and send reason to the page
                    witnessRead(contract, w3.toChecksumAddress(addr), privKey, 0, w3.toChecksumAddress(addr), False, reason)
                    reasonArray = []
                    reasonArray = getDisagreeReason(contract, reasonArray)
                    return render_template('getReason.html', reasonArray=reasonArray)
            except Exception as ex:
                print("error in split of choices")
                print("ex is {}".format(ex))
    except Exception as ex:
        print("error in witnessMiddle")
        print("ex is {}".format(ex))

@app.route('/getReason')
def getReason():
    reasonArray = []
    reasonArray = getDisagreeReason(contract, reasonArray)
    return render_template('getReason.html', reasonArray=reasonArray)

@app.route('/terminate',methods=['Get','POST'])
def terminate():
    amount_in_ether = 0.01
    try:
        wei_amount = w3.eth.getBalance(contract_address)
        eth_amount = w3.fromWei(wei_amount, 'ether')
        message=None
        if request.method == 'POST':
            try:
                req = request.form
                print('req in termiante is {}'.format(req))
                terminateContract(contract, WALLET_ADDRESS, WALLET_PRIVATE_KEY, WALLET_ADDRESS)
                message="Remaining value has been sent to your account"
            except Exception as excep:
                print("error in calling terminateContract")
                print(excep)
                message="ether unable to be sent"
    except Exception as ex:
        print("error in terminate")
        print(ex)
    finally:
        return render_template('/terminate.html',contract_address=contract_address,eth_amount=eth_amount,message=message)

####compiling contract to get abi
contract_name, contract_interface = compile_contract(CONTRACTWILL_SOL,CONTRACT_NAME)
####deploying contract
contract_address = deploy_contract(acct, contract_interface)
print('contract address = {}'.format(contract_address))
##create contract object
contract = w3.eth.contract(address=contract_address, abi=contract_interface['abi']);
print('contract after building is {}'.format(contract))


# ###check for remaining percentage left after setting benefiicaries
# BeneficiariesArray = []
# BeneficiariesArray = getBeneficiaries(contract, BeneficiariesArray)
# print('\nBeneficiariesArray is {}'.format(BeneficiariesArray))
# remainingPercent = 100
# for i in range(len(BeneficiariesArray)):
#     percent = BeneficiariesArray[i][3]
#     print(percent)
#     remainingPercent -= percent
#     print('remaining percentage is {}'.format(remainingPercent))

if __name__ == '__main__':
    #app.run(debug=True,use_reloader=False)
    app.run()
    #app.run(debug=True)