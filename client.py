# Amir Arsalan Yavari - 9830253
# FTP protcol client code
# exercise one in network course of the 4th semester @ IUT

from socket import *

serverName = "127.0.0.1"
serverPort = 2121
ClientSocket = socket(AF_INET, SOCK_STREAM)


def controlChannelConnection():
    try:
        ClientSocket.connect((serverName, serverPort))

    except:
        print("Opps!! Try again!")
        print("The connection intrupt :(\n")
        inp = input(
            "Please select one of them\n1. trying again...\n2.exit... \n>> ")

        while(inp != "1" or inp != "2"):
            if inp == "1":
                controlChannelConnection()
            elif inp == "2":
                print("The connection closed...\nBe a nice person :)")
                exit(1)
            else:
                print("Wrong input! Try again...")
    return True


def datChannelConnection(port, name):
    DataChannel = socket(AF_INET, SOCK_STREAM)
    try:
        DataChannel.connect(("127.0.0.1", port))
    except:
        return False
    print("Downloading the file is in progress...")

    data = b""
    while True:
        tempdata = DataChannel.recv(1024)
        data += tempdata
        if not tempdata:
            break

    with open(name, 'wb') as f:
        f.write(data)
    print("File recive succesfully =) ")
    DataChannel.close()
    return True


def main():
    if not controlChannelConnection():
        print("Opps somthing is wrong!! :(\nPlease Trying again...")
        exit(2)

    #print("Now you connect to the server =) \nEnter your commands (Enter help to show list of commands)")
    # The above line transfered to the server code. When client connect to the server this message will be resiveed by client
    msg = ClientSocket.recv(1024)
    print(msg.decode())

    while True:
        cmd = input("\033[0m>> ")
        ClientSocket.send(cmd.encode())
        if "dwld " in cmd.lower():
            TempPort = ClientSocket.recv(1024).decode()
            if TempPort != "0":
                if not datChannelConnection(int(TempPort), cmd[5:]):
                    print(
                        "Opps!! Something is wrong. Please try again in the correct form (the file doesnt exist!)")
            else:
                print(
                    "Opps! The file does not exist :(\nPlease try in the correct form.")
                continue
        recive = ClientSocket.recv(1024).decode()
        print(recive)

        if "quit" == cmd.lower():  # ///////////////////////////space ro handle kon
            print("Have a nice time... :)\nExitting...")
            exit(0)


if __name__ == "__main__":
    main()
