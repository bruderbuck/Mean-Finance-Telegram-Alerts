import web3
import json
import requests
from datetime import datetime as Datetime
import time

lastMessageTime = 0

#load telegram bot token
token = 0
with open("token.txt") as file:
    token = file.read()

#load the ABI from a JSON file
contract_abi = 0
with open("abi.json") as f:
    contract_abi = json.load(f)

#load position ID
positionID = 0
with open("positionID.txt") as file:
    positionID = int(file.read())

#load chat ID
chatID = 0
with open("chatID.txt") as file:
    chatID = file.read()


# Set the HTTP endpoint for your Polygon node
w3 = web3.Web3(web3.Web3.HTTPProvider("https://polygon-rpc.com"))

# Set the contract address and ABI (Application Binary Interface)
contract_address = "0xA5AdC5484f9997fBF7D405b9AA62A7d88883C345"


# Instantiate the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


#loop
while(True):

    #get the current time
    currentTime = int(time.time())

    #check wether 4 hours have passed
    if currentTime > (lastMessageTime+(3600*4)): 
        lastMessageTime = currentTime
        # Call the "userPosition" function of the contract with the input "positionID"
        try:
            result = contract.functions.userPosition(positionID).call()
        


            #calculate how much time is left until last swap 
            swapsLeft = result[-3]
            secondsBetweenSwaps = result[2]
            roughlyTimeLeftSeconds = swapsLeft*secondsBetweenSwaps
            roughlyTimeLeftHours = swapsLeft*secondsBetweenSwaps/3600
            # Print the result
            print(swapsLeft)
            print(roughlyTimeLeftHours)



            outOfFundsTimestamp = int(time.time()) + roughlyTimeLeftSeconds
            datetime_obj = Datetime.utcfromtimestamp(outOfFundsTimestamp)

            print(str(datetime_obj.strftime("%d.%m.%y %H:%M:%S")))

            #check wether the last swap is less than 72 hours away
            if roughlyTimeLeftHours < 72:
                
                #text user on telegram
                messageString = str("you have only funds left for " + str(swapsLeft) + " swaps! You will run out of funds around " + str(datetime_obj.strftime("%d.%m.%y %H:%M:%S")))
                params = {"chat_id":chatID, "text":messageString}
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                try:
                    message = requests.post(url, params=params)
                except:
                    print("Oops! I tried to send a telegram message. But ", sys.exc_info()[0], " occurred.")

        except:
            print("Oops! I tried to call userPosition(). But ", sys.exc_info()[0], " occurred.")
    #wait 60s before checking if 4 hours have passed
    time.sleep(60)