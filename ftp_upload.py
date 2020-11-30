import ftplib
import os
import re
CONST_BUFFER_SIZE = 8192


def main(remote_dict, local_dict, file_name, host, user, pwd):
    ftp_client = _connect(host, user, pwd)
    if not ftp_client:
        return False
    ftp_client = _prepare_remote_dict(ftp_client, remote_dict)
    if file_name != "*":
        result = _upload(ftp_client, local_dict, file_name)
    else:
        result = _uploads(ftp_client, local_dict)
    _disconnect(ftp_client)
    return result


def _connect(host, user, pwd):
    try:
        ftp_client = ftplib.FTP()
        ftp_client.connect(host)
        ftp_client.login(user, pwd)
        return ftp_client
    except Exception as e:
        return None


def _prepare_remote_dict(ftp_client, remote_path):
    path_list = remote_path.split("/")
    for dictionary in path_list:
        if dictionary not in ftp_client.nlst():
            ftp_client.mkd(dictionary)
            break
        ftp_client.cwd(dictionary)
    return ftp_client


def _upload(ftp_client, local_dict, file_name):
    file_path = local_dict + file_name
    f = open(file_path, "rb")
    try:
        ftp_client.storbinary('STOR %s' % file_name, f, CONST_BUFFER_SIZE)
        print("upload successful!")
    except ftplib.error_perm as e:
        print('upload failed: ',e)
        return False
    return True


def _uploads(ftp_client, local_dict):
    file_name_list = os.listdir(local_dict)
    result = False
    for file_name in file_name_list:
        file_path = local_dict + file_name
        if os.path.isfile(file_path):
            result = _upload(ftp_client, local_dict, file_name)
            if not result:
                return result
    return result


def _disconnect(ftp_client):
    ftp_client.quit()


if __name__ == "__main__":
    main(upload_address,file_path, file_location)
