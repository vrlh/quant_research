import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

#sin func
def sine(x, A, B, C, D, E):
    return A * np.sin(B*x + C) + D + E*x

#reads and plots the data:

df = pd.read_csv('Nat_Gas.csv')

df['Dates'] = pd.to_datetime(df['Dates'])
df['Dates_seconds'] = (df['Dates'] - df['Dates'].min()).dt.total_seconds()



y = df['Prices']
x = df['Dates_seconds'].values.reshape(-1,1)

#plt.plot(df['Dates'], y, linestyle='-', color='b', label='Price over time')

plt.xlabel('Dates')
plt.ylabel('Prices')

#adds a line over the data to see a general trend

linModel = LinearRegression()
linModel.fit(x, y)


y_lin = linModel.predict(x)

#plt.plot(df['Dates'], y_lin, linestyle='-', color='r', label='Regressed line')


#sin funciton fitting

f_cubic = interp1d(x.flatten(), y, kind='cubic') #model interpolates points

x_interp = np.linspace(x.min(), x.max(), 1000)
y_interp = f_cubic(x_interp) #interpolation 

dates_interp = pd.to_datetime(df['Dates'].min()) + pd.to_timedelta(x_interp, unit='s')

#plt.plot(dates_interp, y_interp, linestyle='-', color='b', label='interpolated')


from scipy.fft import fft, fftfreq
y_detrended = y - linModel.predict(x)  # Remove linear trend
y_fft = np.fft.fft(y_detrended)
freq = np.fft.fftfreq(len(x), (x.max() - x.min())/(len(x)-1))
dominant_freq = 2 * np.pi * abs(freq[np.argmax(np.abs(y_fft[1:]))+1])

# bounds = (
#     [0, dominant_freq/2, -2*np.pi, min(y_interp), -np.inf],  # Lower bounds
#     [max(y_interp)-min(y_interp), 0.5, 2*np.pi, max(y_interp), np.inf]  # Upper bounds
# )


init_guess = [(max(y_interp) - min(y_interp))/2,  
              dominant_freq, 
              0, 
              np.mean(y_interp),
              linModel.coef_[0]]

params, covariance = curve_fit(sine, x_interp, y_interp, p0=init_guess, maxfev=10000)

y_sin = sine(x_interp, *params)

#plt.plot(dates_interp, y_sin, linestyle='-', color='g', label='Sin Wave')


#predicted values

x_exterp = np.linspace(x.max(), 2*x.max(), 1000)
dates_exterp = pd.to_datetime(df['Dates'].min()) + pd.to_timedelta(x_exterp, unit='s')

y_sin_exterp = sine(x_exterp, *params)

# plt.plot(dates_exterp, y_sin_exterp, linestyle='-', color='g')

# y_lin_exterp = linModel.predict(x_exterp.reshape(-1, 1))
# plt.plot(dates_exterp, y_lin_exterp, linestyle = '-', color='r')

# plt.legend()
# plt.grid(True)
# plt.gcf().autofmt_xdate() 

# plt.show()

###### TASK ONE FUNCTION ######
#input: date
#output: projected price


date = input("Enter date in format YYYY-MM-DD ")

def predict_price(input_date):
    input_date = pd.to_datetime(input_date)
    input_seconds = (input_date - df['Dates'].min()).total_seconds()

    return sine(input_seconds, *params)
print(predict_price(date))


