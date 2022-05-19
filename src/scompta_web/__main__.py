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

from   aiohttp import web
import aiohttp_cors

from   scompta import transactions
from dataclasses import asdict


async def transactions_get(request):
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


if __name__ == "__main__":
    app = web.Application()

    # Add routes
    app.router.add_routes([
        web.get("/transactions", transactions_get)
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
