import os

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

from .models import User, Exhibit, ExhibitPicture, UserLang


VALID_EXTENSIONS = ['.jpg', '.jpeg']


class ExhibitForm(forms.ModelForm):

    class Meta:
        model = Exhibit
        fields = ('exhibit_name', 'exhibit_desc', 'exhibit_name_en', 'exhibit_desc_en', 'exhibit_name_zh', 'exhibit_desc_zh')
        widgets = {
            'exhibit_name': forms.TextInput(attrs={'id': 'exhibit_name', 'class': 'form-control', 'placeholder': '名称を入力'}),
            'exhibit_desc': forms.Textarea(attrs={'id': 'exhibit_desc', 'class': 'form-control', 'rows': '5'}),
            'exhibit_name_en': forms.TextInput(attrs={'id': 'exhibit_name_en', 'class': 'form-control', 'placeholder': '名称を入力'}),
            'exhibit_desc_en': forms.Textarea(attrs={'id': 'exhibit_desc_en', 'class': 'form-control', 'rows': '5'}),
            'exhibit_name_zh': forms.TextInput(attrs={'id': 'exhibit_name_zh', 'class': 'form-control', 'placeholder': '名称を入力'}),
            'exhibit_desc_zh': forms.Textarea(attrs={'id': 'exhibit_desc_zh', 'class': 'form-control', 'rows': '5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exhibit_name'].required = False
        self.fields['exhibit_desc'].required = False
        self.fields['exhibit_name_en'].required = False
        self.fields['exhibit_desc_en'].required = False
        self.fields['exhibit_name_zh'].required = False
        self.fields['exhibit_desc_zh'].required = False

    def clean_exhibit_name(self):
        """各フィールドごとのバリデーション処理"""
        exhibit_name = self.cleaned_data['exhibit_name']
        if len(exhibit_name) >= 60:
            raise forms.ValidationError("60文字以内で入力してください。")
        return exhibit_name

    def clean_exhibit_desc(self):
        exhibit_desc = self.cleaned_data['exhibit_desc']
        if len(exhibit_desc) >= 2000:
            raise forms.ValidationError("2000文字以内で入力してください。")
        return exhibit_desc

    def clean_exhibit_name_en(self):
        exhibit_name_en = self.cleaned_data['exhibit_name_en']
        if len(exhibit_name_en) >= 140:
            raise forms.ValidationError("140文字以内で入力してください。")
        return exhibit_name_en

    def clean_exhibit_desc_en(self):
        exhibit_desc_en = self.cleaned_data['exhibit_desc_en']
        if len(exhibit_desc_en) >= 2500:
            raise forms.ValidationError("2500文字以内で入力してください。")
        return exhibit_desc_en

    def clean_exhibit_name_zh(self):
        exhibit_name_zh = self.cleaned_data['exhibit_name_zh']
        if len(exhibit_name_zh) >= 100:
            raise forms.ValidationError("100文字以内で入力してください。")
        return exhibit_name_zh

    def clean_exhibit_desc_zh(self):
        exhibit_desc_zh = self.cleaned_data['exhibit_desc_zh']
        if len(exhibit_desc_zh) >= 2000:
            raise forms.ValidationError("2000文字以内で入力してください。")
        return exhibit_desc_zh

    def clean(self):
        """複数フィールド間のバリデーション相関処理（データベースの整合性etc）"""
        super().clean()
        # name = self.cleaned_data.get('exhibit_name')
        # desc = self.cleaned_data.get('exhibit_desc')

        # if name == desc:
        #     raise forms.ValidationError("名称と説明文が同じです。")


class ExhibitPictureForm(forms.ModelForm):

    # 複数の画像ファイルを選択可能
    post_pic = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input upload-portfolio-image', 'multiple': True, 'style': 'display:none;'}),
    )

    class Meta:
        model = ExhibitPicture
        fields = ('post_pic',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_pic'].required = False

    # def clean_post_pic(self):
    #     image = self.cleaned_data['post_pic']
    #     extension = os.path.splitext(image)[1]
    #     if not extension.lower() in VALID_EXTENSIONS:
    #         raise forms.ValidationError("jpgファイルをアップロードしてください")
    #     return image


class ContactForm(forms.Form):
    contact_title = forms.CharField(
        label='お問い合わせ件名',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '件名を入力'})
    )

    contact_content = forms.CharField(
        label='お問い合わせ内容',
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'お問い合わせ内容を入力'})
    )


# Singup
class SignupForm(UserCreationForm):
    """User registration"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'username-create-form'}),
            'email': forms.EmailInput(attrs={'class': 'email-create-form'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        # TODO: Emailの形式をチェックする処理
        # 仮登録でemailを登録している場合に削除処理をする
        User.objects.filter(email=email, is_active=False).delete()
        return email


class UserEditForm(forms.ModelForm):

    thumbnail = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'user-thumbnail-input upload-user-image'}),
    )

    class Meta:
        model = User
        fields = ('username', 'thumbnail', 'self_intro', 'major_category', 'address_prefecture', 'address_city', 'address_street', 'latitude', 'longitude', 'telephone', 'url', 'entrance_fee', 'business_hours', 'holiday')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'obj_username', 'placeholder': '名称を入力'}),
            'self_intro': forms.Textarea(attrs={'class': 'obj_self_intro', 'rows': '7', 'placeholder': '紹介文を入力'}),
            'major_category': forms.Select(attrs={'class': ''}),
            'address_prefecture': forms.TextInput(attrs={'class': 'add_pre', 'placeholder': '※東京都'}),
            'address_city': forms.TextInput(attrs={'class': 'add_city', 'placeholder': '※渋谷区代々木神園町'}),
            'address_street': forms.TextInput(attrs={'class': 'add_street', 'placeholder': '※1-1-5'}),
            'latitude': forms.TextInput(attrs={'id': 'latitude', 'class': '', 'placeholder': '緯度'}),
            'longitude': forms.TextInput(attrs={'id': 'longitude', 'class': '', 'placeholder': '経度'}),
            'telephone': forms.TextInput(attrs={'class': '', 'placeholder': '0312345678'}),
            'url': forms.TextInput(attrs={'class': '', 'placeholder': 'https://www.'}),
            'entrance_fee': forms.TextInput(attrs={'class': '', 'placeholder': '大人: 1300円、子供: 800円'}),
            'business_hours': forms.TextInput(attrs={'class': '', 'placeholder': '10:00 ~ 19:00'}),
            'holiday': forms.TextInput(attrs={'class': '', 'placeholder': '毎週火曜日'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] += ' form-control'
            field.required = False


class UserLangEditForm(forms.ModelForm):
    class Meta:
        model = UserLang
        fields = ('language', 'username', 'self_intro', 'address_prefecture', 'address_city', 'address_street', 'entrance_fee', 'business_hours', 'holiday')
        widgets = {
            'language': forms.Select(attrs={'class': 'userlang_laguage'}),
            'username': forms.TextInput(attrs={'class': 'userlang_username', 'placeholder': 'Enter your name'}),
            'self_intro': forms.Textarea(attrs={'class': 'userlang_self_intro', 'rows': '7', 'placeholder':'Enter your introduction'}),
            'address_prefecture': forms.TextInput(attrs={'class': 'userlang_address_prefecture', 'placeholder': 'Tokyo'}),
            'address_city': forms.TextInput(attrs={'class': 'userlang_address_city', 'placeholder': 'Kamisono-cho, Yoyogi, Shibuya-ku'}),
            'address_street': forms.TextInput(attrs={'class': 'userlang_address_street', 'placeholder': '1-1-5'}),
            'entrance_fee': forms.TextInput(attrs={'class': 'userlang_entrance_fee', 'placeholder': 'Adult: 1000yen, child: 500yen'}),
            'business_hours': forms.TextInput(attrs={'class': 'userlang_business_hours', 'placeholder': 'Mon: 10:00-19:00, Tue ~ Fri: 9:00-18:00'}),
            'holiday': forms.TextInput(attrs={'class': 'userlang_holiday', 'placeholder': 'Weekend'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] += ' form-control'
            field.required = False


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
