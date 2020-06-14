import logging
import json
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
        commit_id = data.get('head_commit', {}).get('id','NA')
        commit_message = data.get('head_commit', {}).get('message', 'NA')
        commit_author = data.get('head_commit', {}).get('author', {}).get('name', 'NA')
        commit_repository = data.get('repository', {}).get('name', 'NA')
        data_text = f'Pushed received in Github: (**_{commit_message}_**) (_{commit_id}_) from **{commit_author}** to repository **{commit_repository}**'
        wt_bot.send_markdown_all_spaces(data_text)
    else:
        pass
    return "OK"

@app.route("/wt_webhook", methods=["GET", "POST"])
def wt_webhook():
    if request.method == "POST":
        logging.info(f'POST received in "/wt_webhook"')
        data = request.get_json()
        #resource = data.get('resource', 'NA')
        message_id = data.get('data', {}).get('id', '')
        #data = data.get('data', {})
        if message_id:
            message_dict = json.loads(wt_bot.get_message_details(message_id))
            #print(json.dumps(message_json, indent = 4))
            wt_bot.send_message_all_spaces(message_dict.get('text', 'NA'))
    else:
        pass
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)