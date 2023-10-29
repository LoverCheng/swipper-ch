from django import forms

from user.models import User
from user.models import Profile


class UserForm(forms.ModelForm):
    '''User 模型的 Form'''
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'birthday', 'location']


class ProfileForm(forms.ModelForm):
    '''Profile 模型的 Form'''
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        '''清洗最大距离'''
        cleaned_data = super().clean()
        if cleaned_data['max_distance'] >= cleaned_data['min_distance']:
            return cleaned_data['max_distance']
        else:
            raise forms.ValidationError('最大距离必须大于等于最小距离')

    def clean_max_dating_age(self):
        '''清洗最大年龄'''
        cleaned_data = super().clean()
        if cleaned_data['max_dating_age'] >= cleaned_data['min_dating_age']:
            return cleaned_data['max_dating_age']
        else:
            raise forms.ValidationError('最大年龄必须大于等于最小年龄')
