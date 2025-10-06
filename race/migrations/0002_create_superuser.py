from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    # Vercelの環境変数からスーパーユーザーの情報を取得
    # もし環境変数がなければ、デフォルト値が使われる（ローカルでのエラー防止）
    SU_NAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    SU_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    SU_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'password')

    # スーパーユーザーがまだ存在しない場合のみ作成する
    if not User.objects.filter(username=SU_NAME).exists():
        print(f'Creating superuser: {SU_NAME}')
        User.objects.create_superuser(
            username=SU_NAME,
            email=SU_EMAIL,
            password=SU_PASSWORD
        )
    else:
        print(f'Superuser {SU_NAME} already exists.')


class Migration(migrations.Migration):

    dependencies = [
        ('race', '0001_initial'),  # 直前のマイグレーションファイル名に合わせてください
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]