import os
import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def get_photo_upload_path(self, filename):
    """
        ユーザーごとにアップロードするフォルダパスを変更
    """
    user_dir_path = settings.MEDIA_ROOT + "/postpic/" + str(self.exhibit_id.owner.id) + "/" + str(self.exhibit_id.id)
    if not os.path.exists(user_dir_path):
        os.makedirs(user_dir_path)
    return user_dir_path + "/" + str(self.id) + '.jpg'
    # TODO : 本番環境のときpath入れ替え
    # return "/postpic/" + str(self.exhibit_id.owner.id) + "/" + str(self.exhibit_id.id) + "/" + + str(self.id) + '.jpg'


def get_thumbnail_path(self, filename):
    """
        ユーザーごとにthumbnailフォルダパスを変更
    """
    user_dir_path = settings.MEDIA_ROOT + "/thumbnail/" + str(self.id)
    if not os.path.exists(user_dir_path):
        os.makedirs(user_dir_path)
    return user_dir_path + "/" + str(self.id) + '.jpg'
    # TODO : 本番環境のときpath入れ替え
    # return "/thumbnail/" + str(self.id) + '.jpg'


def get_userthumbnail_path(self, filename):
    """
        モバイルユーザーごとにthumbnailフォルダパスを変更
    """
    user_dir_path = settings.MEDIA_ROOT + "/userthumbnail/" + str(self.id)
    if not os.path.exists(user_dir_path):
        os.makedirs(user_dir_path)
    return user_dir_path + "/" + str(self.id) + '.jpg'


def get_infference_model_path(self, filename):
    """
        各事業所ごとにknn推論モデルとexhibitのcsvファイルを格納するパス
    """
    user_dir_path = settings.MEDIA_ROOT + "/infference/" + str(self.id)
    if not os.path.exists(user_dir_path):
        os.makedirs(user_dir_path)
    return user_dir_path + "/" + filename


class UserManager(BaseUserManager):
    """User Manager"""
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        """Required to register Email address"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """is_staff(if able to login to admin site) and is_superuser(all authorization) is set to be false"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('id',00000)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        db_table = 'user'

    MAJOR_FIELD_CHOICE = [
        ('00', '-'),
        ('11', '山岳'),
        ('12', '高原・湿原・原野'),
        ('13', '湖沼'),
        ('14', '河川・渓谷'),
        ('15', '滝'),
        ('16', '海岸・岬'),
        ('17', '岩石・洞窟'),
        ('18', '動物'),
        ('19', '植物'),
        ('21', '史跡'),
        ('22', '神社・寺院・教会'),
        ('23', '城跡・宮殿'),
        ('24', '集落・街'),
        ('25', '郷土景観'),
        ('26', '庭園・公園'),
        ('27', '建造物'),
        ('28', '年中行事（祭り・伝統行事）'),
        ('29', '動植物園・水族館'),
        ('30', '博物館・美術館'),
        ('31', 'テーマ公園・テーマ施設'),
        ('32', '温泉'),
        ('33', '食'),
        ('34', '芸能・イベント'),
    ]

    id = models.IntegerField('サイトID', primary_key=True)
    email = models.EmailField('Emailアドレス', unique=True)
    username = models.CharField('ユーザー名', max_length=30, default='', help_text='30文字以内で入力してください。')
    # TODO: default path変更
    thumbnail = models.ImageField('サムネイル画像', upload_to=get_thumbnail_path, default='./thumbnail/noimage.png')
    # imagekitによるCACHEからの画像参照
    thumbnail_resized = ImageSpecField(source='thumbnail', processors=[ResizeToFill(250, 250)], format='JPEG', options={'quality': 60})

    self_intro = models.CharField('説明文', max_length=2000, default='', help_text='2,000文字以内で入力してください。')
    major_category = models.CharField('カテゴリー分類', max_length=4, choices=MAJOR_FIELD_CHOICE, default='00')
    address_prefecture = models.CharField('都道府県', max_length=20, default='', help_text='※東京都')
    address_city = models.CharField('市区町村', max_length=50, default='', help_text='※港区芝公園')
    address_street = models.CharField('番地', max_length=50, default='', help_text='※4-2-8')
    latitude = models.FloatField('緯度', max_length=4, null=True, blank=True)
    longitude = models.FloatField('経度', max_length=4, null=True, blank=True)
    tel_number_regex = RegexValidator(regex=r'^[0-9]+$', message=('"09012345678"のようにハイフンなしの形式で入力してください。'))
    telephone = models.CharField('電話番号', max_length=15, validators=[tel_number_regex])
    url = models.CharField('URL', max_length=200, default='', help_text='200文字以内で入力してください。')
    entrance_fee = models.CharField('費用', max_length=200, default='', help_text='200文字以内で入力してください。')
    business_hours = models.CharField('営業時間', max_length=200, default='', help_text='200文字以内で入力してください。')
    rating_sum = models.FloatField('レビュー合計', default=0)
    rating_amount = models.IntegerField('レビュー数', default=0)
    holiday = models.CharField('定休日', max_length=50, default='', help_text='50文字以内で入力してください。')
    knn_model = models.FileField('KNNモデル', upload_to=get_infference_model_path, null=True, blank=True)
    exhibit_csv = models.FileField('対象物CSVリスト', upload_to=get_infference_model_path, null=True, blank=True)
    # TODO: 最新の情報（要検討）
    is_staff = models.BooleanField('スタッフ権限', default=False, help_text='管理サイトにログイン可能かどうか指定してください。')
    is_active = models.BooleanField('アクティブステータス', default='True', help_text='ユーザーがアクティブ状態か指定してください。')
    date_joined = models.DateTimeField('登録日', default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send Email to user"""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


# Exhibit class
class Exhibit(models.Model):

    class Meta:
        db_table = 'exhibit'
        ordering = ('-upload_date',)

    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='exhibit_owner')
    exhibit_name = models.CharField('日本語名', max_length=60, default='', help_text='60文字以内で入力しください')
    exhibit_desc = models.TextField('日本語説明文', max_length=2000, default='', help_text='2000文字以内で入力してください')
    exhibit_name_en = models.CharField('英語名', max_length=140, default='', help_text='140文字以内で入力しください')
    exhibit_desc_en = models.TextField('英語説明文', max_length=2500, default='', help_text='2500文字以内で入力してください')
    exhibit_name_zh = models.CharField('中国語名', max_length=100, default='', help_text='100文字以内で入力しください')
    exhibit_desc_zh = models.TextField('中国語説明文', max_length=2000, default='', help_text='2000文字以内で入力してください')
    upload_date = models.DateTimeField('登録日', default=timezone.now)

    def __str__(self):
        return str(self.exhibit_name) + '(' + str(self.owner) + ')'


class ExhibitPicture(models.Model):

    class Meta:
        db_table = 'exhibit_picture'
        ordering = ('-upload_date',)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exhibit_id = models.ForeignKey(Exhibit, on_delete=models.CASCADE, related_name='exhibit_pk')
    post_pic = models.ImageField(upload_to=get_photo_upload_path, blank=True, null=True)
    upload_date = models.DateTimeField('登録日', default=timezone.now)

    def __str__(self):
        return str(self.exhibit_id.owner.id) + '/' + str(self.exhibit_id.id) + '/' + str(self.id)


# Other Language model class
class UserLang(models.Model):
    class Meta:
        db_table = 'userlang'

    LANGUAGE_FIELD_CHOICE = [
        ('NA', ''),
        ('en', 'English'),
        ('zh', 'Chinese'),
        ('ko', 'Korea')
    ]

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    language = models.CharField('言語', max_length=5, choices=LANGUAGE_FIELD_CHOICE, default='NA')
    username = models.CharField('ユーザー名', max_length=50, default='', help_text='50文字以内で入力してください。')
    self_intro = models.TextField('説明文', max_length=2500, default='', help_text='2,500文字以内で入力してください。')
    address_prefecture = models.CharField('Prefacture', max_length=20, default='', help_text='※Tokyo')
    address_city = models.CharField('City', max_length=50, default='', help_text='※Shiba park, Minato-ku')
    address_street = models.CharField('Street', max_length=50, default='', help_text='※4-2-8')
    entrance_fee = models.CharField('費用', max_length=200, default='', help_text='200文字以内で入力してください。')
    business_hours = models.CharField('営業時間', max_length=200, default='', help_text='200文字以内で入力してください。')
    holiday = models.CharField('定休日', max_length=200, default='', help_text='200文字以内で入力してください。')
    upload_date = models.DateTimeField('登録日', default=timezone.now)

    def __str__(self):
        return str(self.owner) + '(' + str(self.language) + ')'


class AppUser(models.Model):

    class Meta:
        db_table = 'appuser'
        ordering = ('-date_joined',)

    email = models.EmailField('Emailアドレス', unique=True)
    password = models.CharField('パスワード', max_length=100)
    apikey = models.CharField('API Key', max_length=150, null=True, blank=True)
    username = models.CharField('ユーザー名', max_length=100, default="未設定")
    # TODO: デフォルトパスの変更
    thumbnail = models.ImageField(upload_to=get_userthumbnail_path, default='./userthumbnail/noimage.png')
    sex = models.IntegerField('性別', default=0)
    birth = models.IntegerField('生年', default=0)
    country = models.CharField('地域', default='None', max_length=5)
    language = models.CharField('言語', default='OT', max_length=5)
    is_active = models.BooleanField('アクティブステータス', default='false')
    date_joined = models.DateTimeField('登録日', default=timezone.now)

    def __str__(self):
        return str(self.email)


class Review(models.Model):

    class Meta:
        db_table = 'review'
        ordering = ('-date_posted',)

    spot = models.ForeignKey(User, on_delete=models.PROTECT, related_name='review_target')
    writer = models.ForeignKey(AppUser, on_delete=models.PROTECT, related_name='review_writer')
    lang = models.CharField('言語', max_length=5, default='None')
    review_post = models.TextField('レビュー', max_length=500, null=True, blank=True, help_text='500文字以内で入力してください。')
    review_rating = models.FloatField('評価', null=True, blank=True)
    date_posted = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return str(self.spot) + '(written by' + str(self.writer) + ')'


class Like(models.Model):
    class Meta:
        db_table = 'like'
        ordering = ('-date_posted',)

    # APIKEYをappUserとForeingKeyで結合
    apikey = models.CharField('API Key', max_length=150, null=True, blank=True)
    spot = models.ForeignKey(User, on_delete=models.PROTECT, related_name='like_target')
    date_posted = models.DateTimeField('更新日', default=timezone.now)
