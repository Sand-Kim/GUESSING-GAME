import socket

host = "localhost"
port = 7777

def start_game():
    s = socket.socket()
    s.connect((host, port))

    # received the banner
    data = s.recv(1024)
    print(data.decode().strip())

    # Get user name
    user_name = input().strip()
    s.sendall(user_name.encode())

    while True:
        reply = s.recv(1024).decode().strip()
        if "Do you want to play again?" in reply:
            print(reply)
            play_again = input().strip().lower()
            if play_again == 'yes':
                s.sendall(play_again.encode())
                continue
            elif play_again == 'no':
                s.sendall(play_again.encode())
                print(s.recv(1024).decode().strip())
                s.close()
                break
        else:
            print(reply)
            user_input = input().strip()
            s.sendall(user_input.encode())

start_game()
