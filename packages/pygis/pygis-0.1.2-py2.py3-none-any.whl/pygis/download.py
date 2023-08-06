import os
import zipfile
import tarfile
import shutil
import urllib.request
from google_drive_downloader import GoogleDriveDownloader as gdd


# Download file from a direct url, e.g., "https://github.com/giswqs/whitebox/raw/master/examples/testdata.zip"
def download_from_url(url, file_name='', out_dir='.', unzip = True):
    zip_name = os.path.basename(url)
    zip_path = os.path.join(out_dir, zip_name)   

    print('Downloading {} ...'.format(zip_name))
    urllib.request.urlretrieve(url, zip_path)   
    print('Downloading done.')

    # if it is a zip file
    if '.zip' in zip_name:       
        print("Unzipping {} ...".format(zip_name))
        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            zip_ref.extractall(out_dir)
        print('Unzipping done.')

    # if it is a tar file
    if '.tar' in zip_name:                  
        print("Unzipping {} ...".format(zip_name))
        with tarfile.open(zip_name, "r") as tar_ref:
            tar_ref.extractall(out_dir)
        print('Unzipping done.')
        
    print('Data directory: {}'.format(os.path.splitext(zip_path)[0]))


# Download file shared via Google Drive
def download_from_gdrive(gfile_url, file_name, out_dir='.', unzip = True):
    file_id = gfile_url.split('/')[5]  
    print('Google Drive file id: {}'.format(file_id))

    dest_path = os.path.join(out_dir, file_name) 
    gdd.download_file_from_google_drive(file_id, dest_path, unzip=True)


if __name__ == "__main__":
    url = "https://github.com/giswqs/whitebox/raw/master/examples/testdata.zip"
    download_from_url(url)
    shutil.rmtree('testdata')
    os.remove('testdata.zip')

    gfile_url = 'https://drive.google.com/file/d/1xgxMLRh_jOLRNq-f3T_LXAaSuv9g_JnV'
    download_from_gdrive(gfile_url, 'testdata.zip')
    shutil.rmtree('testdata')
    os.remove('testdata.zip')