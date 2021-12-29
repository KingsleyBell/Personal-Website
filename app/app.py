from datetime import datetime
import random

from flask import Flask, render_template

from auth import requires_auth
from settings import INPUT_FILE_PATH

# the all-important app variable:
application = Flask(__name__)


@application.route('/')
def hello():
    return render_template('index.html', now=datetime.utcnow())


def wallet(fake=False):
    balances = []
    btc_balances = []
    zar_balances = []
    with open(INPUT_FILE_PATH, 'r') as wallet_file:
        if fake:
            multiplier = random.random() * random.randrange(1, 3)
        for line in wallet_file:
            line = line.split('root:')[1]
            date = line.split('|')[0].split(' ')[0] + ' '
            amounts = line.split('|')[1:]
            btc_amount = float(amounts[0].split(' ')[-2])
            zar_amount = float(amounts[1].split(' ')[-1][1:-1])

            if fake:
                btc_amount = round(btc_amount * multiplier, 3)
                zar_amount = round(zar_amount * multiplier, 3)

            btc_balances.append([date, btc_amount])
            zar_balances.append([date, zar_amount])
            balances.append(' .  '.join([f'Date: {date}', f'BTC: {btc_amount}', f'ZAR: {zar_amount}']))

    return render_template(
        'wallet.html',
        balances=reversed(balances),
        btc_balances=btc_balances,
        zar_balances=zar_balances,
        btc_diff=round(btc_balances[-1][1] - btc_balances[-2][1], 5),
        zar_diff=round(zar_balances[-1][1] - zar_balances[-2][1], 5),
        now=datetime.utcnow()
    )


# @application.route('/wallet')
# @requires_auth
# def wallet_real():
#     return wallet()
#
#
# @application.route('/wallet-fake')
# def wallet_fake():
#     return wallet(fake=True)


@application.route('/resume')
def resume():
    return application.send_static_file('pdf/Resume.pdf')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=800)
