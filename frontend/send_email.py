from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_html_email(subject, html_template, context, to_email):
    # Render the HTML content using a Django template
    html_content = render_to_string(html_template, context)

    # Create a text content by stripping the HTML tags
    text_content = strip_tags(html_content)
    
    # Create the EmailMessage object
    email = EmailMessage(subject, text_content, to=[to_email])
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send()
