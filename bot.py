from fetch_stock import fetch_stock_information
from send_message import send_telegram

stock = fetch_stock_information("0050.TW")

print(f"股票 {stock.symbol} 的最新 K 值為 {stock.current_k:.2f}，D 值為 {stock.current_d:.2f}。")
send_telegram(
    f"股票 {stock.symbol} 的最新 K 值為 {stock.current_k:.2f}，D 值為 {stock.current_d:.2f}。")
