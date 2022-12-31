import web3
import json
import requests
from datetime import datetime as Datetime
import time

with open("token.txt") as file:
    token = file.read()


contract_abi = 0
with open("abi.json") as f:
    contract_abi = json.load(f)
    #print(info_json)
#print(contract_abi)

chatID = 0
with open("chatID.txt") as file:
    chatID = file.read()


positionID = 0
with open("positionID.txt") as file:
    positionID = int(file.read())


update_id=0

w3 = web3.Web3(web3.Web3.HTTPProvider("https://polygon-rpc.com")) #https://polygon-mainnet.infura.io/v3/fc232585a19c491998585ac383ca7510
# Set the contract address and ABI (Application Binary Interface)
contract_address = "0xA5AdC5484f9997fBF7D405b9AA62A7d88883C345"
# Instantiate the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

while True:

    try:
        answer = requests.get(f"https://api.telegram.org/bot{token}/getUpdates")
        content = answer.content
        data = json.loads(content)
        newUpdate_id = data['result'][-1]['update_id']
        #print(data['result'])

        if newUpdate_id>update_id:
            update_id = newUpdate_id
            text = data['result'][-1]['message']['text']
            #print(text)
            if text == 'Update':
                result = contract.functions.userPosition(positionID).call()

                swapsLeft = result[-3]
                secondsBetweenSwaps = result[2]
                roughlyTimeLeftSeconds = swapsLeft*secondsBetweenSwaps
                roughlyTimeLeftHours = swapsLeft*secondsBetweenSwaps/3600

                outOfFundsTimestamp = int(time.time()) + roughlyTimeLeftSeconds
                datetime_obj = Datetime.utcfromtimestamp(outOfFundsTimestamp)

                messageString = str("you have funds left for " + str(swapsLeft) + " swaps! You will run out of funds around " + str(datetime_obj.strftime("%d.%m.%y %H:%M:%S")))
                params = {"chat_id":chatID, "text":messageString}
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                message = requests.post(url, params=params)
    except:
        print("Oops! I tried to get Updates from the telegram bot. But ", sys.exc_info()[0], " occurred.")
                
    time.sleep(3)
