#!/usr/bin/env python

import color

class PPrint( object ):

	def lprint( self, *args, **kwargs  ):
		return self.pprint( *args, **kwargs ).lstrip()

	def pprint( self, marker='*' ):
		return ' {blue}[{purple}{marker}{blue}]{green} {{}}' \
				.format(blue=color.BLUE,
						purple=color.PURPLE,
						green=color.GREEN,
						marker=marker)

	def aprint( self, align=0, marker='*' ):
		return ' {blue}[{purple}{marker}{blue}]{green} {{:<{align}}} '\
				'{purple}-{green} {{}}'.format( blue=color.BLUE,
												purple=color.PURPLE,
												green=color.GREEN,
												align=align,
												marker=marker )

	def sprint( self ):
		return ' {blue}--[{purple} {{}}{green} '.format(blue=color.BLUE, 
														purple=color.PURPLE,
														green=color.GREEN)

	def fprint( self, align=0 ):
		return ' {blue}--[{purple} {{:<{align}}}{blue} ]:{green} {{}} '\
				.format(blue=color.BLUE,
						purple=color.PURPLE,
						green=color.GREEN,
						align=align)

	def cprint( self ):
		return '{}{{}}'.format( color.GREEN )
