from wtforms import StringField, TextAreaField, BooleanField, SelectField, IntegerField, FloatField
from wtforms import SubmitField

from wtforms import Form, StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm

class BaseForm(FlaskForm):

    cancel = SubmitField('Cancel')
    submit = SubmitField('Submit')

    def render_form(self, action: str = "") -> str:
        rows_html = ""

        for field in self:
            if field.type in ("CSRFTokenField", "SubmitField"):
                continue

            # size da 1 a 12, default 12 (piena larghezza)
            size    = field.render_kw.get("size", 12) if field.render_kw else 12
            width   = round((size / 12) * 100, 4)

            if field.type == "TextAreaField":
                input_html = str(field(class_="form-input", rows=4, placeholder=field.label.text))
            elif field.type == "BooleanField":
                input_html = f"""
                    <label class="form-checkbox">
                        {str(field(class_="form-checkbox-input"))}
                        <span>{field.label.text}</span>
                    </label>
                """
            elif field.type == "SelectField":
                input_html = str(field(class_="form-select"))
            else:
                input_html = str(field(class_="form-input", placeholder=field.label.text))

            errors_html = ""
            if field.errors:
                errors_html = f'<span class="form-error">{field.errors[0]}</span>'

            rows_html += f"""
                <div class="form-group" style="width: {width}%">
                    <label class="form-label">{field.label.text}</label>
                    {input_html}
                    {errors_html}
                </div>
            """

        submit_field = next((f for f in self if f.name == "submit"), None)
        cancel_field = next((f for f in self if f.name == "cancel"), None)

        submit_html = ""
        if cancel_field or submit_field:
            cancel_btn = str(cancel_field(class_="form-submit-btn cancel")) if cancel_field else ""
            submit_btn = str(submit_field(class_="form-submit-btn"))        if submit_field else ""
            submit_html = f"""
                <div class="form-submit">
                    {cancel_btn}
                    {submit_btn}
                </div>
            """

        return f"""
            <form method="POST" action="{action}">
                {self.hidden_tag()}
                <div class="form-container">
                    <div class="form-row">
                        {rows_html}
                    </div>
                    {submit_html}
                </div>
            </form>
        """
    # #enddef render_form

#endclass
