import ipfsapi
import os


# Connect to specific server ip and port according to configuration
def connect_to_ipfs(server='127.0.0.1', port=5001):
    try:
        connection = ipfsapi.connect(server, port)
        return connection
    except ipfs.exceptions.ConnectError as ce:
        print(str(ce))


# Push a new file to ipfs
def push_content(ipfs_api, file_path):
    return ipfs_api.add(file_path)


# Read file content
def read_content(ipfs_api, hash_value):
    return ipfs_api.cat(hash_value)


# Download file, currently only at current working dir according to ipfs docs
def download_content(ipfs_api, hash_value):
    ipfs_api.get(hash_value)


if __name__ == '__main__':
    ipfs_api = connect_to_ipfs()
    result = push_content(ipfs_api, os.path.join(os.getcwd(), 'test.txt'))
    content = read_content(ipfs_api, result['Hash'])
    download_content(ipfs_api, result['Hash'])
    print(content)

