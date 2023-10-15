from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import os
from smtplib import SMTP

app = Flask(__name__)
bootstrap = Bootstrap5(app)
# app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
MY_EMAIL = 'p.gurungislington@gmail.com'
MY_APP_PASSWORD = os.environ.get('MY_APP_PASSWORD')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    contact_number = IntegerField('Contact Number', validators=[DataRequired()])
    service_information = TextAreaField('Service Information', validators=[DataRequired()])
    adverts_username = StringField('Adverts Username')
    submit = SubmitField('Send')


@app.route('/')
# Get all the ads in the home page.
def home():
    return render_template('index.html')


@app.route('/contact')
def contact():
    form = ContactForm()
    print(MY_EMAIL)
    print(app.secret_key)

    return render_template("contact.html", form=form)


@app.route('/contact', methods=['POST'])
def receive_data():
    form = ContactForm()
    successful_message = 'Your Inquiry has been sent. Our team will get back to you shortly.'

    sent_message = False
    if form.validate_on_submit():
        sent_message = True
        name = form.name.data
        email = form.email.data
        contact_number = form.contact_number.data
        service_information = form.service_information.data
        adverts_username = form.adverts_username.data
        sent_message = True
        # print(contact_number)
        with SMTP("smtp.gmail.com") as server:
            server.starttls()
            server.login(MY_EMAIL, "dxixvupzpjrqaxcv")
            server.sendmail(
                from_addr='p.gurungislington@gmail.com',
                to_addrs="pritamgrg47@gmail.com",
                msg=f"Subject: Client Information\n\nName: {name}\nEmail: {email}\nContact-Number: {contact_number}\nMessage: {service_information}"
            )
        return render_template('contact.html', form=form, sent_message=sent_message,
                               successful_message=successful_message, show_popup=True)


@app.route('/about')
def about():
    return render_template("about.html")


# @app.route('/clients')
# def clients():
#     clients = Client.query.all()
#     return render_template("clients_information.html", clients=clients)

@app.route('/services')
def services():
    return render_template('service.html')


if __name__ == '__main__':
    app.run(debug=True)
