import logging
import json
import re
from wt_bot import wt_bot
import spotify_util
from flask import Flask, render_template, request, url_for

logging_level = logging.INFO

logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging_level)

# Create Flask object
app = Flask(__name__)

@app.route("/github_webhook", methods=["GET", "POST"])
def github_webhook():
    if request.method == "POST":
        logging.info(f'POST received in "/github_webhook". Sending message to WT')
        data = request.get_json()
        if 'commits' in data or 'head_commit' in data:
            commit_id = data.get('head_commit', {}).get('id','NA')
            commit_message = data.get('head_commit', {}).get('message', 'NA')
            commit_author = data.get('head_commit', {}).get('author', {}).get('name', 'NA')
            commit_repository = data.get('repository', {}).get('name', 'NA')
            data_text = f'Pushed received in Github: (**_{commit_message}_**) (_{commit_id}_) from **{commit_author}** to repository **{commit_repository}**'
        elif data.get('ref_type') == "tag":
            data_text = f"Tag created in Github: **_{data.get('ref', 'NA')}_** from **{data.get('sender',{}).get('login', 'NA')}** on repository **{data.get('repository', {}).get('name', 'NA')}**"
        else:
            data_text = "Unknown event in Github"
            with open("github_webhook_data.json", "w") as file:
                file.write(json.dumps(data, indent = 4))
        wt_bot.send_markdown_all_spaces(data_text)
    else:
        pass
    return "OK"

@app.route("/wt_webhook", methods=["GET", "POST"])
def wt_webhook():
    if request.method == "POST":
        logging.info(f'POST received in "{url_for("wt_webhook")}"')
        data = request.get_json()
        #spotify_util.jprint(data)
        resource = data.get('resource', 'NA')
        if resource == 'messages':
            message_id = data.get('data', {}).get('id', '')
            if message_id:
                message_dict = json.loads(wt_bot.get_message_details(message_id))
                text = message_dict.get('text', 'NA')
                final_text = re.sub(rf"^{wt_bot.bot_info.get('bot_name')}\s+", "", text)
                #person_id = message_dict.get('personId', '')
                person_email = message_dict.get('personEmail', '')
                context = wt_bot.filter_message(final_text)
                if context == "spotify":
                    response = spotify_util.spotify_message(final_text, person_email)
                    wt_bot.send_message_several_spaces([message_dict.get('roomId')], response)
                else:
                    wt_bot.send_message_several_spaces([message_dict.get('roomId')], final_text*5)
            else:
                logging.error('Message received without ID')
        else:
            logging.error('A new resource has been received')
    else:
        pass
    return "OK"

@app.route("/spotify_callback", methods=["GET"])
def spotify_callback():
    logging.info(f'GET received in "{url_for("spotify_callback")}"')
    code = request.args.get('code')
    if code:
        spotify_util.get_token_from_code(code)
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)