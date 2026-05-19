from flask import Flask
import requests
import random

app = Flask(__name__)

USDT_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"


@app.route("/")
def home():

    try:

        url = "https://api.bscscan.com/api"

        params = {

            "module": "account",

            "action": "tokentx",

            "contractaddress": USDT_CONTRACT,

            "page": 1,

            "offset": 50,

            "sort": "desc"

        }

        response = requests.get(
            url,
            params=params
        ).json()

        txs = response["result"]

        final_tx = None

        for tx in txs:

            amount = float(
                tx["value"]
            ) / 1000000000000000000

            # 5 se 500 USDT only
            if amount >= 5 and amount <= 500:

                final_tx = tx

                break

        if not final_tx:

            return {
                "error": "No suitable USDT transaction found"
            }

        hash_value = final_tx["hash"]

        wallet = final_tx["to"]

        amount = round(

            float(final_tx["value"]) / 1000000000000000000,

            2

        )

        user_id = random.randint(

            100000,

            999999

        )

        return {

            "user_id": str(user_id),

            "amount": str(amount),

            "wallet": wallet,

            "hash": hash_value,

            "bot": "@YourBot"

        }

    except Exception as e:

        return {

            "error": str(e)

        }


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=10000

    )
