from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
import random
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .utils.KakuroBoard import KakuroBoard
from .utils.BoardGenerator import BoardGenerator
from .utils.RandomBoardGenerator import RandomBoardGenerator
from .utils.BoardSerializer import BoardSerializer
from .utils.KakuroValidator import KakuroValidator
from .utils.NumberCell import NumberCell

User = get_user_model()

# Dictionary to store active boards and their solutions
active_boards = {}


@api_view(['GET', 'POST'])
def init_board(request):
    board = KakuroBoard()  # Create a new board instance

    # Get difficulty level from request
    if request.method == 'POST':
        difficulty = request.data.get('difficulty', 'medium')
    else:
        # Default to medium difficulty for GET requests
        difficulty = request.GET.get('difficulty', 'medium')

    # Add a random seed to ensure we get different boards each time
    random.seed()  # Reset the random seed

    # Generate a random board with its solution
    generated_board, solution = RandomBoardGenerator.generate_board_with_solution(difficulty)
    board.set_board(generated_board)

    # Generate a unique ID for this board
    board_id = str(random.randint(10000, 99999))

    # Store the board and solution
    active_boards[board_id] = {
        "board": generated_board,
        "solution": solution,
        "difficulty": difficulty
    }

    # Return board data, difficulty level, and the board_id
    return JsonResponse({
        "board": BoardSerializer.serialize(board.get_board()),
        "difficulty": difficulty,
        "board_id": board_id
    })


@api_view(['POST'])
def validate_board(request):
    kakuro_board = BoardSerializer.deserialize(request.data.get('board'))
    is_valid = KakuroValidator.validate(kakuro_board.get_board())

    return JsonResponse({
        "is_valid": is_valid  # Send the validity status back
    })


@api_view(['POST'])
def get_hint(request):
    # Get the data from the request
    board_id = request.data.get('board_id')
    row = request.data.get('row')
    col = request.data.get('col')

    # Check if the board ID exists
    if board_id not in active_boards:
        return JsonResponse({"error": "Invalid board ID"}, status=400)

    # Get the board and solution
    board_data = active_boards[board_id]
    board = board_data["board"]
    solution = board_data["solution"]

    # Check if the coordinates are valid and point to a NumberCell
    if (row < 0 or row >= len(board) or
            col < 0 or col >= len(board[0]) or
            not isinstance(board[row][col], NumberCell)):
        return JsonResponse({"error": "Invalid cell coordinates"}, status=400)

    # Get the correct value from the solution
    hint_value = solution[row][col]

    # Debug info
    print(f"Providing hint for board {board_id}: cell ({row},{col}) = {hint_value}")

    return JsonResponse({
        "hint_value": hint_value,
        "row": row,
        "col": col
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