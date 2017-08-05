# arXiv subscription script
This is to subscribe to your favourite authors and topics from arXiv.org server. 

# Usage

Edit your "list" file (see the provided example) and run in Linux shell:

python collect.py

It will collect new articles since the last time the script was launched to the new_articles file,
separated by $. You can then do whatever you want with it. Example code that posts updates via your Telegram bot
is provided in arxbot.py. Edit it to add your bot's credentials and run:

python arxbot.py

Note that it will only consider article new if it appeared on the second 
run after the query was added to the "list" file.
