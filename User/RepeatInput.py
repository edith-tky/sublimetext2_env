import sublime, sublime_plugin


class RepeatInputCommand(sublime_plugin.WindowCommand):
	
	def eraseErrorMessage( self ):
		print "here"
		view = sublime.active_window().active_view()
		view.erase_status( "repeat_input_message" )
		return
	
	def errorMessage( self, str ):
		view = sublime.active_window().active_view()
		view.set_status( "repeat_input_message", str )
		sublime.set_timeout( self.eraseErrorMessage, 2500 )
		
	
	def showInputPanel_onDone( self, str ):
		
		if "/" not in str:
			self.errorMessage( "invalid string \"" + str + "\"" )
			self.showInputPanel( str )
			return
		
		inputs = str.split( "/" )
		
		base = inputs[0]
		ranges = inputs[1].split( "," )
		
		for i in range( 0,len(ranges) ):
			ranges[i] = int(ranges[i])
			
		inputRangeParamCount = len(ranges)
		
		while len(ranges) < 3:
			ranges.append(0)
		
		begin, end, step = tuple( ranges )
		
		if inputRangeParamCount > 1:
			
			rangeSign = ( end - begin ) > 0
			stepSign = step >= 0
			
			if step == 0:
				stepSign = rangeSign
				step = 1
			
			if rangeSign != stepSign:
				step = -step
			
			end += step
			
		else:
			# count
			
			end = begin + 1
			begin = 1
			step = 1
			
		print begin, end, step
		
		output = ""
		for i in range( begin, end, step ):
			num = u"%d" % i
			tmp = base.replace( "##", num )
			output += tmp
			
		
		view = sublime.active_window().active_view()
		edit = view.begin_edit()
		view.insert( edit, view.sel()[0].a, output )
		
		# add history.
		histories = []
		if view.settings().has( "repeat_input" ):
			histories = view.settings().get( "repeat_input" )
		
		if str in histories:
			histories.remove(str)
		
		histories.append( str )
		
		if len( histories ) > 10:
			del histories[0]
		
		view.settings().set( "repeat_input", histories )
		
		return
		
		
	def showInputPanel( self, defaultString ):
		
		window = sublime.active_window()
		view = window.active_view()
		if view is None:
			return
		
		window.show_input_panel( "repeat input. ex) \"input string ( ## is replaced numeric ) / ( count | begin [ , end [ , step ] ] )\"", defaultString, self.showInputPanel_onDone, None, None )
		
		
	def showQuickPanel_onDone( self, index ):
		
		window = sublime.active_window()
		view = window.active_view()
		if view is None:
			return
		
		if index < 0:
			self.showInputPanel( "" )
		else:
			histories = view.settings().get( "repeat_input" )
			histories.reverse()
			self.showInputPanel( histories[index] )
		
		
	def showQuickPanel( self ):
		
		window = sublime.active_window()
		view = window.active_view()
		if view is None:
			return
		
		histories = view.settings().get( "repeat_input" )
		histories.reverse()
		window.show_quick_panel( histories, self.showQuickPanel_onDone )
		
		
		
	def run(self):
		
		window = sublime.active_window()
		view = window.active_view()
		if view is None:
			return
		
		if view.settings().has( "repeat_input" ):
			self.showQuickPanel()
		else:
			self.showInputPanel( "" )
		
		return
		
		
