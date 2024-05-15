import socket
import random

host = ""
port = 7777
banner = """
== Guessing Game v1.0 ==
Enter your name:"""

difficulty = """
Choose difficulty:
A. EASY (1-50)
B. MEDIUM (1-100)
C. HARD (1-500)
Enter your choice:"""

data_file = "leaderboard.txt"

def generate_random_int(low, high):
    return random.randint(low, high)

def load_data():
    data = []
    try:
        with open(data_file, 'r') as f:
            for line in f:
                data.append(eval(line.strip()))
    except FileNotFoundError:
        pass
    return data

def save_data(data):
    with open(data_file, 'w') as f:
        for record in data:
            f.write(str(record) + '\n')

leaderboard = load_data()

# initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")
conn = None
user_data = {}

while True:
    if conn is None:
        print("waiting for connection...")
        conn, addr = s.accept()
        print(f"new client: {addr[0]}")
        # cheat_str = f"==== number of guess is {guessme} \n" + banner
        # conn.sendall(cheat_str.encode())
        conn.sendall(banner.encode())
        user_data = {
            "name": "",
            "score": 0,
            "difficulty": "",
            "range": (1, 100),
            "tries": 0
        }
    else:
        client_input = conn.recv(1024).decode().strip()

        if not user_data["name"]:
            user_data["name"] = client_input
            conn.sendall(difficulty.encode())
            continue

        if not user_data["difficulty"]:
            if client_input.upper() == 'A':
                user_data["difficulty"] = "EASY"
                user_data["range"] = (1, 50)
            elif client_input.upper() == 'B':
                user_data["difficulty"] = "MEDIUM"
                user_data["range"] = (1, 100)
            elif client_input.upper() == 'C':
                user_data["difficulty"] = "HARD"
                user_data["range"] = (1, 500)
            else:
                conn.sendall(b"Invalid choice. Please enter A, B, or C: ")
                continue
            guessme = generate_random_int(*user_data["range"])
            user_data["tries"] = 0
            conn.sendall(f"Guess a number between {user_data['range'][0]} and {user_data['range'][1]}: ".encode())
            continue

        if client_input.lower() == 'no':
            conn.sendall(b"Thank you for playing! Goodbye!\n")
            print(f"""
            USER NAME: {user_data['name']} 
            SCORE: {user_data['score']}S
            DIFFICULTY: {user_data['difficulty']} difficulty 
            Disconnected...""")
            leaderboard.append(user_data)
            save_data(leaderboard)
            conn.close()
            conn = None
            continue

        if client_input.lower() == 'yes':
            conn.sendall(difficulty.encode())
            user_data["difficulty"] = ""
            continue

        try:
            guess = int(client_input)
            user_data["tries"] += 1
            if guess == guessme:
                user_data["score"] = user_data["tries"]
                conn.sendall(f"Correct Answer! It took you {user_data['tries']} tries.\nDo you want to play again? (yes/no)".encode())
                leaderboard.append(user_data)
                save_data(leaderboard)
            elif guess > guessme:
                conn.sendall(b"Guess Lower!\nEnter guess: ")
            elif guess < guessme:
                conn.sendall(b"Guess Higher!\nEnter guess: ")
        except ValueError:
            conn.sendall(b"Invalid input. Please enter a number: ")

s.close()
