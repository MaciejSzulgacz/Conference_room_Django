from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Rooms, Booking
from django.views import View
import datetime


class BaseView(View):
    template_name = 'ConferenceRoom/Base_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        if capacity:
            capacity = int(capacity)
            if capacity < 1:
                message = "Capacity should be more than zero."
                return render(request, self.template_name, {'message': message})
        projector = request.POST.get('projector')
        if name:
            if capacity:
                if projector:
                    my_rooms = Rooms.objects.filter(name=name, capacity__gte=capacity, projector=projector)
                else:
                    my_rooms = Rooms.objects.filter(name=name, capacity__gte=capacity)
            elif projector:
                my_rooms = Rooms.objects.filter(name=name, projector=projector)
            else:
                my_rooms = Rooms.objects.filter(name=name)
        elif capacity:
            if projector:
                my_rooms = Rooms.objects.filter(capacity__gte=capacity, projector=projector)
            else:
                my_rooms = Rooms.objects.filter(capacity__gte=capacity)
        elif projector:
            my_rooms = Rooms.objects.filter(projector=projector)
        else:
            message = "Fill in at least one field."
            return render(request, self.template_name, {'message': message})
        if not my_rooms:
            message = "No conference room with such parameters."
            return render(request, self.template_name, {'message': message})
        return render(request, self.template_name, {'my_rooms': my_rooms})


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
        return redirect('/list-of-rooms/')


class DeleteRoomView(View):

    def get(self, request, my_id, *args, **kwargs):
        room = Rooms.objects.get(id=my_id)
        room.delete()
        return redirect('/list-of-rooms/')


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
        if Rooms.objects.filter(name=name):
            message = "Room already exist."
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
        else:
            message = "Enter all fields."
            return render(request, self.template_name, {'message': message})
        return redirect('/list-of-rooms/')


class ReserveRoomView(View):
    template_name = 'ConferenceRoom/Reserve_room.html'

    def get(self, request, my_id, *args, **kwargs):
        reservations = Booking.objects.filter(rooms=my_id).order_by('date')
        context = {'reservations': reservations}
        return render(request, self.template_name, context)

    def post(self, request, my_id, *args, **kwargs):
        my_room = Rooms.objects.get(id=my_id)
        my_date = request.POST.get('date')
        comment = request.POST.get('comment')
        if Booking.objects.filter(id=my_id, date=my_date):
            message = "Room is already booked."
            return render(request, self.template_name, {'message': message})
        if my_date < str(datetime.date.today()):
            message = "Choose future date."
            reservations = Booking.objects.filter(rooms=my_id).order_by('date')
            return render(request, self.template_name, {'message': message, 'reservations': reservations})
        try:
            Booking.objects.create(date=my_date, rooms=my_room, comment=comment)
        except IntegrityError:
            message = "Room on this day is already booked."
            return render(request, self.template_name, {'message': message})
        return redirect('/list-of-rooms/')


class DetailsRoomView(View):
    template_name = 'ConferenceRoom/Details_room.html'

    def get(self, request, my_id, *args, **kwargs):
        my_room = Rooms.objects.get(id=my_id)
        reservations = Booking.objects.filter(rooms=my_id).order_by('date')
        context = {'name': my_room.name,
                   'capacity': my_room.capacity,
                   'projector': my_room.projector,
                   'reservations': reservations,
                   'my_id': my_id,
                   }
        return render(request, self.template_name, context)


class ListOfRoomsView(View):
    template_name = 'ConferenceRoom/List_of_rooms.html'

    def get(self, request, *args, **kwargs):
        my_rooms = Rooms.objects.all()
        if not my_rooms:
            message = "There is no available room."
            return render(request, self.template_name, {'message': message})
        for room in my_rooms:
            reservation_dates = [reservation.date for reservation in room.booking_set.all()]
            room.reserved = datetime.date.today() in reservation_dates
        context = {'my_rooms': my_rooms}
        return render(request, self.template_name, context)
