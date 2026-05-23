"""
GTR Bank Payment Gateway Integration
Handles deposit processing and verification
"""

import requests
import json
from datetime import datetime

class GTRBankService:
    def __init__(self):
        # GTR Bank API Configuration
        self.base_url = "https://gtrbank.com/gtr_api/api"
        self.api_key = "YOUR_GTR_API_KEY"  # Replace with actual API key
        self.merchant_id = "YOUR_MERCHANT_ID"  # Replace with actual merchant ID
        
    def initiate_payment(self, amount, email, phone, name, reference=None):
        """
        Initiate payment with GTR Bank
        Amount should be in Naira (e.g., 3000 for ₦3,000)
        """
        try:
            # Convert amount to kobo (multiply by 100)
            amount_in_kobo = int(float(amount) * 100)
            
            if not reference:
                reference = f"GTR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{email.split('@')[0]}"
            
            payload = {
                "api_key": self.api_key,
                "merchant_id": self.merchant_id,
                "amount": amount_in_kobo,  # Amount in kobo
                "email": email,
                "phone": phone,
                "name": name,
                "reference": reference,


代收请求地址：https://api.nekpayment.com/pay/web
===========================================================================

请求方式：POST
=========

| 国家 | 测试商户号 | 二类通道编码(pay\_type) | 代收密钥 |
| --- | --- | --- | --- |
| 尼日利亚 | 999300111 | 尼日利亚二类A=520 | e8a4cdd0ccdb4d2b9ca6212453c5e40c |

*   注：测试完毕后更换正式商户号和代收秘钥，即可进入正式环境
*   注：正式商户号的代收秘钥和通道编码(pay\_type)在商户后台首页查看

### Header：

| 参数名 | 必选 | 类型 | 说明 |
| --- | --- | --- | --- |
| Content-Type | 是 | string | application/x-www-form-urlencoded |

代收请求参数
======

| 参数值 | 参数名 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| version | 版本号 | String | Y | 固定值 “1.0” |
| mch\_id | 商户号 | String | Y | 平台分配唯一 |
| notify\_url | 后台通知地址 | String | Y | 不超过 200 字节 |
| page\_url | 前台通知地址 | String | N | 不超过 200 字节 |
| mch\_order\_no | 商家订单号 | String | Y | 保证每笔订单唯一 |
| pay\_type | 支付类型 | String | Y | 请查阅商户后台通道编码 |
| trade\_amount | 交易金额 | String | Y | 最多2位小数 |
| order\_date | 订单时间 | String | Y | 时间格式： yyyy-MM-dd HH:mm:ss |
| bank\_code | 银行代码 | String | Y | 填写固定值：NGR044 |
| goods\_name | 商品名称 | String | Y | 不超过 50 字节 |
| mch\_return\_msg | 透传参数 | String | N | 不超过200字节，不可提交空值 |
| sign\_type | 签名方式 | String | Y | 固定值 MD5，不参与签名 |
| sign | 签名 | String | Y | 不参与签名 |

*   代收请求参数：（以post表单方式请求，且参数的值不可以为空）

    goods_name=test, 
    mch_id=977977001,
    mch_order_no=WE123456789, 
    mch_return_msg=test, 
    notify_url=http://www.baidu.com, 
    order_date=2021-11-11 11:11:11,
    page_url=https://wwww.baidu.com, 
    pay_type=122, 
    sign=3cf44d27eb41696938d80135ef6af98b,
    sign_type=MD5, 
    trade_amount=100, 
    version=1.0
    

*   请求参数签名串：

goods\_name=test&mch\_id=977977001&mch\_order\_no=WE123456789&mch\_return\_msg=test&notify\_url=[http://www.baidu.com&order\_date=2021-11-11](http://www.baidu.com&order_date=2021-11-11/) 11:11:11&page\_url=[https://wwww.baidu.com&pay\_type=122&trade\_amount=100&version=1.0&key=520261072ab44e05a475697960941f69](https://wwww.baidu.com&pay_type=122&trade_amount=100&version=1.0&key=520261072ab44e05a475697960941f69/)

代收同步响应（返回 json 数据）
==================

| 参数值 | 参数名 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| respCode | 响应状态 | String | Y | SUCCESS：响应成功,FAIL:响应失败 |
| tradeMsg | 响应失败原因 | String | Y | 响应成功时为 request success |
| 以下参数只有响应成功respCode为SUCCESS才有值 |
| signType | 签名方式 | String | Y | MD5 不参与签名 |
| sign | 签名 | String | Y | 不参与签名 |
| mchId | 商户号 | String | Y | 商户号 |
| mchOrderNo | 商家订单号 | String | Y | 商家订单号 |
| oriAmount | 实际金额 | String | Y | 实际金额，与订单金额一致 |
| tradeAmount | 订单金额 | String | Y | 订单金额 |
| orderDate | 订单时间 | String | Y | 订单时间 |
| orderNo | 平台转账单号 | String | Y | 平台转账单号 |
| tradeResult | 下单状态 | String | Y | 1下单成功，其他失败 |
| payInfo | 付款链接 | String | Y | 付款链接 |

*   同步响应JSON参数：
    
        "signType":"MD5",
        "sign":"00deafedf32acb0baf23c061db258405",
        "respCode":"SUCCESS",
        "tradeResult":"1",
        "tradeMsg":"test",
        "mchId":"977977001",
        "mchOrderNo":"WE123456789",
        "oriAmount":"100",
        "tradeAmount":"100",
        "orderDate":"2021-11-11 11:11:11",
        "orderNo":"300001033",
        "payInfo":"https://www.baidu.com"
        
    

代收异步通知消息(以post的form形式(返回数据)
===========================

#### 1：订单支付成功，发送异步支付成功通知

#### 2：商户未收到通知，系统会连续补发通知8 次

#### 3：商户收到异步通知，需向平台返回“success”终止补发

| 参数值 | 参数名 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| tradeResult | 订单状态 | String | Y | 1：支付成功 |
| mchId | 商户号 | String | Y |
| mchOrderNo | 商家订单号 | String | Y |
| oriAmount | 原始订单金额 | String | Y | 商家上传的订单金额 |
| amount | 交易金额 | String | Y | 实际支付金额 |
| orderDate | 订单时间 | String | Y |
| orderNo | 平台支付订单号 | String | Y |
| merRetMsg | 透传参数 | String | N | 下单时未提交则无需参与签名 |
| signType | 签名方式 | String | Y | 不参与签名 |
| sign | 签名 | String | Y | 不参与签名 |

*   异步通知内容 (以post表单形式返回)

    "tradeResult":"1",
    "oriAmount":"100.00",
    "amount":"100.00",
    "mchId":"977977001",
    "orderNo":"300001033",
    "mchOrderNo":"WE123456789",
    "merRetMsg":"test",
    "sign":"da4e275be34024dfe817268c5be6c70b",
    "signType":"MD5",
    "orderDate":"2021-11-11 11:11:11"
    

*   异步响应签名验证源串形式：

amount=100.00&mchId=977977001&mchOrderNo=WE123456789&merRetMsg=test&orderDate=2021-11-11 11:11:11&orderNo=300001033&oriAmount=100.00&tradeResult=1&key=520261072ab44e05a475697960941f69                "callback_url": "https://yoursite.com/gtr-payment-callback",  # Use your public Vercel domain here
                "return_url": "https://yoursite.com/dashboard"  # Use your public Vercel domain here
            }
            
            response = requests.post(
                f"{self.base_url}/payment/initialize",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'success': True,
                        'payment_url': data.get('data', {}).get('payment_url'),
                        'reference': reference,
                        'amount': amount,
                        'amount_kobo': amount_in_kobo
                    }
            
            return {
                'success': False,
                'error': f'Payment initialization failed: {response.text}',
                'status_code': response.status_code
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def verify_payment(self, reference):
        """
        Verify payment status with GTR Bank
        """
        try:
            payload = {
                "api_key": self.api_key,
                "merchant_id": self.merchant_id,
                "reference": reference
            }
            
            response = requests.post(
                f"{self.base_url}/payment/verify",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'data': data,
                    'status': data.get('data', {}).get('status'),
                    'amount': data.get('data', {}).get('amount', 0) / 100,  # Convert back to Naira
                    'reference': reference
                }
            
            return {
                'success': False,
                'error': f'Verification failed: {response.text}',
                'status_code': response.status_code
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }

# Create global instance
gtr_service = GTRBankService()
