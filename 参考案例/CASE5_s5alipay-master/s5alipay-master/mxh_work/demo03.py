import json
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    data = request.form.to_dict()
    # sign must be poped out
    signature = data.pop("sign")

    print(json.dumps(data))
    print(signature)

    # verify
    success = alipay.verify(data, signature)
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED" ):
        print("trade succeed")
    return 'Hello, World!'