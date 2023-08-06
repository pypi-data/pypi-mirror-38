from django.test import TestCase
# from rest_framework.test import APITestCase, APIRequestFactory
# from rest_framework import status
# from apps.test_app.models import Model
# from apps.test_app.views import ModelViewSet


# class TestClass(APITestCase, TestCase):
#     view = None

    # @classmethod
    # def setUpTestData(cls):
    #     """Run once to set up non-modified data for all class methods."""
    #     print('#'*100, f'\nsetUpTestData {__name__}...', sep='')
    #
    # @classmethod
    # def tearDownClass(cls):
    #     """Run once after all test methods"""
    #     print()
    #
    # def setUp(self):
    #     """Run before every test method"""
    #     print(f'\nTest: {self._testMethodName}...')
    #
    #     views = {
    #         'model': ModelViewSet,
    #     }
    #     self.view = views.get(self._testMethodName.split('test_', 1)[-1].split('_', 1)[0])
    #
    # def tearDown(self):
    #     """Run after every test method"""
    #     pass

    # def rest(self, urn: str, pk: str=None, data: dict=None, method: str='GET', view=None):
    #     urn = urn.replace('<pk>', str(pk)) if pk else urn
    #     method = method.upper() if isinstance(method, str) else method
    #     view = view or self.view or None
    #     print('Request', method, urn)
    #
    #     actions = {
    #         'get': 'retrieve',
    #         'post': 'create',
    #         'put': 'update',
    #         'patch': 'partial_update',
    #         'delete': 'destroy',
    #     }
    #
    #     view = view.as_view(actions)
    #     factory = APIRequestFactory()
    #
    #     request = None
    #     if method in ('GET', 'DELETE'):
    #         request = getattr(factory, method.lower())(urn)
    #     elif data and method in ('POST', 'PUT', 'PATCH'):
    #         request = getattr(factory, method.lower())(urn, data=data, format='json')
    #
    #     if request:
    #         response = view(request, pk=str(pk)).render()
    #         print(response)
    #         print(response.data)
    #         return response
    #
    # def rest_get(self, urn: str, pk: str, view=None):
    #     return self.rest(urn, pk=pk, method='GET', view=view)
    #
    # def rest_post(self, urn: str, data: dict, view=None):
    #     return self.rest(urn, data=data, method='POST', view=view)
    #
    # def rest_put(self, urn: str, data: dict, pk: str, view=None):
    #         return self.rest(urn, pk=pk, data=data, method='PUT', view=view)
    #
    # def rest_patch(self, urn: str, data: dict, pk: str, view=None):
    #     return self.rest(urn, pk=pk, data=data, method='PATCH', view=view)
    #
    # def rest_delete(self, urn: str, pk: str, view=None):
    #     return self.rest(urn, pk=pk, method='DELETE', view=view)

    # def test_model_create(self):
    #     response = self.rest_post('/api/model', self.model_data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIsNotNone(response.data.get('uid'))
    #
    # def test_model_get(self):
    #     model = Model.objects.create(**self.model_data)
    #     response = self.rest_get('/api/model/<pk>', pk=model.uid)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsNotNone(response.data.get('pk'))
    #     self.assertEqual(response.data['pk'], str(model.pk))
    #
    # def test_model_put(self):
    #     model = Model.objects.create()
    #     response = self.rest_put('/api/model/<pk>', pk=model.pk, data=self.model_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data.get('attribute'), self.model_data['attribute'])
    #
    # def test_model_patch(self):
    #     model = Model.objects.create()
    #     response = self.rest_patch('/api/model/<pk>', pk=model.pk, data=self.model_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data.get('attribute'), self.model_data['attribute'])
    #
    # def test_model_delete(self):
    #     model = Model.objects.create(**self.model_data)
    #     response = self.rest_delete('/api/model/<pk>', pk=model.pk)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data, None)
