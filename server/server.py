# Amir Arsalan Yavari - 9830253
# FTP protcol server code
# exercise one in network course of the 4th semester @ IUT

from socket import *
import os
from random import randint

socketServer = socket(AF_INET, SOCK_STREAM)
socketServer.bind(("127.0.0.1", 2121))
socketServer.listen(5)
os.chdir("files")
serverPath = os.getcwd()
os.chdir(os.getcwd())
print("The server is ready to connect to the cilent...")


def help():
    print("The client request to print help...")
    string = ""
    string += "HELP:\t\t\t\tShow this help\n"
    string += "LIST:\t\t\t\tList of files\n"
    string += "PWD:\t\t\t\tShow current dir\n"
    string += "CD {dir name}\t\t\tChange directory\n"
    string += "DWLD {file path}\t\tDownload file\n"
    string += "QUIT\t\t\t\tExit"

    return string


def lst():  # The list name is a keyword in python :')
    print("The client request to print list...")
    size = 0
    string = ""
    line = os.listdir()
    for l in line:
        size += os.path.getsize(l)
        if os.path.isdir(l):
            string += "\033[94m>\t" + l + "\t\t\t" + \
                str(os.path.getsize(l)) + "\033[0m\n"
        elif "png" in l or "jpeg" in l or "jpg" in l:
            string += "\u001b[1m\033[35m\t" + l + "\t\t\t" + \
                str(os.path.getsize(l)) + "\033[0m\n"
        else:
            string += "\t" + l + "\t\t\t" + str(os.path.getsize(l)) + "\n"

    return "total " + str(size) + "\n" + string[0:len(string) - 2]


def dwld(contorol_channel, file_name):
    if not file_name in os.listdir():
        print("Bad request! The file does not exist...")
        return "0"

    d_port = randint(3000, 50000)
    DataChannel = socket(AF_INET, SOCK_STREAM)
    DataChannel.bind(("127.0.0.1", d_port))
    print("Data channel created on port " +
          str(d_port) + "\nWating till the client connect")
    DataChannel.listen(5)
    contorol_channel.send(str(d_port).encode())
    Connection_DataChannel, addr = DataChannel.accept()
    print("The client by " + str(addr) + " addres connect to the server")

    try:
        with open(file_name, 'rb') as f:
            data = f.read()
            Connection_DataChannel.send(data)
        print("the file send")
        Connection_DataChannel.close()
        DataChannel.close()
        return "Successful downloading file =)"

    except:
        print("Incorrect file name!")
        Connection_DataChannel.close()
        DataChannel.close()
        return "Incorrect file name! Plase try again in the correct way"


def pwd():
    print("The client request to print directory path (pwd)...")
    curPath = os.getcwd()
    for i in range(0, len(serverPath)):
        if curPath[0] == serverPath[i]:
            curPath = curPath[1:]
            i += 1
        else:
            break

    if len(curPath) == 0:
        return "/"
    else:
        return curPath


def cd(path):
    try:
        curPath = os.getcwd()
        if path == curPath:
            os.chdir(serverPath)
            return "You change directory to " + str(pwd())
        if '/' == path[0]:
            path = serverPath + "/" + path[1:]
        if path[0] == '.' and path[1] == '.':
            path = curPath
            for i in range(len(curPath) - 1, 0, -1):
                if path[i] == '/':
                    break
                path = path[0:i]
        os.chdir(path)
        if not serverPath in os.getcwd():
            print("Bad request! NOOB NOOB NOOB =)")
            os.chdir(curPath)
            return "You dont have access... :)"
    except:
        return "The path doesnt exist..."
    return "You change directory to " + str(pwd())


def main():
    try:
        serverSocket, address = socketServer.accept()
        print("The client from "+str(address)+" connect to the server...")
        serverSocket.send(
            "Now you connect to the server =) \nEnter your commands (Enter help to show list of commands)".encode())
        while True:
            print("Waiting to get request from cilent...")
            command = serverSocket.recv(1024).decode()
            for i in range(0, len(command)):
                command = command[0:i] + command[i].lower() + command[i+1:]
                if command[i] == ' ':
                    break

            rep = ""
            if command == "help":
                rep = help()
            elif command == "list":
                rep = lst()
            elif command[0:4] == "dwld":  # check it///////////////////////////
                rep = dwld(serverSocket, command[5:])
            elif command == "pwd":
                rep = pwd()
            elif command[0:2] == "cd":
                if len(command) > 2 and command[2] != ' ':
                    print("Command not found!")
                    rep = "Command not found: " + command
                elif len(command) == 4 and command[3] == '.':
                    rep = cd(os.getcwd())
                elif len(command) > 3:
                    if command[3] == '.' and command[4] == '/':
                        rep = cd(command[5:])
                    else:
                        rep = cd(command[3:])
                else:
                    rep = cd(serverPath)
            elif command == "quit":
                print("Client close the connection...")
                break
            else:
                print("Command not found!")
                rep = "Command not found: " + command

            serverSocket.send(rep.encode())
    except:
        print("An error ocured... :(")
        serverSocket.send(
            "Sorry the connection faild. Please type quit and try again".encode())

    socketServer.close()


if __name__ == '__main__':
    main()
