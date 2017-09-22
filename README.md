This script is developed to follow the changes in a currency using Relative Strength Index (RSI). RSI is the relative strength of the current value with respect to the previous values as the name suggests. You can check how it is computed from the following website: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi. The current value of the currency is fetched from https://www.investing.com/. It is designed to send a mail to notify the user if RSI is above 70 or below 30 (These are the limits that are generally used). It requires the following parameters from the user:
* Time Period (--tp): The time period for which RSI will be computed. If it is 14, it means the RSI will be computed for the last 14 values that is fetched according to the fetch frequency.
* Currency (--curr): The currency for which the RSI will be computed. (usd-try)
* Fetch Frequency (--ff): Fetch frequency (seconds)
* Gmail User (--gu): Gmail Username
* Gmail Password (--gp): Gmail Password

For information about RSI (Relative Strength Index), you can check the following website: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi

An example command to run the script is given below below. This example fetches the currency value in every 5 minutes and compute the RSI using the last 14 values for the currency usd-try. If the RSI is lower than 30, it sends a buy alert to the given e-mail. If the RSI exceeds 70, it sends a sell alert to the given e-mail.
```
python rsi-script.py --tp 14 --curr usd-try --ff 300 --gu abc@gmail.com --gp 123456
```

Personally, I use this script on a free-tier Amazon EC2 machine as a cronjob.
