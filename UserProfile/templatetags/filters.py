from django import template
from datetime import datetime

register = template.Library()

# @register.simple_tag
# def dia_habil():
#     hoy = datetime.today()
#     print(hoy.weekday())
#     return hoy.weekday() < 5