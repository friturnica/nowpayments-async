# nowpayments-async
  Asynchronous API wrapper for working with NowPayments API
 
  Usage:
  ```python
  payments = nowpayments.NowPayments("your api_key")
  status = await payments.get_status()
  print(status)
  ```
