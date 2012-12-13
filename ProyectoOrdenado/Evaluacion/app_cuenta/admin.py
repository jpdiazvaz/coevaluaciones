import app_cuenta.models as models
from django.contrib import admin
from django.db.models import Model
import inspect

ms = inspect.getmembers(
    models,
    lambda c: inspect.isclass(c) and issubclass(c, Model))

for (name,m) in ms:
    admin.site.register(m)
