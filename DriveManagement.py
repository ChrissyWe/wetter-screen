from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime, timedelta


""" this class was for writing and reading files on google drive. eventually only worked on windows, not linux. 
So the class was not used in the end and remains only if someone wants to keep trying on it. """


#file = drive.CreateFile({'id': '1H2gFWfNR_tKqlj7HGooZQZy9iZOC-QLt'})
#content_string = file.getContentString()

#print(content_string)
def writeExcel():
	datetime.today()
	gauth = GoogleAuth(settings_file='/wetter-screen/driveData/settings.yaml')
	# gauth.DEFAULT_SETTINGS['client_config_file'] = 'C:\\Users\\Chris\\Documents\\Semester_8\\Bundesgartenschau\\gdrive-credentials.json'
	drive = GoogleDrive(gauth)
	file = drive.CreateFile({'title': f'{datetime.today().date() - timedelta(days=1)}_Temperatures', 'parents': [{'id': '1NggFkhUZ1LmAEObTvGU7H9sfLc9QKW-B'}]})
	file.SetContentFile(f"/wetter-screen/Data/{datetime.today().date() - timedelta(days=1)}_Temperatures")
	file.Upload()

#file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('1NggFkhUZ1LmAEObTvGU7H9sfLc9QKW-B')}).GetList()
#for file in file_list:
#	print('title: %s, id: %s' % (file['title'], file['id']))

def getContent():
	gauth = GoogleAuth(settings_file='/wetter-screen/driveData/settings.yaml')
	# gauth.DEFAULT_SETTINGS['client_config_file'] = 'C:\\Users\\Chris\\Documents\\Semester_8\\Bundesgartenschau\\gdrive-credentials.json'
	drive = GoogleDrive(gauth)
	file = drive.CreateFile({'id': '1MUtalibYpvJ1FBHQGzDC4wEW19xL0wZw'})
	content = file.GetContentString()
	return content

#file = drive.CreateFile({'id': '1NggFkhUZ1LmAEObTvGU7H9sfLc9QKW-B'})
#file.GetContentFile('test.txt')