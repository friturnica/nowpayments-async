import aiohttp

class NowPayments:
    MAIN_URL = "https://api.nowpayments.io/v1"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    
    def urljoin(self, *args) -> str:
        return "/".join(map(lambda x: str(x).rstrip("/"), args))


    async def _make_request(self, method: str, path: str, params: dict = None, data: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, 
                self.urljoin(self.MAIN_URL, path), 
                headers={
                    "x-api-key": self.api_key
                },
                json=data,
                params=params
            ) as response:
                return await response.json()
    

    async def get_status(self) -> dict:
        return await self._make_request("get", "status")

    
    async def get_currencies(self) -> dict:
        return await self._make_request("get", "currencies")

    
    async def get_full_currencies(self) -> dict:
        return await self._make_request("get", "full_currencies")

    
    async def get_coins(self) -> dict:
        return await self._make_request("get", "merchant/coins")
    

    async def get_estimated_price(self, amount: float, currency_from: str, currency_to: str) -> dict:
        params = {
            "amount": amount,
            "curreny_from": currency_from,
            "currency_to": currency_to
        }
        return await self._make_request("get", "estimate", params=params)
    

    async def create_payment(
        self, 
        price_amount: float, 
        pay_currency: str, 
        price_currency: str = "usd", 
        pay_amount: int = None, 
        ipn_callback_url: str = None, 
        order_id: str = None,
        order_description: str = None,
        purchase_id: int = None,
        payout_address: int = None,
        payout_currency: str = None,
        payout_extra_id: str = None,
        fixed_rate: bool = None
    ):
        data = {
            "price_amount": price_amount,
            "price_currency": price_currency,
            "pay_currency": pay_currency,
        }

        if pay_amount is not None:
            data["pay_amount"] = pay_amount

        if ipn_callback_url is not None:
            data["ipn_callback_url"] = ipn_callback_url

        if order_id is not None:
            data["order_id"] = order_id

        if order_description is not None:
            data["order_description"] = order_description

        if purchase_id is not None:
            data["purchase_id"] = purchase_id

        if payout_address is not None:
            data["payout_address"] = payout_address

        if payout_currency is not None:
            data["payout_currency"] = payout_currency

        if payout_extra_id is not None:
            data["payout_extra_id"] = payout_extra_id

        if fixed_rate is not None:
            data["fixed_rate"] = fixed_rate
        
        return await self._make_request("post", "payment", data=data)
    

    async def get_payment_status(self, payment_id: int):
        return await self._make_request("get", f"payment/{payment_id}")

    
    async def get_minimum_payment_amount(self, currency_from: str, currency_to: str):
        params = {
            "currency_from": currency_from,
            "currency_to": currency_to
        }
        return await self._make_request("get", "min-amount", params=params)


    async def get_payments_list(self, limit: int = 10, page: int = 0, sort_by: str = "created_at", order_by: str = "asc", date_from: str = "", date_to: str = ""):
        params = {
            "limit": limit,
            "page": page,
            "sort_by": sort_by,
            "order_by": order_by,
            "date_from": date_from,
            "date_to": date_to
        }
        return await self._make_request("get", "payment", params=params)
    

    async def create_invoice(
        self, 
        price_amount: int, 
        price_currency: str = "usd", 
        pay_currency: str = None, 
        ipn_callback_url: str = None, 
        order_id: str = None, 
        order_description: str = None, 
        success_url: str = None, 
        cancel_url: str = None
    ):
        data = {
            "price_amount": price_amount,
            "price_currency": price_currency
        }

        if pay_currency is not None:
            data["pay_currency"] = pay_currency

        if ipn_callback_url is not None:
            data["ipn_callback_url"] = ipn_callback_url
        
        if order_id is not None:
            data["order_id"] = order_id
        
        if order_description is not None:
            data["order_description"] = order_description
        
        if success_url is not None:
            data["success_url"] = success_url
        
        if cancel_url is not None:
            data["cancel_url"] = cancel_url
        
        return await self._make_request("post", "invoice", data=data)


async def main():
    payments = NowPayments("your api_key")
    status = await payments.get_status()
    print(status)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    
    