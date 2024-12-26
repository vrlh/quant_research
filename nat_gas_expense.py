from datetime import date
import pandas as pd
import math

###### TASK TWO FUNCTION #####
#inputs: in_dates, in_prices, out_dates, out_prices, rate, storage_cost_rate, total_vol, inj_withdrawal_cost_rate
#output: value (price you can sell minus price youc an buy)

#max_vol in terms of Liter
#storage price is per Liter per Day
#inj_rate in terms of LIter per day
#rate is how much you inject/withdraw per day

def contractValue(in_dates, in_prices, out_dates, out_prices, rate, storage_cost_rate, max_vol, inj_with_cost_rate):
    volume = 0
    buy_cost = 0
    cash_intake = 0

    
    all_dates = sorted(set(in_dates + out_dates))
    
    for i in range(len(all_dates)):
        curr_date = all_dates[i]

        if curr_date in in_dates and volume <= max_vol - rate:
            volume += rate
            buy_cost += (rate*inj_with_cost_rate) + rate*in_prices[in_dates.index(curr_date)]
        elif curr_date in out_dates and volume >= rate:
            volume -= rate
            cash_intake += rate*out_prices[out_dates.index(curr_date)] - (rate*inj_with_cost_rate)
        
    storage_cost = math.ceil((max(out_dates) - min(in_dates)).days // 30) * storage_cost_rate
    
    return cash_intake - buy_cost - storage_cost

in_dates = [date(2022, 1, 1), date(2022, 2, 1), date(2022, 2, 21), date(2022, 4, 1)] #injection dates
in_prices = [20, 21, 20.5, 22]#prices on the injection days
out_dates = [date(2022, 1, 27), date(2022, 2, 15), date(2022, 3, 20), date(2022, 6, 1)] # extraction dates
out_prices = [23, 19, 21, 25] # prices on the extraction days
rate = 100000  # rate of gas in cubic feet per day
storage_cost_rate = 10000  # total volume in cubic feet
injection_withdrawal_cost_rate = 0.0005  # $/cf
max_storage_volume = 500000 # maximum storage capacity of the storage facility
result = contractValue(in_dates, in_prices, out_dates, out_prices, rate, storage_cost_rate, max_storage_volume, injection_withdrawal_cost_rate)
print()
print(f"The value of the contract is: ${result}")