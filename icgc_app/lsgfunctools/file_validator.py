import json, os, re 
from django.utils.html import strip_tags 
from django.core.exceptions import ValidationError


def get_to_json(post_data):  
    return json.loads(post_data[0]) if post_data else {}

def clean_text(search_term, custom=False, pattern=r"[^a-zA-Z0-9@.\s+_]+"):
    search_term = search_term.strip() # NOTE: removes with spaces in the beginning and end
    search_term = strip_tags(search_term) # NOTE: removes HTML
    
    if custom:
        search_term = re.sub(pattern,"",search_term)
        return search_term
    
    search_term = re.sub(pattern,"",search_term) # NOTE: Removes special characters
    return search_term


def file_validator_image(value):
    """
        Validates the type of image, file and size
    """
    file_size = value.size
    valid_file_extension = ['.jpg', '.png', '.jpeg', '.svg',]

    file_extension = os.path.splitext(value.name)[1] 

    file_size_kb = file_size * 0.001
    file_size_mb = file_size_kb * 0.0001 

    if not file_extension.lower() in valid_file_extension: 
        raise ValidationError("Invalid file! Valid files only: ('.jpg', '.png', '.jpeg')")

    else:
        if file_size_mb > 5: # 5MB 
            raise ValidationError("The maximum file size can be upload is 5 MB")
        else: 
            return value
 
def file_validator_pdf(value): 
    file_size = value.size
    valid_file_extension = ['.pdf',]

    file_extension = os.path.splitext(value.name)[1] 

    file_size_kb = file_size * 0.001
    file_size_mb = file_size_kb * 0.0001 

    if not file_extension.lower() in valid_file_extension: 
        raise ValidationError("Invalid file! Valid files only: ('.pdf')")

    else:
        if file_size_mb > 35: # 5MB 
            raise ValidationError("The maximum file size can be upload is 5 MB")
        else: 
            return value
 