from django import forms
from .models import Transaction, Category



class TransactionForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.RadioSelect())
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be positive")
        return amount

    
    class Meta:
        model = Transaction
        fields = ('date', 'type', 'amount', 'category')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
           
  
        }