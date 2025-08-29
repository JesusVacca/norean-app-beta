from django import forms
from django.utils.safestring import mark_safe


class CustomForm:
    def as_custom(self):
        self.__load_default_style()
        html = ''
        for name, field in self.fields.items():
            errors = self.errors.get(name)
            error_html = ''
            if errors:
                error_html =f'<span class="form__error">{errors[0]}</span>'
            html +=f'''
                <div class="form__group">
                    <label 
                        class="form__label" 
                        for="{self[name].id_for_label}"
                        data-required="{str(field.required).lower()}"
                        >
                            {field.label}
                        </label>
                    {self[name]}
                    {error_html}
                </div>
            '''
        return mark_safe(html)
    def __load_default_style(self):
        for name, field in self.fields.items():
            css_classes = field.widget.attrs.get('class', '')
            css_classes += 'form__input'
            if self.errors.get(name):
                css_classes += ' form__input-error'
            field.widget.attrs['class'] = css_classes.strip()

class BaseModelForm(forms.ModelForm, CustomForm):
    pass


class BaseForm(forms.Form, CustomForm):
    pass