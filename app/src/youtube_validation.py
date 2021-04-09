from wtforms import Form, StringField, validators


class ScrapValidation(Form):
    url = StringField('url', [validators.required(),
                              validators.length(max=200)
                              ])
