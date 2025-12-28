#calculate daily interest
def daily_int(principal_amount, annual_interest_rate, duration):
    try:
        interest = (annual_interest_rate) / 100
        daily_interest = interest / 365
        daily_int_amount = principal_amount * daily_interest
        return daily_int_amount
    except Exception as e:
        print(f"Could not calculate")
        return 0