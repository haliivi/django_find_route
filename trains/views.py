from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from .models import *
__all__ = [
    'TrainListView',
    'TrainDetailView',
    # 'TrainCreateView',
    # 'TrainUpdateView',
    # 'TrainDeleteView',
]


class TrainListView(ListView):
    paginate_by = 5
    model = Train
    template_name = 'trains/home.html'


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


# class TrainCreateView(SuccessMessageMixin, CreateView):
#     model = Train
#     form_class = TrainForm
#     template_name = 'cities/create.html'
#     success_url = reverse_lazy('cities:home')
#     success_message = 'Город успешно создан'
#
#
# class TrainUpdateView(SuccessMessageMixin, UpdateView):
#     model = Train
#     form_class = TrainForm
#     template_name = 'cities/update.html'
#     success_url = reverse_lazy('cities:home')
#     success_message = 'Город успешно отредактирован'
#
#
# class TrainDeleteView(DeleteView):
#     model = Train
#     # template_name = 'cities/delete.html'
#     success_url = reverse_lazy('cities:home')
#
#     def get(self, request, *args, **kwargs):
#         messages.success(request, 'Город успешно удален')
#         self.object = self.get_object()
#         self.object.delete()
#         return HttpResponseRedirect(self.get_success_url())
