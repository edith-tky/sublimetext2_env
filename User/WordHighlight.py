import sublime, sublime_plugin
import re



class WordHighlightTestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# for test.
		WordHighlight().on_selection_modified( sublime.active_window().active_view() )
		return
		

class WordHighlight(sublime_plugin.EventListener):
	
	def eraseHighlight( self, view ):
		view.erase_regions( "word_highlight" )
		view.erase_regions( "word_highlight_original" )
	
	def on_selection_modified( self, view ):
		
		window = sublime.active_window()
		if window is None:
			return
		
		view = window.active_view()
		if view is None:
			return
		
		if not view.settings().has( "word_highlight_enabled" ):
			self.eraseHighlight( view )
			return
		
		
		baseRegion = view.sel()[0]
		highlightWord = view.substr( baseRegion.a )
		wordSeparator = view.settings().get( "word_separators" )
		
		if highlightWord not in wordSeparator or highlightWord in "<>=+-*/%~^" :
			
			baseRegion = view.word( view.sel()[0].a )
			highlightWord = view.substr( baseRegion )
			highlightWord = highlightWord.lstrip().rstrip()
			
		
		
		if len(highlightWord) <= 0:
			self.eraseHighlight( view )
			return
			
		wordRegions = []
		if len(highlightWord) == 1:
			
			if highlightWord not in "<>":
				escaped = re.escape( highlightWord )
				patern = escaped + "+"
			else:
				patern = highlightWord + "+"
			
			wordRegions = view.find_all( patern )
			
		else:
			wordRegions = view.find_all( highlightWord, sublime.LITERAL )
		
		if len(wordRegions) <= 0:
			self.eraseHighlight( view )
			return
		# ...
		# print wordRegions
		highlight_color = ""
		if view.settings().has( "word_highlight_color_score" ):
			highlight_color = view.settings().get( "word_highlight_color_score" )
		
		# print highlight_color
		view.add_regions( "word_highlight", wordRegions, highlight_color, "", sublime.DRAW_OUTLINED )
		
		if view.settings().has( "word_highlight_original_color_score" ):
			original_color = view.settings().get( "word_highlight_original_color_score" )
			
			reg = view.find( highlightWord, baseRegion.a, sublime.LITERAL )
			view.add_regions( "word_highlight_original", [reg], original_color, "", sublime.DRAW_OUTLINED )
			
		
		return
	
	
