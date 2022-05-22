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

from   aiohttp     import web
import aiohttp_cors

from   scompta     import transactions, accounts
from   dataclasses import dataclass, asdict

from   pathlib     import Path
from   functools   import partial

from   money       import Money

# ┌────────────────────────────────────────┐
# │ Config dataclass                       │
# └────────────────────────────────────────┘

@dataclass
class SComptaWeb_Config:
    dir_accounts: Path
    dir_periods:  Path

    @classmethod
    def from_dict(cls, data):
        return cls(
            dir_accounts = Path(data["directories"]["accounts"]),
            dir_periods  = Path(data["directories"]["periods" ])
        )


# ┌────────────────────────────────────────┐
# │ Transactions endpoints                 │
# └────────────────────────────────────────┘

class API_Error(Exception):
    """
    Helper class for API errors
    """
    def __init__(self, msg, error_code=500):
        super().__init__(msg)
        self.error_code = error_code


class API_Transactions_Handler:
    def __init__(self, config):
        self.config = config

    # ──────────────── Helpers ─────────────── #
    
    def _transactions_path_for_period(self, period):
        return self.config.dir_periods / period / "transactions.csv"

    def _load_transactions_period(self, period):
        transactions_path = self._transactions_path_for_period(period)

        if not transactions_path.exists():
            raise API_Error(f"transactions for period {period} not found", error_code=404)

        return transactions.load(transactions_path)


    # ─────────────── GET stuff ────────────── #

    async def all_get(self, request):
        try:
            # Extract period
            period = request.match_info["period"]

            # Load period's transactions
            df_tr = self._load_transactions_period(period)
            df_tr["amount"] = df_tr["amount"].transform(lambda x: {"currency": x.currency, "amount": str(x.amount)})

            # DataFrame with NaN columns as None
            df_tr   = df_tr.replace({numpy.nan: None})

            # Transform to dict
            dict_tr = df_tr.to_dict(orient="records")

            return web.json_response({"data": dict_tr}, status=200)

        except API_Error as exc:
            return web.json_response({
                "error": f"Could not load transactions: {exc!s}",
                "traceback": traceback.format_exc().split("\n")
            }, status=exc.error_code)

        except Exception as exc:
            return web.json_response({
                "error": f"Could not load transactions: {exc!s}",
                "traceback": traceback.format_exc().split("\n")
            }, status=500)

    async def raise_error(self, err_msg, err_code):
        return web.json_response({"error": err_msg}, status=err_code)

    # ────────────── POST stuff ────────────── #
    
    async def post(self, request):
        """
        Post data:
            - day
            - time
            - label
            - from
            - to
            - amount
            - tag [Optional]
        """
        try:
            data = await request.json()

            # Load transactions
            period = request.match_info["period"]
            df_tr  = self._load_transactions_period(period)

            # Build entry record
            record = {
                "day":   data["day"],
                "time":  data.get("time", None),
                "label": data["label"],
                "from":  data["from"],
                "to":    data["to"],
                "amount": Money(data["amount"]["value"], data["amount"]["currency"]),
                "tag":   data.get("tag", None)
            }

            # Add entry record to dataframe
            df_tr = pd.concat([df_tr, pd.DataFrame.from_records([record])])

            # Save transactions!
            transactions.save(self._transactions_path_for_period(period), df_tr)

            # Return 200 response
            return web.json_response({}, status=200)

        except KeyError  as exc:
            return web.json_response({
                "error": f"Missing field '{exc!s}'",
                "traceback": traceback.format_exc().split("\n")
            }, status=500)

        except API_Error as exc:
            return web.json_response({
                "error": f"Could not post transaction: {exc!s}",
                "traceback": traceback.format_exc().split("\n")
            }, status=exc.error_code)

        except Exception as exc:
            return web.json_response({
                "error": f"Could not post transaction: {exc!s}",
                "traceback": traceback.format_exc().split("\n")
            }, status=500)




    # ──────────── Routes property ─────────── #

    def routes(self, prefix=""):
        return [
            web.get (prefix + "/transactions/{period:\d{4}-\d{2}}", self.all_get),
            web.get (prefix + "/transactions/{inv_period}"        , lambda r: self.raise_error(f"Invalid period name: {r.match_info['inv_period']}", 404)),

            web.post(prefix + "/transactions/{period:\d{4}-\d{2}}", self.post),
            web.post(prefix + "/transactions/{inv_period}"        , lambda r: self.raise_error(f"Invalid period name: {r.match_info['inv_period']}", 404)),
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
            # Load accounts
            df_accounts         = accounts.load_from_dir(self.config.dir_accounts)
            df_accounts["type"] = df_accounts["type"].transform(lambda x: x.value)

            # Replace NaN with None
            df_accounts   = df_accounts.replace({numpy.nan: None})

            # Transform to dict
            dict_accounts = df_accounts.to_dict(orient="index")

            return web.json_response({"data": dict_accounts}, status=200)

        except API_Error as exc:
            return web.json_response({
                "error": f"Could not load accounts: {exc!s}",
                "traceback": traceback.format_exc().split("\n")
            }, status=exc.error_code)

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
        config = SComptaWeb_Config.from_dict(toml.load(fhandle))

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
