import requests
import os

def download_file_from_google_drive(id, destination):
    '''
    The url to download is from Google API but will using requests module instead
    Need to fill the parameter for the whole url to work
    '''
    url = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    
    response = session.get(url, params = {'id': id}, stream = True)


    token = get_confirm_token(response)
    
    '''
    When download large file, there will be warning message and require confirmaton, the below is to take care of that
    '''
    if token:
        params = {'id' : id, 'confirm' : token}
        response = session.get(url, params = params, stream = True)
    
    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

'''
The function simply write to file.txt, change later
'''
def save_response_content(response, destination):
    chunk_size = 32768

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)

if __name__ == "__main__":
    file_id = '1OqGe29clJRzloYSGf7hGEONoLzRqpUZk'
    destination = os.path.join(os.getcwd(), 'test.txt')
    download_file_from_google_drive(file_id, destination)	
