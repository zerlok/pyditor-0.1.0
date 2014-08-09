from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_module, unregister_module
import bpy


#
#	Files navigation button
#
def is_active_text(text, context):
	return context.area.spaces.active.text.name == text.name


class PYDITOR_OT_file_switcher_button(Operator):
	bl_idname = "pyditor.switch_file"
	bl_label = "Button"
	filename = StringProperty()
	
	@classmethod
	def poll(self, context):
		return context.area.type == 'TEXT_EDITOR'
	
	def execute(self, context):
		space = context.area.spaces.active
		
		space.text = bpy.data.texts[self.filename]
		
		return {'FINISHED'}


#
#	Comment Line operator
#
def is_commented(line):
	return line.body.startswith('#')


def comment_line(line):
	text = line.body

	if text.startswith('\t'):
		line.body = '#{}'.format(text)
		bpy.ops.text.move(type='NEXT_CHARACTER')

	elif text.startswith(' '*2):
		line.body = '#{}'.format(text[1:])

	else:
		line.body = '# {}'.format(text)

	return {'FINISHED'}


def uncomment_line(line):
	text = line.body
	
	if text.startswith('#\t'):
		line.body = text[1:]
		bpy.ops.text.move(type='PREVIOUS_CHARACTER')
	
	elif text.startswith('#  '):
		line.body = ' {}'.format(text[1:])
	
	else:
		line.body = text[2:]

	return {'FINISHED'}


#	comment button
class PYDITOR_OT_Comment_line(Operator):
	bl_idname = "pyditor.comment_line"
	bl_label = "Add/Remove Comment"
	
	@classmethod
	def poll(self, context):
		return context.area.type == 'TEXT_EDITOR'
	
	def execute(self, context):
		code = context.edit_text
		
		if is_commented(code.current_line):
			uncomment_line(code.current_line)
		else:
			comment_line(code.current_line)

		return {'FINISHED'}


def register():
	register_module(__name__)


def unregister():
	unregister_module(__name__)


if __name__ == "__main__":
	unregister()
	register()
