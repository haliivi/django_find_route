from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from .forms import *
from .utils import *
from trains.models import *
from cities.models import *
from routes.models import *
__all__ = [
    'home',
    'find_routes',
    'add_route',
    'save_route',
    'RouteListView',
    'RouteDetailView',
    'RouteDeleteView',
]


# @login_required
def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as e:
                messages.error(request, e)
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})
    else:
        form = RouteForm()
        messages.error(request, 'Нет данных для поиска')
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            total_time = data['total_time']
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = list(map(int, data['trains'].split(',')[:-1]))
            qs_trains = Train.objects.filter(id__in=trains).select_related('from_city', 'to_city')
            qs_cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()
            form = RouteModalForm(
                initial={
                    'from_city': qs_cities[from_city_id],
                    'to_city': qs_cities[to_city_id],
                    'travel_time': total_time,
                    'trains': qs_trains
                }
            )
            context['form'] = form
        return render(request, 'routes/create.html', context)
    else:
        messages.error(request, 'Невозможно сохранить не существующий маршрут')
        return redirect('/')


def save_route(request):
    if request.method == 'POST':
        form = RouteModalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Маршрут успешно сохранен')
            return redirect('/')
        return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, 'Невозможно сохранить не существующий маршрут')
        return redirect('/')


class RouteListView(ListView):
    paginate_by = 5
    model = Route
    template_name = 'routes/list.html'


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/detail.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удален')
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
