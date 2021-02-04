from django.shortcuts import render
from .models import Rooms
from django.views import View


class Base(View):
    template_name = 'ConferenceRoom/Base_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


class NewRoomView(View):
    template_name = 'ConferenceRoom/New_room.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        message = None
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = request.POST.get('projector')
        if not name:
            message = "Enter the name."
        if Rooms.objects.filter(name='Sala 1'):
            message = "Name is already used."
        if not capacity > 0:
            message = "Capacity should be more than zero."
        if all([name, capacity, projector]):
            Rooms.objects.create(name=name, capacity=capacity, projector=projector)
        context = {'message': message}
        return render(request, self.template_name, context)
