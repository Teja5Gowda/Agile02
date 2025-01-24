from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Simulated market data
market_data = {
    "AAPL": 150.0,
    "TSLA": 700.0,
    "GOOGL": 2800.0,
    "AMZN": 3300.0,
    "MSFT": 300.0,
}

# User's portfolio and history
portfolio = {
    "cash": 100000.0,  # Initial cash balance
    "assets": {},  # Stocks and their quantities
}

trade_history = []  # List to store the user's trade history


def generate_market_data():
    """Randomly update stock prices to simulate live market changes."""
    for stock in market_data:
        market_data[stock] += random.uniform(-5, 5)  # Random price fluctuation
        market_data[stock] = round(market_data[stock], 2)  # Round to 2 decimal places


def calculate_portfolio_value():
    """Calculates the total portfolio value including cash and assets."""
    total_value = portfolio["cash"]  # Start with available cash
    for stock, quantity in portfolio["assets"].items():
        total_value += market_data[stock] * quantity  # Add the value of each stock in the portfolio
    return round(total_value, 2)


@app.route("/")
def index():
    """Homepage showing market data, portfolio, and trade history."""
    generate_market_data()  # Simulate live updates to stock prices
    total_value = calculate_portfolio_value()
    profit_loss = round(total_value - 100000, 2)  # Compare with the initial cash amount ($100,000)
    return render_template(
        "index.html",
        market_data=market_data,
        portfolio=portfolio,
        trade_history=trade_history,
        total_value=total_value,
        profit_loss=profit_loss,
    )


@app.route("/trade", methods=["POST"])
def trade():
    """Handles buy/sell trade requests."""
    action = request.form["action"]
    stock = request.form["stock"]
    quantity = int(request.form["quantity"])

    stock_price = market_data[stock]
    cost = stock_price * quantity

    if action == "buy":
        if cost > portfolio["cash"]:
            return "Insufficient funds to complete the trade.", 400
        portfolio["cash"] -= cost
        portfolio["assets"][stock] = portfolio["assets"].get(stock, 0) + quantity
        trade_history.append({"action": "buy", "stock": stock, "quantity": quantity, "price": stock_price})

    elif action == "sell":
        if stock not in portfolio["assets"] or portfolio["assets"][stock] < quantity:
            return "Insufficient stock quantity to sell.", 400
        portfolio["cash"] += cost
        portfolio["assets"][stock] -= quantity
        if portfolio["assets"][stock] == 0:
            del portfolio["assets"][stock]
        trade_history.append({"action": "sell", "stock": stock, "quantity": quantity, "price": stock_price})

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
