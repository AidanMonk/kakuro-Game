from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .utils.KakuroBoard import KakuroBoard
from .utils.BoardGenerator import BoardGenerator
from .utils.BoardSerializer import BoardSerializer
from .utils.KakuroValidator import KakuroValidator

User = get_user_model()

@api_view(['GET', 'POST'])
def init_board(request):
    board = KakuroBoard()  # Create a new board instance

    # Get difficulty level from request
    if request.method == 'POST':
        difficulty = request.data.get('difficulty', 'medium')
    else:
        # Default to medium difficulty for GET requests
        difficulty = request.GET.get('difficulty', 'medium')

    # Generate board with specified difficulty
    board.set_board(BoardGenerator.generate_board(difficulty))

    # Return board data and difficulty level
    return JsonResponse({
        "board": BoardSerializer.serialize(board.get_board()),
        "difficulty": difficulty
    })

@api_view(['POST'])
def validate_board(request):
    kakuro_board = BoardSerializer.deserialize(request.data.get('board'))
    is_valid = KakuroValidator.validate(kakuro_board.get_board())

    return JsonResponse({
        "is_valid": is_valid  # Send the validity status back
    })

# User Registration
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists. Please use another email."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists. Please choose another one."}, status=400)

        user = User.objects.create(
            email=email,
            username=username,
            password=make_password(password)  # Ensures password is properly hashed!
        )
        return JsonResponse({"message": "User created successfully"}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)


# User Login
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        # Authenticate using email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid email or password"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)