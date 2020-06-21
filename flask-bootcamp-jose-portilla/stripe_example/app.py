
from flask import Flask, render_template, request, redirect, url_for
import stripe

app = Flask(__name__)

public_key = "pk_test_51GwZ1lII6VBfjdwNPagci7I5pNzasVqolkn5Yb8BUvKxJGEbZMQEySePUHQlooef023fns22CKCK7v9LDPt0A60e00l066kgKu"

stripe.api_key = "sk_test_51GwZ1lII6VBfjdwNJeNCGTa2KzrJ176oZhxZYYHa0KOEymuUaxQ249IbTk25Vv8E8yj9Bqo4aJYk9CTPBQRqqlZJ00MhtrCryN"


@app.route('/')
def index():
    return render_template('index.html', public_key=public_key)


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@app.route('/payment', methods=['POST'])
def payment():

    # Customer Info
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # Payment Information
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999,
        currency='usd',
        description='Donation'
    )

    return redirect(url_for('thankyou'))


if __name__ == "__main__":
    app.run()
