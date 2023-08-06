# pyforms generic editor

**pyforms generic editor** offers a easy way to bootstrap projects that make use of pyforms. 

Often, one need to create a GUI with a main window which follows a typical structure: mdi area to open windows, one left dock window (top) to display tree-like information and a left dock window (bottom) to display details depending on the resources selected on the tree. 

Moreover, this main window typical offers a set of top menus to organize windows, display app help & info, etc. 

By using this generic editor one avoids repeated code by offering a template that can then be extended with more features depeding on a specific app.

![main window](https://bytebucket.org/fchampalimaud/pyforms-generic-editor/raw/60375326743c094dc0d86548e7b3e4269d58f2e6/main_window.png)


| Info   |      Pic      |
|----------|:-------------:|
| Menu About offers info about python, software and libraries version| ![menu about](https://bytebucket.org/fchampalimaud/pyforms-generic-editor/raw/60375326743c094dc0d86548e7b3e4269d58f2e6/menu_about.png) |
| Menu Window offers basic actions to perform on windows opened in the mdi area |    ![menu window](https://bytebucket.org/fchampalimaud/pyforms-generic-editor/raw/60375326743c094dc0d86548e7b3e4269d58f2e6/menu_window.png) |



## Try it

From inside the project folder run:

	python -m pyforms_generic_editor

## How to use in other projects

**pyforms generic editor** needs pyforms to run. The most simple form to use it and extend it is shown in the example below. Just create a class which extends from BaseEditor and pass it to the startApp method of pyforms.
	
	from pyforms_generic_editor.editor.base_editor import BaseEditor
	import pyforms
	
	class Editor(BaseEditor):
		def __init__(self):
			# do something here when project is loading	
			super(Editor, self).__init__()
	
		def initForm(self):
			super(Editor, self).initForm()
	
			# do something here after project is loaded
	
	def start(): 
		pyforms.startApp(Editor)


	if __name__ == '__main__': 
		start()