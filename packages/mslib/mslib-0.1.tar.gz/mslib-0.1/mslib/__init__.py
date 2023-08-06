import math

def sharpe(returns, periods_per_year=252):
    mean_period = returns.mean()
    mean_yearly = mean_period * periods_per_year
    std_period = returns.std()
    std_yearly = std_period * math.sqrt(periods_per_year)
    sharpe = mean_yearly / std_yearly
    return sharpe