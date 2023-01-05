# Script to transfer files between two computers in the same network
# Author: Mário
# Date: 04/01/2023
import paramiko

def transfer_file(file = str, target = str, host = "192.168.178.150", user = "panama1") -> None:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port = "22", username = user)

    ftp_client=ssh.open_sftp()
    try:
        ftp_client.put(file, target)
    except (IOError, OSError) as error:
        raise error  
    ftp_client.close()

def main() -> None:
    original_file = "test.jpg"
    target_file = "/home/panama1/external/Frog_videos/test.jpg"

    transfer_file(original_file, target_file)

if __name__ == "__main__":
    main()