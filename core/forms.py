# core/forms.py
from django import forms
from django.contrib.contenttypes.models import ContentType
from core.models import Caixa, Pessoa, Grupo

class CaixaForm(forms.ModelForm):
    origin_content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(app_label='core', model__in=['pessoa', 'grupo']),
        required=False,
        label="Tipo de Origem"
    )
    # Em vez de queryset=None, use um queryset vazio a partir de um model, por exemplo, Pessoa.objects.none()
    origin_object = forms.ModelChoiceField(
        queryset=Pessoa.objects.none(),
        required=False,
        label="Origem"
    )

    class Meta:
        model = Caixa
        fields = ['descricao', 'origin_content_type', 'origin_object', 'valor', 'tipo']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da transação'}),
            'valor': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Valor'}),
            'tipo': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(CaixaForm, self).__init__(*args, **kwargs)
        # Se houver um POST ou GET com valor para origin_content_type, popula o origin_object
        if self.data.get('origin_content_type'):
            try:
                ct_id = int(self.data.get('origin_content_type'))
                content_type = ContentType.objects.get_for_id(ct_id)
                model_label = content_type.model
                if model_label == 'pessoa':
                    self.fields['origin_object'].queryset = Pessoa.objects.all()
                elif model_label == 'grupo':
                    self.fields['origin_object'].queryset = Grupo.objects.all()
                else:
                    # Define o queryset como vazio usando .none() em um queryset válido
                    self.fields['origin_object'].queryset = Pessoa.objects.none()
            except (ValueError, ContentType.DoesNotExist):
                self.fields['origin_object'].queryset = Pessoa.objects.none()
        else:
            self.fields['origin_object'].queryset = Pessoa.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        content_type = cleaned_data.get('origin_content_type')
        origin_object = cleaned_data.get('origin_object')
        if (content_type and not origin_object) or (origin_object and not content_type):
            raise forms.ValidationError("Para definir a origem, selecione tanto o tipo quanto o objeto de origem.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        origin_object = self.cleaned_data.get('origin_object')
        if origin_object:
            instance.origin_object_id = origin_object.pk
            instance.origin_content_type = ContentType.objects.get_for_model(origin_object)
        if commit:
            instance.save()
        return instance
