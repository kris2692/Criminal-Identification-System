# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 15:29:12 2018

@author: krish
"""

from django.forms import ModelForm
from .models import Details

class DetailForm(ModelForm):
  class Meta:
    model=Details
    fields=['name','description','location','date']

form=DetailForm()