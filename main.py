import csv
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['SECRET_KEY'] = "any long name"
Bootstrap5(app)


class MyForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    result = TextAreaField('Result')
    method_list = [('encode', 'Encode'), ('decode', 'Decode')]
    method = SelectField('Select Fruit', choices=method_list)
    submit = SubmitField('Submit')


@app.route("/", methods=["POST", "GET"])
def home():
    form = MyForm()
    if form.validate_on_submit():
        if form.method.data == 'encode':
            result = encode(form.message.data)
            form.result.data = result
        else:
            result = decode(form.message.data)
            form.result.data = result
    return render_template("index.html", form=form)


with open("data/morse.csv") as data:
    morse_code = {key[0]: key[1] for key in list(csv.reader(data))}


def encode(message_txt):
    code = "   ".join(morse_code.get(c.upper(), c) for c in message_txt)
    return code


def decode(code_txt):
    result = ""
    for d in code_txt.split("   "):
        if d in morse_code.values():
            for key, value in morse_code.items():
                if d == value:
                    result += key

        else:
            result += d
    return result


if __name__ == "__main__":
    app.run(debug=True)

