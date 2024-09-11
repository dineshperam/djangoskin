# Generated by Django 5.0.4 on 2024-04-21 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dataset",
            fields=[
                ("Id", models.AutoField(primary_key=True, serialize=False)),
                ("Image", models.ImageField(null=True, upload_to="media/")),
            ],
            options={
                "db_table": "Dataset",
            },
        ),
        migrations.CreateModel(
            name="Last_login",
            fields=[
                ("Id", models.AutoField(primary_key=True, serialize=False)),
                ("Login_Time", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "db_table": "last_login",
            },
        ),
        migrations.CreateModel(
            name="Predict_details",
            fields=[
                ("predict_id", models.AutoField(primary_key=True, serialize=False)),
                ("Field_1", models.CharField(max_length=60, null=True)),
                ("Field_2", models.CharField(max_length=60, null=True)),
                ("Field_3", models.CharField(max_length=60, null=True)),
                ("Field_4", models.CharField(max_length=60, null=True)),
                ("Field_5", models.CharField(max_length=60, null=True)),
                ("Field_6", models.CharField(max_length=60, null=True)),
                ("Field_7", models.CharField(max_length=60, null=True)),
                ("Field_8", models.CharField(max_length=60, null=True)),
            ],
            options={
                "db_table": "predict_detail",
            },
        ),
        migrations.CreateModel(
            name="UserModel",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("user_name", models.CharField(help_text="user_name", max_length=50)),
                ("user_age", models.IntegerField(null=True)),
                (
                    "user_email",
                    models.EmailField(help_text="user_email", max_length=254),
                ),
                (
                    "user_password",
                    models.EmailField(help_text="user_password", max_length=50),
                ),
                (
                    "user_address",
                    models.TextField(help_text="user_address", max_length=100),
                ),
                (
                    "user_subject",
                    models.TextField(
                        default="default_value_here",
                        help_text="user_subject",
                        max_length=100,
                    ),
                ),
                (
                    "user_contact",
                    models.CharField(
                        help_text="user_contact", max_length=15, null=True
                    ),
                ),
                ("user_image", models.ImageField(null=True, upload_to="media/")),
                ("Date_Time", models.DateTimeField(auto_now=True, null=True)),
                (
                    "User_Status",
                    models.TextField(default="pending", max_length=50, null=True),
                ),
                ("Otp_Num", models.IntegerField(null=True)),
                (
                    "Otp_Status",
                    models.TextField(default="pending", max_length=60, null=True),
                ),
                ("Last_Login_Time", models.TimeField(null=True)),
                ("Last_Login_Date", models.DateField(auto_now_add=True, null=True)),
                ("No_Of_Times_Login", models.IntegerField(default=0, null=True)),
                ("Message", models.TextField(max_length=250, null=True)),
            ],
            options={
                "db_table": "user_details",
            },
        ),
    ]
