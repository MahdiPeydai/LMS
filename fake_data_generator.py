import os
import django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnlineLearning.settings")
django.setup()

from accounts.models import User
from course.models import Course, Category
from instructor.models import Instructor

fake = Faker()


def generate_fake_users():
    for _ in range(20):
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = fake.email()
        password = fake.password()
        phone = fake.random_int(min=10000000000, max=50000000000)

        User.objects.create(first_name=firstname, last_name=lastname, email=email, password=password, phone=phone)

    for _ in range(5):
        category_name = fake.word()
        Category.objects.create(name=category_name)

    for _ in range(30):
        course = Course.objects.create(name=fake.text(max_nb_chars=30), instructor=Instructor.objects.get(id=1), description=fake.text(max_nb_chars=250),
                                       duration=fake.random_int(min=1, max=90),
                                       level=fake.random_int(min=1, max=3), image=fake.image_url(),
                                       price=fake.random_int(min=10000, max=1000000))
        for _ in range(fake.random_int(min=1, max=3)):
            category = Category.objects.get(id=fake.random_int(min=1, max=5))
            course.categories.add(category)


if __name__ == "__main__":
    generate_fake_users()
