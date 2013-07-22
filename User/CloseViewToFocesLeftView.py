import sublime, sublime_plugin

class CloseViewToFocusLeftViewCommand(sublime_plugin.WindowCommand):
	def run(self):
		
		myWindow = sublime.active_window()
		myView = myWindow.active_view()
		
		myGroup, myIndex = myWindow.get_view_index( myView )
		
		sameGroupViews = []
		for view in myWindow.views():
			group, index = myWindow.get_view_index( view )
			
			if group == myGroup:
				while len(sameGroupViews) <= index: sameGroupViews.append(-1)
				sameGroupViews[index] = view
		
		nextIndex = myIndex - 1
		if nextIndex < 0:
			nextIndex = 0
		
		myWindow.run_command( "close_file" )
		myWindow.focus_view( sameGroupViews[nextIndex] )
		
		
