from django import forms
from .models import Mentoria
from django.contrib.auth.models import User

PREGUNTAS = [
    ("pregunta1", "Me gusta trabajar en equipo"),
    ("pregunta2", "Disfruto resolver problemas complejos"),
    ("pregunta3", "Prefiero tareas prácticas y manuales"),
    ("pregunta4", "Me interesan los temas científicos"),
    ("pregunta5", "Me gusta ayudar a otras personas"),
]

OPCIONES = [(i, str(i)) for i in range(1, 6)]  # Escala 1 a 5

class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for clave, texto in PREGUNTAS:
            self.fields[clave] = forms.ChoiceField(
                label=texto,
                choices=OPCIONES,
                widget=forms.RadioSelect
            )

class IkigaiForm(forms.Form):
    ama_1 = forms.CharField(
        label="¿Qué actividad disfrutas tanto que perderías la noción del tiempo?",
        widget=forms.Textarea(attrs={'rows': 2})
    )
    ama_2 = forms.CharField(
        label="¿Qué harías gratis toda la vida si pudieras?",
        widget=forms.Textarea(attrs={'rows': 2})
    )

    bueno_1 = forms.CharField(
        label="¿En qué actividades te sientes competente o talentoso?",
        widget=forms.Textarea(attrs={'rows': 2})
    )
    bueno_2 = forms.CharField(
        label="¿Qué te dicen los demás que haces bien?",
        widget=forms.Textarea(attrs={'rows': 2})
    )

    pagado_1 = forms.CharField(
        label="¿Por qué habilidades o conocimientos te han pagado o podrían pagarte?",
        widget=forms.Textarea(attrs={'rows': 2})
    )
    pagado_2 = forms.CharField(
        label="¿Qué servicios podrías ofrecer profesionalmente?",
        widget=forms.Textarea(attrs={'rows': 2})
    )

    necesario_1 = forms.CharField(
        label="¿Qué problemas sociales o globales te gustaría resolver?",
        widget=forms.Textarea(attrs={'rows': 2})
    )
    necesario_2 = forms.CharField(
        label="¿Qué causa te motiva profundamente?",
        widget=forms.Textarea(attrs={'rows': 2})
    )

class MentoriaForm(forms.ModelForm):
    class Meta:
        model = Mentoria
        fields = ['mentor', 'fecha', 'hora', 'mensaje']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        mentor = cleaned_data.get('mentor')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if mentor and fecha and hora:
            conflicto = Mentoria.objects.filter(
                mentor=mentor,
                fecha=fecha,
                hora=hora
            ).exists()

            if conflicto:
                raise forms.ValidationError(
                    "Este mentor ya tiene una mentoría agendada en esa fecha y hora."
                )
        usuario = self.initial.get('usuario')
        if usuario:
            ya_agendada = Mentoria.objects.filter(
                usuario=usuario,
                mentor=mentor,
                fecha=fecha,
                hora=hora
            ).exists()
            if ya_agendada:
                raise forms.ValidationError("Ya has agendado con este mentor en ese horario.")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']