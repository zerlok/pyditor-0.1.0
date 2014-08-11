bl_info = {
	'name' : 'Updater',
	'author' : 'Danil Troshnev (denergytro@gmail.com)',
	'version' : (0, 1, 0),
	'blender' : (2, 71, 0),
	'location' : 'User Settings >',
	'description' : "\
This script checks the current blender version with others versions at ftp.\
If there are upgraded versions, it downloads and installs them.",
	'warning' : 'Was not tested on OSX systems',
	'wiki_url' : '(in development)',
	'tracker_url' : '',
	'support' : 'TESTING',
	'category' : 'System',
}


import ftplib
import re
import platform
import bpy


FTP_URL = 'ftp.nluug.nl'
FTP_DIR = 'pub/graphics/blender/release'


bl_dir_ptrn = re.compile(r'Blender(\d)\.(\d+)(-?\w*)')


def download_version(bl_ver, bl_sub):
	download_dir = 'Blender{}.{}{}'.format(bl_ver[0], bl_ver[1], bl_sub)
	print("Gonna download from '%s' dir" % download_dir)
	return None


def get_upper_versions(bl_versions, bl_subs):
	return [bl_ver for bl_ver in bl_versions if bl_ver > bpy.app.version[:2]]


def get_blender_versions(furl=FTP_URL, fdir=FTP_DIR):
	ftp = ftplib.FTP(furl)
	ftp.login()
	ftp.cwd(fdir)
	
	bl_versions_lst = []
	bl_subs_lst = []
	dirs_lst = []
	
	ftp.retrlines('NLST', callback=lambda x: dirs_lst.append(x))
	
	for dirname in dirs_lst:
		mo=re.match(bl_dir_ptrn, dirname)
		
		if mo:
			bl_versions_lst.append((
					int(mo.group(1)),
					int(mo.group(2)),
			)) # (ver, subver)
			bl_subs_lst.append(mo.group(3)) # sub
	
	return bl_versions_lst, bl_subs_lst


def register():
	pass


def unregister():
	pass


if __name__ == "__main__":
	register()
	bl_versions = get_blender_versions() # All Blender versions at ftp url
	higher_versions = get_upper_versions(*bl_versions) # Upper versions
	print(higher_versions)
#	download_version(bl_versions[0][7], bl_versions[1][])
