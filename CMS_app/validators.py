from django.core.exceptions import ValidationError

def only_digit(value): 
    if value.isdigit()==False:
        raise ValidationError('ID contains characters')
