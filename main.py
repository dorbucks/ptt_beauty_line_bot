#-*- coding: utf-8 -*
import os
from flask import Flask, request, abort, redirect
from beauty import beauty
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

app = Flask(__name__)

load_dotenv()
line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_SECRET'))

@app.route('/local_test/<name>', methods=['GET'])
def local_test(name):
    img_url = beauty.beauty_crawler(name)
    return redirect(img_url, code=302)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text

    if "find:" in message:
        name = message[5:]
        images = beauty.beauty_crawer(name)

        original_url = images
        preview_url = images
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=original_url,preview_image_url=preview_url))
        print(original_url)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()