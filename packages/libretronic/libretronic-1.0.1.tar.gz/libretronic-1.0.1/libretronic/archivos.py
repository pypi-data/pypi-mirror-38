
import paramiko

def subirArchivo(hostname,username,password,file,rutal,rutar):
    local = rutal+"\\"+file
    remoto = rutar+file
    port = 22
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local,remoto)

    finally:
        t.close()

def bajarArchivo(hostname,username,password,file,rutal,rutar):
    local = rutal+"\\"+file
    remoto = rutar+file
    port = 22
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remoto,local)

    finally:
        t.close()        