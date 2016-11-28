from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from cloudmanager.board import MicropythonBoards


class IndexView(TemplateView):
    template_name = "cloudmanager_notebook_ui/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['boards'] = MicropythonBoards().all()
        return context


class BoardView(TemplateView):
    template_name = "cloudmanager_notebook_ui/board.html"

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        context['boards'] = MicropythonBoards().all()
        return context
