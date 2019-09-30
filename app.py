from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('aV+6qeP0zga7jQZyX0VCUFZXrWkNJzl/DWXDfRBAwStO40omgIJM96WsHhCWm9s5JpaCPKkj+7FpDr1jZZjLusoT21oTON4ZCU1VeFiYNLbrW/G9jYJgBSd7t+Ay6hglwDUgi4Bi99WrcSixrmk2RwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d3d12c1c071c73f304697195b1687c92')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()