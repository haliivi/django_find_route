from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from cities.models import *
from trains.models import *
from routes import views as routes_views
from routes import forms as routes_forms
from cities import views as cities_views
from routes.utils import dfs_paths, get_graph


class AllTestsCase(TestCase):
    def setUp(self):
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')
        list_ = [
            Train(name='tr_1', from_city=self.city_A, to_city=self.city_B, travel_time=9),
            Train(name='tr_2', from_city=self.city_B, to_city=self.city_A, travel_time=11),
            Train(name='tr_3', from_city=self.city_A, to_city=self.city_C, travel_time=7),
            Train(name='tr_4', from_city=self.city_A, to_city=self.city_C, travel_time=10),
            Train(name='tr_5', from_city=self.city_C, to_city=self.city_B, travel_time=6),
            Train(name='tr_6', from_city=self.city_B, to_city=self.city_D, travel_time=8),
            Train(name='tr_7', from_city=self.city_B, to_city=self.city_E, travel_time=3),
            Train(name='tr_8', from_city=self.city_D, to_city=self.city_E, travel_time=4),
            Train(name='tr_9', from_city=self.city_E, to_city=self.city_D, travel_time=5),
        ]
        Train.objects.bulk_create(list_)

    def test_model_city_duplicate(self):
        """
        Тестирование возникновения ошибки при создании дубля города
        """
        city = City(name='A')
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_model_train_duplicate(self):
        """
        Тестирование возникновения ошибки при создании дубля поезда
        """
        train = Train(name='tr_1', from_city=self.city_A, to_city=self.city_B, travel_time=129)
        with self.assertRaises(ValidationError):
            train.full_clean()

    def test_model_travel_time_duplicate(self):
        """
        Тестирование возникновения ошибки при создании дубля поезда
        """
        train = Train(name='tr_11', from_city=self.city_A, to_city=self.city_B, travel_time=9)
        with self.assertRaises(ValidationError):
            train.full_clean()
        try:
            train.full_clean()
        except ValidationError as e:
            self.assertEqual({'__all__': ['Необходимо изменить время в пути']}, e.message_dict)
            self.assertIn('Необходимо изменить время в пути', e.messages)

    def test_home_routes_views(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='routes/home.html')
        self.assertEqual(response.resolver_match.func, routes_views.home)

    def test_cdv_detail_cities_routes_views(self):
        response = self.client.get(reverse('cities:detail', kwargs={'pk': self.city_A.pk}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='cities/detail.html')
        self.assertEqual(response.resolver_match.func.__name__, cities_views.CityDetailView.as_view().__name__)

    def test_find_all_routes(self):
        qs = Train.objects.all()
        graph = get_graph(qs)
        all_routes = dfs_paths(graph, self.city_A.pk, self.city_E.pk)
        self.assertEqual(len(list(all_routes)), 4)

    def test_valid_route_form(self):
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_B.pk,
            'cities': [self.city_E.pk, self.city_D.pk],
            'travel_time': 9,
        }
        form = routes_forms.RouteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_message_error_more_time(self):
        data = {
            'from_city': self.city_A.pk,
            'to_city': self.city_E.pk,
            'cities': [self.city_C.pk],
            'travel_time': 9,
        }
        response = self.client.post('/find_routes/', data)
        self.assertContains(response, 'Время в пути больше заданного', 1, 200)

    def test_message_error_from_cities(self):
        data = {
            'from_city': self.city_B.pk,
            'to_city': self.city_E.pk,
            'cities': [self.city_C.pk],
            'travel_time': 349,
        }
        response = self.client.post('/find_routes/', data)
        self.assertContains(response, 'Маршрут, через эти города не возможен', 1, 200)
