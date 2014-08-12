from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty, StringProperty
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
	bl_label = 'Comment block'
	
	border = StringProperty(
			name = 'Border',
			description = "Set the char at border",
			maxlen = 1,
			default = '#',
	)
	
	width = IntProperty(
			name = 'Block width',
			description = "The comment block width in chars",
			min = 0,
			max = 100,
			default = 50,
	)
	
	height = IntProperty(
			name = 'Block height',
			description = "The number of lines between top and bottom borders",
			min = 1,
			step = 2,
			max = 100,
			default = 1,
	)
	
	centered = BoolProperty(
			name = 'Text at center',
			description = "Align the body text at center",
			default = True,
	)

	title = StringProperty(
			name = 'Title',
			description = "The title of comment block",
			maxlen = 50,
			default = '',
	)

	@classmethod
	def poll(self, context):
		return context.area.type == 'TEXT_EDITOR'

	def execute(self, context):
		top_border = '#{}{}{}'.format(
				self.border * ((self.width - len(self.title))// 2),
				self.title,
				self.border * ((self.width - len(self.title))// 2),
		)
		bottom_border = '#{}'.format(self.border * self.width)
		space_line = '#'
		body = '#\t'
		centered_body = '#\t\t'
		
		if self.centered:
			# Just a comment block
			comment_block = '\n'.join(
					[top_border] + 
					[space_line] * (self.height // 2) +
					[centered_body] +
					[space_line] * (self.height // 2) +
					[bottom_border] +
					['']
			)
			
			# Lines between body text and cursor
			lines_to_body = (self.height // 2) + 2
		
		else:
			# An annotation block
			comment_block = '\n'.join(
					[top_border] + 
					[space_line] +
					[body] +
					[space_line] * (self.height - 2) +
					[bottom_border] +
					['']
			)
			# Lines between body text and cursor
			lines_to_body = self.height
		
		code = context.edit_text
		
		bpy.ops.text.move(type='LINE_BEGIN')
		bpy.ops.text.insert(text=comment_block)
		
		for i in range(lines_to_body):
			bpy.ops.text.move(type='PREVIOUS_LINE')
		
		bpy.ops.text.move(type='LINE_END')
		
		return {'FINISHED'}
	

class PYDITOR_OT_insert_bl_info(Operator):
	bl_idname = 'pyditor.insert_bl_info'
	bl_label = 'Insert blender script info'
	bl_description = 'Insert bl_info dictionary at top of the file'
	
	@classmethod
	def poll(self, context):
		return context.area.type == 'TEXT_EDITOR'
	
	def execute(self, context):
		from pyditor_templates import bl_info_template
		
		bpy.ops.text.move(type='FILE_TOP')
		
		if not 'bl_info' in context.edit_text.current_line.body:
			bpy.ops.text.insert(text=bl_info_template.format(
					proj_name = context.edit_text.name,
					bl_version = str(bpy.app.version),
			))
		
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
