from django.core.validators import EmailValidator
from rest_framework.fields import IntegerField, ChoiceField, CharField, ImageField, ListField, BooleanField, FloatField, \
    DecimalField, URLField, DateField, MultipleChoiceField, FileField, DateTimeField, JSONField, TimeField
from rest_framework.relations import PrimaryKeyRelatedField

key_map = {
    "first_name": "first name",
    "last_name": "last name",
    "contact_number": "contact number",
    "username": "email",
    "licence_number": "licence number",
    "licence_file": "licence file",
    "notary_licence_number": "notary licence number",
    "notary_licence_file": "notary licence file",
    "old_password": "old password",
    "new_password": "new password",
}


class CustomIntegerField(IntegerField):
    default_error_messages = {
        'invalid': 'A valid field_title is required.',
        'max_value': 'Ensure field_title is less than or equal to {max_value}.',
        'min_value': 'Ensure field_title is greater than or equal to {min_value}.',
        'max_string_length': 'field_title value too large.',
        'required': 'field_title is required.',
        'null': 'field_title may not be null.',
    }


class CustomCharField(CharField):
    default_error_messages = {
        'invalid': 'A valid field_title is required.',
        'blank': 'field_title may not be blank.',
        'max_length': 'Ensure field_title has no more than {max_length} characters.',
        'min_length': 'Ensure field_title has at least {min_length} characters.',
        'required': 'field_title is required.',
        'null': 'field_title may not be null.',
    }


class CustomChoiceField(ChoiceField):
    default_error_messages = {
        'invalid_choice': '"{input}" is not a valid choice in field_title.',
        'required': 'field_title is required.',
        'null': 'field_title may not be null.',
    }


class CustomMultipleChoiceField(MultipleChoiceField):
    default_error_messages = {
        'invalid_choice': '"{input}" is not a valid choice in field_title.',
        'not_a_list': 'Expected a list of items but got type "{input_type}" in field_title.',
        'empty': 'This selection may not be empty in field_title.'
    }


class CustomImageField(ImageField):
    default_error_messages = {
        'invalid_image':
            'Upload a valid image. field_title you uploaded was either not an image or a corrupted image.'
        ,
        'required': 'field_title is required.',
        'null': 'field_title may not be null.',
    }


class CustomEmailField(CustomCharField):
    default_error_messages = {
        'invalid': 'Enter a valid email address.'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validator = EmailValidator(message=self.error_messages['invalid'])
        self.validators.append(validator)


class CustomListField(ListField):
    default_error_messages = {
        'not_a_list': 'Expected a list of items in field_title but got type "{input_type}".',
        'empty': 'field_title may not be empty.',
        'min_length': 'Ensure field_title has at least {min_length} elements.',
        'max_length': 'Ensure field_title has no more than {max_length} elements.',
        'required': 'field_title is required.',
        'null': 'field_title may not be null.',
    }


class CustomBooleanField(BooleanField):
    default_error_messages = {
        'invalid': 'Must be a valid field_title.',
        'required': 'field_title is required.',
        'null': 'field_title may not be null.',
    }


class CustomFloatField(FloatField):
    default_error_messages = {
        'invalid': 'A valid field_title is required.',
        'max_value': 'Ensure field_title is less than or equal to {max_value}.',
        'min_value': 'Ensure field_title is greater than or equal to {min_value}.',
        'max_string_length': 'field_title too large.',
        'required': 'field_title is required.',
        'null': 'field_title may not be null.',
    }


class CustomDecimalField(DecimalField):
    default_error_messages = {
        'invalid': 'A field_title number is required.',
        'max_value': 'Ensure field_title is less than or equal to {max_value}.',
        'min_value': 'Ensure field_title is greater than or equal to {min_value}.',
        'max_digits': 'Ensure that in field_title are no more than {max_digits} digits in total.',
        'max_decimal_places': 'Ensure that in field_title are no more than {max_decimal_places} decimal places.',
        'max_whole_digits': 'Ensure that in field_title are no more than {max_whole_digits} digits before the decimal point.',
        'max_string_length': 'String value too large in field_title.',
        'required': 'field_title is required.',
        'null': 'field_title may not be null.',
    }


class CustomURLField(URLField):
    default_error_messages = {
        'invalid': 'Enter a valid URL in field_title.',
        'required': 'field_title is required.',
        'null': 'field_title may not be null.',
    }


class CustomPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    default_error_messages = {
        'required': 'field_title is required.',
        'does_not_exist': 'Invalid pk "{pk_value}" - object does not exist.',
        'incorrect_type': 'Incorrect type. Expected pk value, received {data_type}.',
        'null': 'field_title may not be null.',
    }


class CustomDateField(DateField):
    default_error_messages = {
        'required': 'field_title is required.',
        'invalid': 'Date has wrong format. Use one of these formats instead: {format}.',
        'datetime': 'Expected a date but got a datetime.',
        'null': 'field_title may not be null.',
    }


class CustomFileField(FileField):
    default_error_messages = {
        'required': 'No file was submitted in field_title.',
        'invalid': 'The submitted data was not a file. Check the encoding type on the form in field_title.',
        'no_name': 'No filename could be determined in field_title.',
        'empty': 'The submitted file is empty in field_title.',
        'max_length': 'Ensure this filename has at most {max_length} characters (it has {length}) in field_title.',
    }


class CustomDateTimeField(DateTimeField):
    default_error_messages = {
        'invalid': 'Datetime has wrong format. Use one of these formats instead: {format} in field_title.',
        'date': 'field_title Expected a datetime but got a date.',
        'make_aware': 'Invalid datetime for the timezone "{timezone} in field_title".',
        'overflow': 'Datetime value out of range in field_title.'
    }


class CustomUrlField(URLField):
    default_error_messages = {
        'invalid': 'Enter a valid URL.'
    }


class CustomJSONField(JSONField):
    default_error_messages = {
        'invalid': 'Value must be valid JSON in field_title.',
        'required': 'field_title field is required',
    }


class CustomTimeField(TimeField):
    default_error_messages = {
        'invalid': 'Time has wrong format in field_title. Use one of these formats instead: {format}.',
        'required': 'field_title field is required',
    }


def validate_serializers_message(errors):
    msg = []
    if isinstance(errors, dict):
        for k, v in errors.items():
            if isinstance(v, list):
                for val in v:
                    if isinstance(val, dict):
                        for ik, iv in val.items():
                            for viv in iv:
                                if isinstance(viv, dict):
                                    for xk, xv in viv.items():
                                        for xvv in xv:
                                            msg.append(xvv.replace("field_title", key_map.get(xk, xk)))
                                else:
                                    msg.append(viv.replace("field_title", key_map.get(ik, ik)))
                    else:
                        msg.append(val.replace("field_title", key_map.get(k, k)))
            else:
                for k1, v1 in v.items():
                    for val1 in v1:
                        msg.append(val1.replace("field_title", key_map.get(str(k1), str(k1))))
    else:
        for v in errors:
            if isinstance(v, list):
                for val in v:
                    for ik, iv in val.items():
                        for viv in iv:
                            msg.append(viv.replace("field_title", key_map.get(ik, ik)))

            else:
                for k1, v1 in v.items():
                    for val1 in v1:
                        if isinstance(val1, dict):
                            for xk1, xv1 in val1.items():
                                for xvv1 in xv1:
                                    msg.append(xvv1.replace("field_title", key_map.get(xk1, xk1)))
                        else:
                            msg.append(val1.replace("field_title", key_map.get(str(k1), str(k1))))

    return "|".join(msg)
