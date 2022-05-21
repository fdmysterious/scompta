"""
┌──────────────────────────────────────────────────────┐
│ Simple REST api server for manipulating scompta data │
└──────────────────────────────────────────────────────┘

 Florian Dupeyron
 May 2022
"""

import numpy
import pandas as pd

import traceback
import toml

from   aiohttp import web
import aiohttp_cors

from   scompta import transactions, accounts

from dataclasses import asdict

# ┌────────────────────────────────────────┐
# │ Transactions endpoints                 │
# └────────────────────────────────────────┘

class API_Transactions_Handler:
    def __init__(self, config):
        self.config = config

    async def all_get(self, request):
        try:
            df_tr           = transactions.load("transactions.csv")
            df_tr["amount"] = df_tr["amount"].transform(lambda x: {"currency": x.currency, "amount": str(x.amount)})

            # DataFrame with NaN columns as None
            df_tr   = df_tr.replace({numpy.nan: None})

            # Transform to dict
            dict_tr = df_tr.to_dict(orient="records")

            return web.json_response({"data": dict_tr}, status=200)

        except Exception as exc:
            return web.json_response({
                "error": f"Could not load transactions: {exc!s}",
                "traceback": traceback.format_exc().split("\n")
            }, status=500)


    # ──────────── Routes property ─────────── #

    def routes(self, prefix=""):
        return [
            web.get(f"{prefix}/transactions", self.all_get)
        ]


# ┌────────────────────────────────────────┐
# │ Accounts endpoints                     │
# └────────────────────────────────────────┘

class API_Accounts_Handler:
    def __init__(self, config):
        self.config = config

    # ───────────── GET endpoints ──────────── #

    async def all_get(self, request):
        try:
            df_accounts         = accounts.load_from_dir("accounts")
            df_accounts["type"] = df_accounts["type"].transform(lambda x: x.value)

            # Replace NaN with None
            df_accounts   = df_accounts.replace({numpy.nan: None})

            # Transform to dict
            dict_accounts = df_accounts.to_dict(orient="index")

            return web.json_response({"data": dict_accounts}, status=200)

        except Exception as exc:
            return web.json_response({
                "error": f"Could not load accounts: {exc!s}",
                "traceback": traceback.format_exc().split("\n")
            }, status=500)

    # ──────────────── Routes ──────────────── #

    def routes(self, prefix=""):
        return [
            web.get(f"{prefix}/accounts", self.all_get)
        ]
    


# ┌────────────────────────────────────────┐
# │ Main webapp                            │
# └────────────────────────────────────────┘

if __name__ == "__main__":
    app = web.Application()

    # Load config
    with open("config.toml", "r") as fhandle:
        config = toml.load(fhandle)

    # Instanciate handlers
    h_transactions = API_Transactions_Handler(config)
    h_accounts     = API_Accounts_Handler    (config)


    # Add routes
    app.router.add_routes([
        *h_transactions.routes(),
        *h_accounts.routes()
    ])

    # CORS setup
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials = True,
            expose_headers    = "*",
            allow_headers     = "*"
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    # Server start
    web.run_app(app)
