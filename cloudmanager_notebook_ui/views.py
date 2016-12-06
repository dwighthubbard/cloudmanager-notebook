from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from cloudmanager.board import MicropythonBoards, MicropythonBoard
from cloudmanager.exceptions import BoardNotResponding


class BoardIndexView(TemplateView):
    template_name = "cloudmanager_notebook_ui/index.html"

    def get_context_data(self, **kwargs):
        context = super(BoardIndexView, self).get_context_data(**kwargs)
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
        context['editor'] = {
            'lineNumbers': 'false'
        }
        # context['boards'] = MicropythonBoards().all()
        return context


@method_decorator(csrf_exempt, name='dispatch')
class RunView(View):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        print(args[0].POST)
        board = args[0].POST['board']
        code = args[0].POST['code']
        output = ''
        try:
            output = MicropythonBoard(board).execute(code).read().decode()
            # for result in MicropythonBoards().execute(code, range=board):
            #     print(result)
            #     output += result.read().decode()
        except BoardNotResponding:
            output = 'Board %r is not responding' % board
        return JsonResponse({'output': output})

@method_decorator(csrf_exempt, name='dispatch')
class StatusView(View):
    http_method_names = ['get']

    def get(self, request, **kwargs):
        self.board = request.GET.get('board', None)
        state = 'Offline'
        if self.board:
            state = MicropythonBoard(self.board).state
        if not state:
            state ='Not Responding'
        if request.GET.get('format', None):
            return JsonResponse({'state': state})
        return HttpResponse(state)
