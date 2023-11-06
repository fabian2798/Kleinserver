
import socket
from threading import Thread
from Aufgabe8a import create_layout
TCP_IP = 'localhost'  # 127.0.0.1
TCP_PORT = 50007
BUFSIZE = 1024
threads = []

# Empfangen und Speichern
def handle_communication(con, a, sid):
    json_string = b'' # bytestring
    with open('Received {} {} {}.txt'.format(addr[0], a[1], sid), 'wb') as f: # as binary
        while True:
            data = con.recv(BUFSIZE) # con = Server
            if not data:
                break
            else:
                f.write(data) # write log_datei
                json_string += data # create bytestring from readed bytes
        create_layout(json_string.decode('utf-8')) # create tex_file

        print('   [{}] [Übertragung und Speichern beendet]'.format(sid))


def thread_for_client(c, a, si):
    print(" [{}] Neuer Client socket thread gestartet auf {} , {}".format(si, a[0], a[1]))
    handle_communication(c, a, si)
    conn.close()
    print("   [{}] beende Thread.".format(si))


s = None
conn = None
server_id = 1 # dient nur der besseren Unterscheidung. Produktiv nicht nötig.

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# AF_INET = IPv4, SOCK_STREAM = TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # SO_REUSEADDR !! # für schnelleren wiedergebrauch des ports
    s.bind((TCP_IP, TCP_PORT)) # bindet Socket(Server) an Port mit bestimmter IP
    s.listen(0) # argument 0 = anzahl egal
    print('Server gestartet auf {}\n'.format(s.getsockname()))

    while True:
        print('Haupt-Thread wartet auf Verbindung (Server-ID={})...'.format(server_id))
        conn, addr = s.accept() # Warte auf eine Verbindung zum Server
        # addr = (IP, Port)
        newthread = Thread(target=thread_for_client, args=(conn, addr, server_id)) # Erstellung eines neues Threads
        newthread.start() # Startet Thread
        threads.append(newthread)
        server_id += 1 # dient nur der besseren Unterscheidung. Produktiv nicht nötig.

except KeyboardInterrupt: # Zum Unterbrechen des Servers per Taste (in Pycharm und Mac: cmd-F2)
    print('Schliesse Haupt-Thread (Server-ID={}).'.format(server_id))
except socket.error as msg:
    print('Exception: socket.error : {}'.format(msg))
finally:
    if conn is not None:
        conn.close() # Connection schliessen
    if s is not None:
        s.close() # Socket schliessen
    for t in threads:
        t.join() # Bearbeitung der Threads nach der Reihe, (Thread 2 wird gestartet wenn Thread 1 beendet ist)
            # Sicherheit : keine Zombiethreads ( nach beendung des hauptprogramm keine unter threads laufen)