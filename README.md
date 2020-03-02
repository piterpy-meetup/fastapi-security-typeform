# fastapi-security-typeform

Security plugin for [FastAPI](https://github.com/tiangolo/fastapi) which allows you check 
[Typeform signature](https://developer.typeform.com/webhooks/secure-your-webhooks/) in your webhook endpoint. 

## How to setup signing flow for your typeform webhook

**Current flow** is here https://developer.typeform.com/webhooks/secure-your-webhooks/ 
(it's little bit a lie about `working only via API`)

tl;dr:
 * create a webhook via UI or API
 * generate random string (secret)
 * update a webhook via UI or API with your secret
 


## How to use

Use pip or another package management util:
```bash
pip install fastapi-security-typeform
```

or

```bash
poetry add fastapi-security-typeform
```

or

```bash
pipenv install fastapi-security-typeform
```

Then initialize it with your webhook secret and pass it to endpoint as dependency.

It will raise 403 error if signature isn't valid.

```python
from fastapi import Depends, FastAPI

from fastapi_security_typeform import SignatureHeader

app = FastAPI()
signature_header_security = SignatureHeader(secret=b'{your_secret}')

@app.post("/typeform_webhook")
def typeform_webhook(signature = Depends(signature_header_security)):
    ...
    return {"success": True}

```
