# Table of Contents

1.  [HFFE: High-Frequency Financial Econometrics](#org5c72cdd)
2.  [Under development](#orgff38988)
    1.  [Add citation to getRV function](#org801e9a4)
    2.  [Add citation to getBV function](#org525fa61)
    3.  [Add citation to getTOD function](#org889c509)
    4.  [Add citation to separateReturns function](#org5ca7272)


<a id="org5c72cdd"></a>

# HFFE: High-Frequency Financial Econometrics

This package implements some tools of the high-frequency financial econometrics literature.
The HFFE package provides a class \`Stock\`. This class can be used in two ways:

1.  Instantiate the class and provide stock data. The instance \`\_<sub>init</sub>\_\_\` method will automatically compute geometric returns, realized and bipower variances, and separate diffusive from jump returns using the stock data supplied.
2.  Use the class methods by themselves as needed. All of the methods in \`Stock\` are static methods and can be used without instantiating the class.

The class can be instantiated via the default constructor by supplying an iterable containing prices (floats) and an iterable containing date stamps (in the format YYYYMMDD for year, month and day). The default constructor also takes an optional iterable containing time stamps (in the format HHMM for hour and minute).
The data is assumed to be rectangular, meaning that each day contains the same number of price observations.

Prices are assumed to be observed \(N\) times per day, at the same discrete intervals. For example, if prices are sampled every 5 minutes starting from 9:30 AM and finishing at 4:00 PM, then we will have \(N=79\) price observations per day.
Prices are assumed to be observed for \(T\) total days. In each of these \(T\) days we have \(N\) price observations.
Geometric returns (log-returns) are computed for each of the days and for each of the discrete sampling intervals. However, <span class="underline">overnight returns are not considered, and the packaged only focuses on the analysis of intraday returns.</span>
If there are \(N=79\) price observations each day, then we will have \(n=78\) returns each day.

Example:

    from hffe import Stock
    from random import normalvariate as randn
    # generate some fake data
    prices = np.array([10.0 + randn(0, 1) for _ in range(10)])
    dates = ['20181112']*len(prices)
    times = [f'093{i}' for i in range(10)]
    # instantiate class
    stock = Stock(prices, dates, times)
    # at this point we can access the returns, variance measures and
    # obtain the diffusive returns separated from the jump returns
    print(f'Number of prices per day: {stock.total["prices"]}\n'
	  f'Number of days: {stock.total["days"]}')
    print(stock.returns)
    # print measures of variance
    print(f'Realized Variance: {stock.RV}\n'
	  f'Annualized Realized Variance: {(252*stock.RV)**0.5}\n'
	  f'Bipower Variance: {stock.BV}\n'
	  f'Annualized Bipower Variance: {(252*stock.BV)**0.5}')


<a id="orgff38988"></a>

# Under development


<a id="org801e9a4"></a>

## TODO Add citation to getRV function


<a id="org525fa61"></a>

## TODO Add citation to getBV function


<a id="org889c509"></a>

## TODO Add citation to getTOD function


<a id="org5ca7272"></a>

## TODO Add citation to separateReturns function
