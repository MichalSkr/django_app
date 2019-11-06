from django.test import TestCase
from main_app.models import DataSet
from main_app.views import count_average


class ApiTests(TestCase):
    def setUp(self):
        """
        Creating fake database with two records

        :return: None
        """
        DataSet.objects.create(first_name='Michal', last_name='Test_name', email='test@email.com', birthday="1995-01-10")
        DataSet.objects.create(first_name='Hans', last_name='Test_name', email='test@123', birthday="1991-01-21")

    def test_get_average(self):
        """
        Asserting it to known value.

        :return: None
        """
        data_query = DataSet.objects.all()
        avg = count_average(data_query.values('birthday'))
        self.assertEqual(avg, 26)
