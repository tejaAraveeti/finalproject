# Importing necessary modules
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Your APIView classes remain the same
class SignupView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created successfully"}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data
            print("User details:", user)
            token = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "access_token": str(token.access_token),
                "refresh_token": str(token)
            })
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=401)


class MovieView(APIView):
    def get(self, request, id = None):
        if id:
            try:
                movie = Movie.objects.get(id=id)
                serializer = MovieSerializer(movie).data
                return Response(serializer, status=200)
            except Movie.DoesNotExist:
                return Response({"error": "Movie not found"}, status=404)

        title = request.GET.get('query', None)
        rating = request.GET.get('rating', None)
        genre = request.GET.get('genre', None)
        language = request.GET.get('language', None)
        page_no = request.GET.get("page", 1)

        all_movies = Movie.objects.all().order_by("-id")
        if title:
            all_movies = all_movies.filter(Q(title__icontains=title) | Q(description__icontains=title))
        if rating:
            all_movies = all_movies.filter(rating__gte=int(rating))
        if genre:
            all_movies = all_movies.filter(genre__icontains=genre)
        if language:
            all_movies = all_movies.filter(Q(language__in=language.split("|")) | Q(language__icontains=language))

        paginate = Paginator(all_movies, 6)
        page = paginate.get_page(page_no)
        page_data = page.object_list
        serializer = MovieSerializer(page_data, many=True).data
        return Response(
            {
                "count": all_movies.count(),
                "total_page": paginate.num_pages,
                "next": page.has_next(),
                "previous": page.has_previous(),
                "data": serializer
            }, status=200
        )





    
    def post(self, request):
        data = request.data
        print("Request Data:", data)

        serializer = MovieSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            print("Validation Error:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request, id=None): 
        try:
           movie = Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
    def delete(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
            movie.delete()
            return Response({"message": "Movie deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response("Movie not found", status=status.HTTP_404_NOT_FOUND) 

#---------- theater---------------
class TheaterView(APIView):
    def post(self, request):
        data = request.data
        serializer = TheaterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id is None:
            theaters = Theater.objects.all()
            serializer = TheaterSerializer(theaters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                theater = Theater.objects.get(id=id)
                serializer = TheaterSerializer(theater)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Theater.DoesNotExist:
                return Response({"error": "Theater not found"}, status=status.HTTP_404_NOT_FOUND)



    def put(self, request, id=None):
        try:
            theater = Theater.objects.get(id=id)
            serializer = TheaterSerializer(theater, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Theater.DoesNotExist:
            return Response({"message": "Theater not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        try:
            theater = Theater.objects.get(id=id)
            theater.delete()
            return Response({"message": "Theater deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Theater.DoesNotExist:
            return Response({"message": "Theater not found"}, status=status.HTTP_404_NOT_FOUND)


 #--------------------seats--------------------
class SeatsView(APIView):
    def get(self, request, seat_id=None):
        if seat_id is None:
            seats = Seats.objects.all()
            serializer = SeatsSerializer(seats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                seat = Seats.objects.get(id=seat_id)
                serializer = SeatsSerializer(seat)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Seats.DoesNotExist:
                return Response({"error": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        serializer = SeatsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, seat_id):
        try:
            seat = Seats.objects.get(id=seat_id)
            serializer = SeatsSerializer(seat, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Seats.DoesNotExist:
            return Response({"message": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, seat_id):
        try:
            seat = Seats.objects.get(id=seat_id)
            seat.delete()
            return Response({"message": "Seat deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Seats.DoesNotExist:
            return Response({"message": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)



#-----------------Movie in theaters list --------------------------------
class MovieTheaterView(APIView):
    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        movie_serializer = MovieSerializer(movie).data
        theaters_serializer = TheaterSerializer(movie.theaters.all(), many=True).data

        response_data = {
            "movie": movie_serializer,
            "theaters": theaters_serializer,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, movie_id):
        data = request.data
        print("Received data:", data)
        try:
            movie = Movie.objects.get(id=movie_id)
            print("Movie found:", movie)
        except Movie.DoesNotExist:
            print("Movie not found")
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        theater_ids = data.get(str(movie_id), [])
        print("Theater IDs:", theater_ids)

        for theater_id in theater_ids:
            try:
                theater = Theater.objects.get(id=theater_id)
                print("Theater found:", theater)
                movie.theaters.add(theater)
            except Theater.DoesNotExist:
                print(f"Theater with ID {theater_id} not found")

        updated_movie_serializer = MovieSerializer(movie).data
        return Response(updated_movie_serializer, status=status.HTTP_200_OK)

    #--------to fetch all movie in theater--------------
        

# class MovieTheaterView(APIView):
#     def get(self, request):
#         movies = Movie.objects.all()
#         movies_serializer = MovieSerializer(movies, many=True).data

#         theaters = Theater.objects.all()
#         theaters_serializer = TheaterSerializer(theaters, many=True).data

#         response_data = {
#             "movies": movies_serializer,
#             "theaters": theaters_serializer,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)





#---------------------theaterseat-------------------------------

class TheaterSeatView(APIView):
    def get(self, request, theater_id):
        try:
            theater = Theater.objects.get(id=theater_id)
            seats = Seats.objects.filter(theater=theater)
            serializer = SeatsSerializer(seats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Theater.DoesNotExist:
            return Response({"error": f"Theater with id {theater_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        except Seats.DoesNotExist:
            return Response({"error": f"No seats found for the specified theater"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, theater_id):
        try:
            theater = Theater.objects.get(id=theater_id)
        except Theater.DoesNotExist:
            return Response({"message": f"Theater with id {theater_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        seats_data = request.data.get(str(theater_id), [])

        added_seats = []
        for seat_id in seats_data:
            try:
                seat = Seats.objects.get(id=seat_id)
                seat.theater = theater
                seat.save()
                added_seats.append(seat.id)
            except Seats.DoesNotExist:
                return Response({"message": f"Seat with id {seat_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Seats added to the theater successfully", "added_seats": added_seats}, status=status.HTTP_201_CREATED)

class BookSeatsView(APIView):
    def post(self, request):
        theater_id = request.data.get('theaterId')
        seat_ids = request.data.get('seatIds', [])

        # Your booking logic goes here
        # Make sure to handle errors, update the seat status, etc.

        return Response({"message": "Seats booked successfully"}, status=status.HTTP_200_OK)




#-------------------------bookings------------------------
class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user 

        bookings = Booking.objects.filter(user=user)

        serializer = BookingSerializer(bookings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user 

        movie_data = request.data.get('movie', {})
        seats_data = request.data.get('seats', [])
        total_cost = request.data.get('total_cost', 0.0)

        theaters_data = movie_data.get('theaters', [])

        try:
            if not theaters_data or not seats_data:
                raise ValueError("Theaters and seats are required for booking.")

            # Log the received data for debugging
            print(f"Received data: {request.data}")

            movie = Movie.objects.get(pk=movie_data['id'])
            seats = Seats.objects.filter(id__in=seats_data)

            total_cost = sum(seat.price for seat in seats)

            booking = Booking.objects.create(user=user, movie=movie, total_cost=total_cost)
            booking.seats.set(seats)

            return Response({"message": "Booking created successfully"}, status=status.HTTP_201_CREATED)

        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        except Seats.DoesNotExist:
            return Response({"error": "One or more selected seats not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
