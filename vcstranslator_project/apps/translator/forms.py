from django import forms

from translator.utils import Translator


class TranslationForm(forms.Form):
    command = forms.CharField(initial="command...")
    vcs = forms.ChoiceField(choices=[("", "Target VCS")] + zip(Translator.vcs, Translator.vcs))

    def clean_command(self):
        value = self.cleaned_data["command"]
        parts = value.split()
        if parts[0] not in Translator.vcs:
            raise forms.ValidationError("Command must start with a valid VCS (%s)." %
                ", ".join(Translator.vcs)
            )
        return value

    def translate(self):
        assert self.is_valid()
        data = self.cleaned_data
        command, rest = data["command"].split(" ", 1)
        return Translator(command.split()[0], data["vcs"]).translate(rest)
