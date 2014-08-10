bl_info = {
		'name' : 'Pyditor (Enhanced Text Editor)',
		'author' : 'Danil Troshnev (denergytro@gmail.com)',
		'version' : (0, 0, 1),
		'blender' : (2, 71, 0),
		'location' : 'Text Editor',
		'description' : "\
This script replace 'Text Editor' to 'Pyditor'.\
This text editor was made for python scripts with same environment as in 'Eclipse'.",
		'warning' : '',
		'wiki_url' : '(in development)',
		'tracker_url' : '',
		'support' : 'TESTING',
		'category' : 'Development',
}


from bpy.types import Header, Menu, Panel
import bpy

import pyditor_operators as py_ops


#
#   	Editor header
#
class PYDITOR_HT_header(Header):
	bl_space_type = 'TEXT_EDITOR'
	bl_idname = 'TEXT_HT_header' # Here I replaced the header in Text Editor
	
	def draw(self, context):
		layout = self.layout
		
		# Main Menu
		row = layout.row(align=True)
		row.template_header()
		
		# Pysitor menu
		PYDITOR_MT_header_menus.draw_collapsible(context, layout)


class PYDITOR_MT_header_menus(Menu):
	bl_idname = "PYDITOR_MT_header_menus"
	bl_label = ""
	
	def draw(self, context):
		self.draw_menus(self.layout, context)
	
	@staticmethod
	def draw_menus(layout, context):
		layout.menu("PYDITOR_MT_file")
		layout.menu("PYDITOR_MT_edit")
		layout.menu("PYDITOR_MT_source")
		layout.menu("PYDITOR_MT_navigate")
		layout.menu("PYDITOR_MT_search")
		layout.menu("PYDITOR_MT_project")
		layout.menu("PYDITOR_MT_run")
		layout.menu("PYDITOR_MT_window")
		layout.menu("PYDITOR_MT_help")


class PYDITOR_MT_file(Menu):
	bl_idname = "PYDITOR_MT_file"
	bl_label = "File"
	
	def draw(self, context):
		layout = self.layout
		st = context.space_data
		text = st.text

		layout.operator("text.new", text="New", icon="FILE_BLANK")
		layout.operator("text.open", text="Open", icon="FILESEL")

		if text:
			layout.column()
			layout.operator("text.save")
			layout.operator("text.save_as")
			
			layout.separator()
			layout.operator("text.reload", text="Reload", icon="FILE_REFRESH")

			if text.filepath:
				layout.operator("text.make_internal")


class PYDITOR_MT_edit(Menu):
	bl_idname = "PYDITOR_MT_edit"
	bl_label = "Edit"
	
	def draw(self, context):
		self.layout.label(self.bl_label)
	
		
class PYDITOR_MT_source(Menu):
	bl_idname = "PYDITOR_MT_source"
	bl_label = "Source"
	
	def draw(self,context):
		layout = self.layout
		
		col = layout.column()
		col.label(self.bl_label)
		
		col.separator()
		
		col.operator("pyditor.comment_line", text="Toggle comment line")
		col.operator("pyditor.paste_an_comment_block", text="Create comment block").border_char = '-'


class PYDITOR_MT_navigate(Menu):
	bl_idname = "PYDITOR_MT_navigate"
	bl_label = "Navigate"
	
	def draw(self, context):
		layout = self.layout
		col = layout.column()
		
		for text in bpy.data.texts:
			py_ops.draw_switcher_button(col, text)


class PYDITOR_MT_search(Menu):
	bl_idname = "PYDITOR_MT_search"
	bl_label = "Search"
	
	def draw(self, context):
		self.layout.label(self.bl_label)
#	   self.layout.template_list(context.scene, 'my_list', context.scene, 'my_list_index', rows= 3)


class PYDITOR_MT_project(Menu):
	bl_idname = "PYDITOR_MT_project"
	bl_label = "Project"
	
	def draw(self, context):
		self.layout.label(self.bl_label)


class PYDITOR_MT_run(Menu):
	bl_idname = "PYDITOR_MT_run"
	bl_label = "Run"
	
	def draw(self, context):
		layout = self.layout
		text = context.space_data.text
		flow = layout.column_flow()
		
		if text.name.endswith('.py'):
			flow.operator("text.run_script", text="Run")
			flow.label("Run Cofigurations...")

			flow.separator()

			flow.label("Debug")


class PYDITOR_MT_window(Menu):
	bl_idname = "PYDITOR_MT_window"
	bl_label = "Window"
	
	def draw(self, context):
		self.layout.label(self.bl_label)


class PYDITOR_MT_help(Menu):
	bl_idname = "PYDITOR_MT_help"
	bl_label = "Help"
	
	def draw(self, context):
		layout = self.layout
		flow = layout.column_flow()
		
		flow.label(bl_info['name'])
		flow.label("ver %s.%s.%s" % bl_info['version'])


#
#   	Side panels
#
class PYDITOR_PT_browser(Panel):
	bl_idname = 'TEXT_PT_properties'
	bl_space_type = 'TEXT_EDITOR'
	bl_region_type = 'UI'
	bl_label = "Project Browser"
	
	def draw(self, context):
		layout = self.layout


def TEXT_PT_find(Panel):
	bl_idname = 'TEXT_PT_find'
	bl_space_type = 'TEXT_EDITOR'
	bl_region_type = 'UI'
	bl_label = ""

	def draw(self, context):
		layout = self.layout
		
		layout.label("huichishe")


#
#		Make it as add-on
#
def register():
	bpy.utils.register_module(__name__)
	bpy.utils.register_module(py_ops.__name__)


def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.utils.unregister_module(py_ops.__name__)


if __name__ == "__main__":
	unregister()
	register()

