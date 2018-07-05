import aiohttp
from pysshchat.commands import register

@register("crypto")
async def do_crypto(user, args):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.binance.com/api/v3/ticker/price") as resp:
            data = await resp.json()
            out = ""

            btc = float(next((item for item in data if item["symbol"] == "BTCUSDT"), None)["price"])
            out += "BTC: $%.2f\n" % btc
            for money in args:
                money = money.upper()
                symbol = next((item for item in data if item["symbol"] == money + "BTC"), None)
                if symbol:
                        price = float(symbol["price"])
                        out += "%s: %.8f ($%.2f)\n" % (money, price, price * btc)

            user.local(out, off_formatting=True)
