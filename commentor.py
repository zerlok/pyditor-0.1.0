bl_info = {
		'name' : 'Simple commentator',
		'author' : 'Danil Troshnev',
		'version' : (0, 1, 0),
		'blender' : (2, 71, 0),
		'location' : 'Text Editor > Edit > Add/Remove Comment',
		'description' : 'This script is better than internal. It creates comment and remove it if it was.',
		'warning' : 'It\'s my first blender script!',
		'wiki_url' : '',
		'tracker_url' : '',
		'support' : 'TESTING',
		'category' : 'Development',
}


from bpy.types import Operator, TEXT_MT_edit
from bpy.utils import register_module, unregister_module


#
#	main functions
#
def is_commented(line):
	return line.body.startswith('#')


def comment_line(line):
	text = line.body

	if text.startswith('\t'):
		line.body = '#{}'.format(text)
	elif text.startswith(' '*2):
		line.body = '#{}'.format(text[1:])
	else:
		line.body = '# {}'.format(text)
	return {'FINISHED'}


def uncomment_line(line):
	text = line.body
	
	if text.startswith('#\t'):
		line.body = text[1:]
	elif text.startswith('#  '):
		line.body = ' {}'.format(text[1:])
	else:
		line.body = text[2:]
	return {'FINISHED'}


#
#	comment button
#
class TEXT_MT_CommentButton(Operator):
	bl_idname = "text.comment_line"
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


def comment_line_button(self, context):
	self.layout.operator("text.comment_line",
			text="Add/Remove Comment",
		)


#
#	Make it as add-on
#
def register():
	register_module(__name__)
	TEXT_MT_edit.prepend(comment_button)


def unregister():
	unregister_module(__name__)
	TEXT_MT_edit.remove(comment_button)


if __name__ == "__main__":
	register()

