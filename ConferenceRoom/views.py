from django.shortcuts import render, redirect
from .models import Rooms
from django.views import View


class BaseView(View):
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
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = request.POST.get('projector')
        if not name:
            message = "Enter the name."
            return render(request, self.template_name, {'message': message})
        if Rooms.objects.filter(name=name):
            message = "Name is already used."
            return render(request, self.template_name, {'message': message})
        if not capacity > 0:
            message = "Capacity should be more than zero."
            return render(request, self.template_name, {'message': message})
        if all([name, capacity, projector]):
            Rooms.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect('/base/')


class DeleteRoomView(View):

    def get(self, request, my_id, *args, **kwargs):
        room = Rooms.objects.get(id=my_id)
        room.delete()
        return redirect('/base/')


class EditRoomView(View):
    template_name = 'ConferenceRoom/Edit_room.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, my_id, *args, **kwargs):
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = request.POST.get('projector')
        if not name:
            message = "Enter the name."
            return render(request, self.template_name, {'message': message})
        if not Rooms.objects.filter(id=my_id):
            message = "Room does not exist."
            return render(request, self.template_name, {'message': message})
        if not capacity > 0:
            message = "Capacity should be more than zero."
            return render(request, self.template_name, {'message': message})
        if all([name, capacity, projector]):
            room = Rooms.objects.get(id=my_id)
            room.name = name
            room.capacity = capacity
            room.projector = projector
            room.save()
        return redirect('/base/')
