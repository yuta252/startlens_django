# Generated by Django 2.2.13 on 2020-07-19 09:00

import analysis.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='サイトID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Emailアドレス')),
                ('username', models.CharField(default='', help_text='30文字以内で入力してください。', max_length=30, verbose_name='ユーザー名')),
                ('thumbnail', models.ImageField(default='./thumbnail/noimage.png', upload_to=analysis.models.get_thumbnail_path, verbose_name='サムネイル画像')),
                ('self_intro', models.CharField(default='', help_text='2,000文字以内で入力してください。', max_length=2000, verbose_name='説明文')),
                ('major_category', models.CharField(choices=[('00', '-'), ('11', '山岳'), ('12', '高原・湿原・原野'), ('13', '湖沼'), ('14', '河川・渓谷'), ('15', '滝'), ('16', '海岸・岬'), ('17', '岩石・洞窟'), ('18', '動物'), ('19', '植物'), ('21', '史跡'), ('22', '神社・寺院・教会'), ('23', '城跡・宮殿'), ('24', '集落・街'), ('25', '郷土景観'), ('26', '庭園・公園'), ('27', '建造物'), ('28', '年中行事（祭り・伝統行事）'), ('29', '動植物園・水族館'), ('30', '博物館・美術館'), ('31', 'テーマ公園・テーマ施設'), ('32', '温泉'), ('33', '食'), ('34', '芸能・イベント')], default='00', max_length=4, verbose_name='カテゴリー分類')),
                ('address_prefecture', models.CharField(default='', help_text='※東京都', max_length=20, verbose_name='都道府県')),
                ('address_city', models.CharField(default='', help_text='※港区芝公園', max_length=50, verbose_name='市区町村')),
                ('address_street', models.CharField(default='', help_text='※4-2-8', max_length=50, verbose_name='番地')),
                ('latitude', models.FloatField(blank=True, max_length=4, null=True, verbose_name='緯度')),
                ('longitude', models.FloatField(blank=True, max_length=4, null=True, verbose_name='経度')),
                ('telephone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='"09012345678"のようにハイフンなしの形式で入力してください。', regex='^[0-9]+$')], verbose_name='電話番号')),
                ('url', models.CharField(default='', help_text='200文字以内で入力してください。', max_length=200, verbose_name='URL')),
                ('entrance_fee', models.CharField(default='', help_text='200文字以内で入力してください。', max_length=200, verbose_name='費用')),
                ('business_hours', models.CharField(default='', help_text='200文字以内で入力してください。', max_length=200, verbose_name='営業時間')),
                ('rating_sum', models.FloatField(default=0, verbose_name='レビュー合計')),
                ('rating_amount', models.IntegerField(default=0, verbose_name='レビュー数')),
                ('holiday', models.CharField(default='', help_text='50文字以内で入力してください。', max_length=50, verbose_name='定休日')),
                ('knn_model', models.FileField(blank=True, null=True, upload_to=analysis.models.get_infference_model_path, verbose_name='KNNモデル')),
                ('exhibit_csv', models.FileField(blank=True, null=True, upload_to=analysis.models.get_infference_model_path, verbose_name='対象物CSVリスト')),
                ('is_staff', models.BooleanField(default=False, help_text='管理サイトにログイン可能かどうか指定してください。', verbose_name='スタッフ権限')),
                ('is_active', models.BooleanField(default='True', help_text='ユーザーがアクティブ状態か指定してください。', verbose_name='アクティブステータス')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Emailアドレス')),
                ('password', models.CharField(max_length=100, verbose_name='パスワード')),
                ('apikey', models.CharField(blank=True, max_length=150, null=True, verbose_name='API Key')),
                ('username', models.CharField(default='未設定', max_length=100, verbose_name='ユーザー名')),
                ('thumbnail', models.ImageField(default='./userthumbnail/noimage.png', upload_to=analysis.models.get_userthumbnail_path)),
                ('sex', models.IntegerField(default=0, verbose_name='性別')),
                ('birth', models.IntegerField(default=0, verbose_name='生年')),
                ('country', models.CharField(default='None', max_length=5, verbose_name='地域')),
                ('language', models.CharField(default='OT', max_length=5, verbose_name='言語')),
                ('is_active', models.BooleanField(default='false', verbose_name='アクティブステータス')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
            ],
            options={
                'db_table': 'appuser',
                'ordering': ('-date_joined',),
            },
        ),
        migrations.CreateModel(
            name='Exhibit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exhibit_name', models.CharField(default='', help_text='60文字以内で入力しください', max_length=60, verbose_name='日本語名')),
                ('exhibit_desc', models.TextField(default='', help_text='2000文字以内で入力してください', max_length=2000, verbose_name='日本語説明文')),
                ('exhibit_name_en', models.CharField(default='', help_text='140文字以内で入力しください', max_length=140, verbose_name='英語名')),
                ('exhibit_desc_en', models.TextField(default='', help_text='2500文字以内で入力してください', max_length=2500, verbose_name='英語説明文')),
                ('exhibit_name_zh', models.CharField(default='', help_text='100文字以内で入力しください', max_length=100, verbose_name='中国語名')),
                ('exhibit_desc_zh', models.TextField(default='', help_text='2000文字以内で入力してください', max_length=2000, verbose_name='中国語説明文')),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exhibit_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exhibit',
                'ordering': ('-upload_date',),
            },
        ),
        migrations.CreateModel(
            name='UserLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('NA', ''), ('en', 'English'), ('zh', 'Chinese'), ('ko', 'Korea')], default='NA', max_length=5, verbose_name='言語')),
                ('username', models.CharField(default='', help_text='50文字以内で入力してください。', max_length=50, verbose_name='ユーザー名')),
                ('self_intro', models.TextField(default='', help_text='2,500文字以内で入力してください。', max_length=2500, verbose_name='説明文')),
                ('address_prefecture', models.CharField(default='', help_text='※Tokyo', max_length=20, verbose_name='Prefacture')),
                ('address_city', models.CharField(default='', help_text='※Shiba park, Minato-ku', max_length=50, verbose_name='City')),
                ('address_street', models.CharField(default='', help_text='※4-2-8', max_length=50, verbose_name='Street')),
                ('entrance_fee', models.CharField(default='', help_text='200文字以内で入力してください。', max_length=200, verbose_name='費用')),
                ('business_hours', models.CharField(default='', help_text='200文字以内で入力してください。', max_length=200, verbose_name='営業時間')),
                ('holiday', models.CharField(default='', help_text='200文字以内で入力してください。', max_length=200, verbose_name='定休日')),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'userlang',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(default='None', max_length=5, verbose_name='言語')),
                ('review_post', models.TextField(blank=True, help_text='500文字以内で入力してください。', max_length=500, null=True, verbose_name='レビュー')),
                ('review_rating', models.FloatField(blank=True, null=True, verbose_name='評価')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日')),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_target', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_writer', to='analysis.AppUser')),
            ],
            options={
                'db_table': 'review',
                'ordering': ('-date_posted',),
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apikey', models.CharField(blank=True, max_length=150, null=True, verbose_name='API Key')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新日')),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='like_target', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'like',
                'ordering': ('-date_posted',),
            },
        ),
        migrations.CreateModel(
            name='ExhibitPicture',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('post_pic', models.ImageField(blank=True, null=True, upload_to=analysis.models.get_photo_upload_path)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
                ('exhibit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exhibit_pk', to='analysis.Exhibit')),
            ],
            options={
                'db_table': 'exhibit_picture',
                'ordering': ('-upload_date',),
            },
        ),
    ]
