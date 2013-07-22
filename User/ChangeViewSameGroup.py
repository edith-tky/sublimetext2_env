import sublime, sublime_plugin

class ChangeViewSameGroupCommand(sublime_plugin.WindowCommand):
	def run(self,order):
		# self.view.insert(edit, 0, "Hello, World!")
		
		myWindow = sublime.active_window()
		myView = myWindow.active_view()
		
		myGroup, myIndex = myWindow.get_view_index( myView )
		
		sameGroupViews = []
		for view in myWindow.views():
			group, index = myWindow.get_view_index( view )
			
			if group == myGroup:
				while len(sameGroupViews) <= index: sameGroupViews.append(-1)
				sameGroupViews[index] = view
				
		
		nextIndex = myIndex
		if order == "next":
			nextIndex += 1
			if nextIndex >= len( myWindow.views_in_group(myGroup) ):
				nextIndex = 0
		
		elif order == "prev":
			nextIndex -= 1
			if nextIndex < 0:
				nextIndex = len( myWindow.views_in_group(myGroup) ) - 1
		
		myWindow.focus_view( sameGroupViews[nextIndex] )
		
		
