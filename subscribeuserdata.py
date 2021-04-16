import logging
import sys
from binance_f import RequestClient
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException

from binance_f.base.printobject import *

import api_secrets

g_api_key = api_secrets.api_key
g_secret_key = api_secrets.api_secret

# Start user data stream
request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
listen_key = request_client.start_user_data_stream()
print("listenKey: ", listen_key)

# Keep user data stream
result = request_client.keep_user_data_stream()
print("Result: ", result)

# Close user data stream
# result = request_client.close_user_data_stream()
# print("Result: ", result)

def setup_logger(log_id: str):
    the_logger = logging.getLogger(log_id)
    the_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    handler.setFormatter(formatter)
    the_logger.addHandler(handler)

setup_logger("user-data-stream")
setup_logger("binance-futures")
setup_logger("binance-client")

my_logger = logging.getLogger("user-data-stream")

sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)

def simple_cb(data_type: SubscribeMessageType, event: 'any', msg):
    if  data_type == SubscribeMessageType.PAYLOAD:
        my_logger.info(msg)

def callback(data_type: 'SubscribeMessageType', event: 'any'):
    if data_type == SubscribeMessageType.RESPONSE:
        print("Event ID: ", event)
    elif  data_type == SubscribeMessageType.PAYLOAD:
        if(event.eventType == "ACCOUNT_CONFIG_UPDATE"):
            print("Event Type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("Transaction time: ", event.transactionTime)
            print("symbol: ", event.symbol)
            print("leverage: ", event.leverage)
        elif(event.eventType == "ACCOUNT_UPDATE"):
            print("Event Type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("Transaction time: ", event.transactionTime)
            print("=== Balances ===")
            PrintMix.print_data(event.balances)
            print("================")
            print("=== Positions ===")
            PrintMix.print_data(event.positions)
            print("================")
        elif(event.eventType == "ORDER_TRADE_UPDATE"):
            print("Event Type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("Transaction Time: ", event.transactionTime)
            print("Symbol: ", event.symbol)
            print("Client Order Id: ", event.clientOrderId)
            print("Side: ", event.side)
            print("Order Type: ", event.type)
            print("Time in Force: ", event.timeInForce)
            print("Original Quantity: ", event.origQty)
            print("Position Side: ", event.positionSide)
            print("Price: ", event.price)
            print("Average Price: ", event.avgPrice)
            print("Stop Price: ", event.stopPrice)
            print("Execution Type: ", event.executionType)
            print("Order Status: ", event.orderStatus)
            print("Order Id: ", event.orderId)
            print("Order Last Filled Quantity: ", event.lastFilledQty)
            print("Order Filled Accumulated Quantity: ", event.cumulativeFilledQty)
            print("Last Filled Price: ", event.lastFilledPrice)
            print("Commission Asset: ", event.commissionAsset)
            print("Commissions: ", event.commissionAmount)
            print("Order Trade Time: ", event.orderTradeTime)
            print("Trade Id: ", event.tradeID)
            print("Bids Notional: ", event.bidsNotional)
            print("Ask Notional: ", event.asksNotional)
            print("Is this trade the maker side?: ", event.isMarkerSide)
            print("Is this reduce only: ", event.isReduceOnly)
            print("stop price working type: ", event.workingType)
            print("Is this Close-All: ", event.isClosePosition)
            if not event.activationPrice is None:
                print("Activation Price for Trailing Stop: ", event.activationPrice)
            if not event.callbackRate is None:
                print("Callback Rate for Trailing Stop: ", event.callbackRate)
        elif(event.eventType == "listenKeyExpired"):
            print("Event: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
    else:
        print("Unknown Data:")
    print()


def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)


sub_client.subscribe_user_data_event(listen_key, simple_cb, error)
