from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from cloudmanager.board import MicropythonBoards, MicropythonBoard
from cloudmanager.exceptions import BoardNotResponding


class BoardIndexView(TemplateView):
    template_name = "cloudmanager_notebook_ui/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['boards'] = list(MicropythonBoards().all())
        context['boards'].sort(key=lambda x: x.name, reverse=False)
        return context


class BoardView(TemplateView):
    template_name = "cloudmanager_notebook_ui/board.html"
    board = None

    def get(self, request, **kwargs):
        self.board = request.GET.get('board', None)
        return super(BoardView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        print(kwargs)
        if self.board:
            context['board'] = MicropythonBoard(self.board)
        # context['boards'] = MicropythonBoards().all()
        return context


@method_decorator(csrf_exempt, name='dispatch')
class RunView(View):
    template_name = 'cloudmanager_notebook_ui/run.html'
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        print(args[0].POST)
        board = args[0].POST['board']
        code = args[0].POST['code']
        try:
            for result in MicropythonBoards().execute(code, range=board):
                output = result.read().decode()
                break
        except BoardNotResponding:
            output = 'Board %r is not responding' % board
        return JsonResponse({'output': output})
