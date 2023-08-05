from django.test import TestCase
# from apps.test_app.models import Model


class TestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Run once to set up non-modified data for all class methods."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Run once after all test methods"""
        print()

    def setUp(self):
        """Run before every test method"""
        print(f'\nTest: {self._testMethodName}...')

    def tearDown(self):
        """Run after every test method"""
        pass

    def test_view(self):
        pass
        # model = Model.objects.create(**self.model_data)
        # self.assertIsNotNone(model.pk)
