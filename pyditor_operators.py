from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_module, unregister_module
from re import sub
import bpy


#
#		PATTERNS
#
space_chars_ptrn = r'^\s+|\s+$'


#
#		Files navigation button
#
def draw_switcher_button(layout, text):
	label = text.name
	icon = 'NONE'
	
	if text.is_dirty and not text.is_in_memory:
		label = '* %s' % label
	
	if is_active_text(text):
		icon = 'SPACE3'
	
	layout.operator("pyditor.switch_file", text=label, icon=icon).filename = text.name


def is_active_text(text):
	return bpy.context.area.spaces.active.text.name == text.name


class PYDITOR_OT_switch_file(Operator):
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
#		Comment Line operator
#
def is_not_empty_line(line):
	return sub(space_chars_ptrn, '', line.body)


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


class PYDITOR_OT_Comment_line(Operator):
	bl_idname = 'pyditor.comment_line'
	bl_label = 'Add/Remove Comment'
	
	@classmethod
	def poll(self, context):
		return context.area.type == 'TEXT_EDITOR'
	
	def execute(self, context):
		code = context.edit_text
		
		if is_commented(code.current_line):
			uncomment_line(code.current_line)
		elif is_not_empty_line(code.current_line):
			comment_line(code.current_line)

		return {'FINISHED'}


#
#		Comment Block
#
class PYDITOR_OT_Comment_block(Operator):
	bl_idname = 'pyditor.paste_an_comment_block'
	bl_label = 'Paste a simple comment block'
	border_char = StringProperty()
	
	@classmethod
	def poll(self, context):
		return context.area.type == 'TEXT_EDITOR'

	def execute(self, context):
		border = '#{}'.format(self.border_char*40)
		center = '#\t\t'
		code = context.edit_text
		
		bpy.ops.text.move(type='LINE_BEGIN')
#		code.write('\n'.join((border, center, border, '')))
		bpy.ops.text.insert(text='\n'.join((border, center, border, '')))
		bpy.ops.text.move(type='PREVIOUS_LINE')
		bpy.ops.text.move(type='PREVIOUS_LINE')
		bpy.ops.text.move(type='LINE_END')
		
		return {'FINISHED'}
	

#
#		Make it as add-on
#
def register():
	register_module(__name__)


def unregister():
	unregister_module(__name__)


if __name__ == "__main__":
	unregister()
	register()
