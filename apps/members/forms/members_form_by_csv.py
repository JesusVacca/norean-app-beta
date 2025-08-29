from django import forms
class MultipleMembersByCSVForm(forms.Form):
    file_csv = forms.FileField(
        label="Archivo CSV",
        widget=forms.FileInput(attrs={'accept': '.csv, .txt'}),
    )