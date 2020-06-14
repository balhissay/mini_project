import logging
from wt_bot import wt_bot
from flask import Flask, render_template, request

logging_level = logging.INFO

logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging_level)

# Create Flask object
app = Flask(__name__)

@app.route("/github_webhook", methods=["GET", "POST"])
def github_webhook():
    if request.method == "POST":
        logging.info(f'POST received in "/github_webhook". Sending message to WT')
        data = request.get_json()
        print(data)
        wt_bot.send_message_all_spaces("Pushed received in Github")
    else:
        pass
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)