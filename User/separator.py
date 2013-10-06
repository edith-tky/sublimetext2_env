

import sublime, sublime_plugin
import re
import sys

# for import comment.
defaultPath = sublime.packages_path() + "\Default"
if sys.path.count( defaultPath ) == 0:
	sys.path.append( defaultPath )

import comment


class SeparatorCommand(sublime_plugin.WindowCommand):
	
	
	def getSeparatorTypes( self ):
		
		ret = ["-"]
		
		view = sublime.active_window().active_view() if sublime.active_window() else None
		if view is None:
			return ret
		
		if view.settings().has( "separator_type" ):
			ret = view.settings().get( "separator_type" )
			
		else:
			# default types.
			ret = [ "-", "=", "*", "/", "~" ]
		
		return ret
		
	
	def makeSeparator( self, size ):
		
		view = sublime.active_window().active_view()
		
		global comment
		line_comments = comment.build_comment_data( view, view.sel()[0].a )[0]
		
		lineComment = line_comments[0][0].strip()
		ret = []
		separatorTypes = self.getSeparatorTypes()
		for i in range( 0, len( separatorTypes ) ):
			
			addComment = lineComment + separatorTypes[i] * size
			ret.append( addComment )
			
		
		return ret
		
	
	def makeQuickPanelItem( self, default ):
		
		items = self.makeSeparator(5)
		
		for i in range( 0, len(items) ):
			
			items[i] = str(i) + " : " + items[i]
			
		
		itemsWithIndex = [ (items.index(x),x) for x in items ]
		itemsWithIndex.append( ( len(itemsWithIndex), "z : undo" ) )
		itemsWithIndex.append( ( len(itemsWithIndex), "r : redo" ) )
		itemsWithIndex.sort( cmp = lambda x, y: self.sortItemProcess(default,x,y) )
		
		return [ x[1] for x in itemsWithIndex ]
		
	
	def onDoneSelector( self, default, index ):
		
		if index < 0:
			return
		
		view = sublime.active_window().active_view() if sublime.active_window() else None
		if view is None:
			return
		
		# select index. 
		items = self.makeQuickPanelItem(default)
		separatorTypeIndex = -1
		mode = "None"
		match = re.search( "^([0-9rz]+)", items[index] )
		if match:
			if match.group(1) == "z":
				separatorTypeIndex = len(items) - 2
				mode = "undo"
				
			elif match.group(1) == "r":
				separatorTypeIndex = len(items) - 1
				mode = "redo"
				
			else:
				separatorTypeIndex = int( match.group(1) )
				mode = "comment"
			
		
		# process
		if mode == "undo":
			
			# undo.
			view.window().run_command( "undo" )
			
		elif mode == "redo":
			
			# redo.
			view.window().run_command( "redo" )
			
		elif separatorTypeIndex >= 0:
			
			# insert separator.
			r, c = view.rowcol( view.sel()[0].begin() )
			linehead = view.text_point( r, 0 )
			indentString = view.substr( sublime.Region( linehead, view.sel()[0].begin() ) )
			
			tabSize = view.settings().get( "tab_size" )
			tab = tabSize
			indentLength = 0
			for char in indentString:
				
				if char == "\t":
					indentLength += tab
					tab = tabSize
					
				else:
					indentLength += 1
					
					tab -= 1
					if tab <= 0:
						tab = tabSize
			
			global comment
			line_comments = comment.build_comment_data( view, view.sel()[0].a )[0]
			commentLength = len( line_comments[0][0].strip() )
			
			separatorLength = 80
			if view.settings().has( "separator_length" ):
				separatorLength = view.settings().get( "separator_length" )
				
			lengthRate = 1.0
			if len( self.getSeparatorTypes()[separatorTypeIndex].encode( "UTF-8" ) ) > 1:
				lengthRate = 0.5
			
			separators = self.makeSeparator( int( ( separatorLength - commentLength - indentLength ) * lengthRate ) )
			
			addString = separators[separatorTypeIndex] + "\n" + indentString
			
			edit = view.begin_edit( "separator", None )
			view.insert( edit, view.sel()[0].begin(), addString )
			view.end_edit( edit )
			
		
		# continue process.
		self.openSelector( separatorTypeIndex )
		
		return
	
	def sortItemProcess( self, default, x, y ):
		
		ret = 0
		if x[0] == default:
			ret = -1
		elif y[0] == default:
			ret = 1
		else:
			ret = cmp(x,y)
		
		return ret
		
	
	def openSelector( self, default = 0 ):
		
		window = sublime.active_window()
		if window is None:
			return
		
		items = self.makeQuickPanelItem(default)
		
		window.show_quick_panel( items, lambda index : self.onDoneSelector(default,index), sublime.MONOSPACE_FONT )
		
		
		
		return
		
	
	def run(self):
		
		self.openSelector()
		
		

