import sublime, sublime_plugin
import re



class WordHighlightTestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# for test.
		WordHighlight().on_selection_modified( sublime.active_window().active_view() )
		return
		

class WordHighlight(sublime_plugin.EventListener):
	
	def on_selection_modified( self, view ):
		
		window = sublime.active_window()
		if window is None:
			return
		
		view = window.active_view()
		if view is None:
			return
		
		highlightWord = view.substr( view.sel()[0].a )
		wordSeparator = view.settings().get( "word_separators" )
		
		if not highlightWord in wordSeparator or highlightWord in "<>=+-*/%~^" :
			
			highlightWord = view.substr( view.word( view.sel()[0].a ) )
			highlightWord = highlightWord.lstrip().rstrip()
			
		
		if len(highlightWord) <= 0:
			view.erase_regions( "word_highlight" )
			return
			
		wordRegions = view.find_all( highlightWord, sublime.LITERAL )
		
		if len(wordRegions) <= 0:
			view.erase_regions( "word_highlight" )
			return
		
		# print wordRegions
		view.add_regions( "word_highlight", wordRegions, "invalid", "", sublime.DRAW_OUTLINED )
		
		return
	
	
