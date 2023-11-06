import socket
import sys

SERVER_PORT = 50007
HOST = '192.168.178.30'


def client(infile):
    f = None
    s = None
    try:
        f = open(infile, "rb")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket erstellen
        s.connect((HOST, SERVER_PORT)) # Zum Server verbinden
        s.send(f.read())
        print('Datei {} an den Server {}␣gesendet.'.format(infile, HOST))
    except OSError as msg:
        print('Konnte keine Verbindung zum Server aufbauen oder die Datei nicht␣lesen:{}'.format(msg))
    finally:
        if f is not None:
            f.close()
        if s is not None:
            s.close()


try:
    while True:
        fname = input("Eingabedatei␣(q=Abbruch):")
        if fname != "q":
            client(fname)
        else:
            break
except KeyboardInterrupt: # Zum Unterbrechen des Servers per Taste (in Pycharm und Mac: cmd-F2)
    print('Keyboard␣Interruption')
finally:
    sys.exit(0)