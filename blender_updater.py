bl_info = {
	'name' : 'Blender Updates Checker',
	'author' : 'Danil Troshnev (denergytro@gmail.com)',
	'version' : (0, 1, 0),
	'blender' : (2, 71, 0),
	'location' : 'User Settings > System > Check for Updates',
	'description' : "\
This script checks is the current version of blender the last.\
Install function will be available soon...",
	'warning' : 'Was not tested on OSX systems',
	'wiki_url' : '',
	'tracker_url' : '',
	'support' : 'TESTING',
	'category' : 'System',
}


import bpy

from ftplib import FTP
from re import compile, match
from platform import platform, machine
from os.path import exists


#
#		The official ftp url
#
FTP_URL = 'ftp.nluug.nl'
FTP_DIR = 'pub/graphics/blender/release'


#
#		Regex Patterns
#
bl_dir_ptrn = compile(r'Blender(\d)\.(\d+)(-?\w*)')


#
#		Main Functions
#
def get_all_blender_versions_list(ftp):
	'''Returns the list of all blender versions from ftp'''
	bl_versions_lst = []
	dirs_lst = []
	
	ftp.retrlines('NLST', callback=lambda x: dirs_lst.append(x))
	
	for dirname in dirs_lst:
		mo=match(bl_dir_ptrn, dirname)
		
		if mo:
			bl_versions_lst.append((
					int(mo.group(1)),
					int(mo.group(2)),
					mo.group(3),
			)) # (ver, subver, sub)
	
	return bl_versions_lst
	

def get_upper_versions_list(bl_versions):
	'''Returns the list of all upper versions then current version of blender'''
	if bpy.app.version[2] == 0:
		current_version = (bpy.app.version[0], bpy.app.version[1], '')
	else:
		current_version = (bpy.app.version[0], bpy.app.version[1], str(bpy.app.version[2]))
	
	return [bl_ver for bl_ver in bl_versions if bl_ver > current_version]


def get_blender_files_list(bl_ver, ftp):
	'''Returns the files list of indicated version at ftp'''
	version_dir = 'Blender{}.{}{}'.format(bl_ver[0], bl_ver[1], bl_ver[2])
	ftp.cwd(version_dir)
		
	files_lst = []
	ftp.retrlines('NLST', callback=lambda x: files_lst.append(x))
	
	return filter_blenders_versions(files_lst)


def filter_blenders_versions(files_lst):
	'''Filters the files list for current operating system at current machine'''
	os_name = platform().lower()[:2] # First 3 letters of os name
	files_lst = [bl_file for bl_file in files_lst if os_name in bl_file] # Only for current operating system

	os_mach = machine() # (32 bit / 64 bit)
	files_lst = [bl_file for bl_file in files_lst if os_mach in bl_file] # Only for current machine
	
	return files_lst


#
#		Downloader in Dev!
#
def download_blender_file(filename, ftp):
	filepath = bpy.app.tempdir + filename
	
	if not exists(filepath):
		with open(filepath, 'wb') as bl_file:
			result = ftp.retrbinary('RETR %s' % filename, callback=bl_file.write)
	
		return filepath if result == '226 Transfer complete.' else result
	else:
		return "%s already exists" % filepath


#
#		Installer in Dev!
#
def install_blender(filepath, os_name):
	pass


#
#		Update Checker class
#
class USERPREF_OT_blender_updater(bpy.types.Operator):
	'''Class of Update Checker operator'''
	bl_idname = "program.check_for_updates"
	bl_space_type = 'USER_PREFERENCES'
	bl_region_type = 'WINDOW'
	bl_label = "Updates Checker"
	
	@classmethod
	def poll(self, context):
		return context.user_preferences.active_section == 'SYSTEM'	

	def execute(self, context):
		# Connect to ftp server
		ftp = FTP(FTP_URL)
		ftp.login()
		ftp.cwd(FTP_DIR)
		# TODO: Except 'No connection' error
		
		# Get versions list
		bl_versions_lst = get_all_blender_versions_list(ftp) # All Blender versions at ftp url
		# Check for higher versions of blender
		higher_versions_lst = get_upper_versions_list(bl_versions_lst) # Upper versions
		
		if higher_versions_lst:
			self.report({'INFO'}, "New versions of Blender are available!")
			# TODO: Make chooser
			# TODO: Run Downloader
		else:
			self.report({'INFO'}, "You already have a highest version of Blender %s" % bpy.app.version_string)

		return {'FINISHED'}


#
#		Button drawer
#
def draw_updates_checker(self, context):
	layout = self.layout
	row = layout.row()
	row.alignment = 'LEFT'
	row.operator("program.check_for_updates", text='Check for new versions', icon='FILE_REFRESH')


#
#		Make it as add-on
#
def register():
	bpy.utils.register_class(USERPREF_OT_blender_updater)
	bpy.types.USERPREF_PT_system.append(draw_updates_checker)


def unregister():
	bpy.utils.unregister_class(USERPREF_OT_blender_updater)
	bpy.types.USERPREF_PT_system.remove(draw_updates_checker)


if __name__ == "__main__":
	register()

