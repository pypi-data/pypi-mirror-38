#!/usr/bin/env python
# $BEGIN_SHADY_LICENSE$
# 
# This file is part of the Shady project, a Python framework for
# real-time manipulation of psychophysical stimuli for vision science.
# 
# Copyright (C) 2017-18  Jeremy Hill, Scott Mooney
# 
# Shady is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/ .
# 
# $END_SHADY_LICENSE$

#: How to add "foreign" (non-Shady) stimuli to a World
"""
DOC-TODO
"""#.
if __name__ == '__main__':

	"""
	First deal with the demo's command-line arguments,
	if any:
	"""#:
	import Shady
	cmdline = Shady.WorldConstructorCommandLine()
	cmdline.Help().Finalize()
	
	"""
	Create a World:
	"""#:
	w = Shady.World( clearColor=[ 0.5, 0.5, 0.5 ], **cmdline.opts )
	Shady.FrameIntervalGauge( w )
	
	"""
	DOC-TODO
	"""#:
	
	from OpenGL.GLUT import *
	from OpenGL.GLU import *
	from OpenGL.GL import *

	@w.Defer
	def Setup():		
			glEnable( GL_LIGHTING )
			glEnable( GL_LIGHT0 )
			glEnable( GL_LIGHT3 )
			
	class CustomStimulus( object ):
	
		def draw( self ):
			glEnable( GL_LIGHTING )
			glEnable( GL_LIGHT0 )
			
			#glMatrixMode( GL_PROJECTION ); glPushMatrix()
			glMatrixMode( GL_MODELVIEW )
			glPushMatrix()
			
			glLightfv( GL_LIGHT0,   GL_POSITION, ( GLfloat * 4 )( 1.0, 1.0, 0.0, 0.0 ) )
			glLightfv( GL_LIGHT0,   GL_AMBIENT,  ( GLfloat * 4 )( 1.0, 0.0, 0.0, 1.0 ) )
			glLightfv( GL_LIGHT0,   GL_DIFFUSE,  ( GLfloat * 4 )( 0.0, 1.0, 0.0, 1.0 ) )
			
			glScalef( 1.0, 1.0, 2.0 / w.width )
			glTranslatef( w.width/2, w.height/2, 0.5 )
			glRotatef( 23.0 * w.t, 1.0, 0.0, 0.0 )
			glRotatef( 31.0 * w.t, 0.0, 1.0, 0.0 )
			
			glMaterialfv( GL_FRONT, GL_AMBIENT,  ( GLfloat * 4 )( 1.0, 1.0, 1.0, 1.0 ) )
			glMaterialfv( GL_BACK,  GL_AMBIENT,  ( GLfloat * 4 )( 1.0, 1.0, 1.0, 1.0 ) )
			glMaterialfv( GL_FRONT, GL_DIFFUSE,  ( GLfloat * 4 )( 1.0, 1.0, 1.0, 1.0 ) )
			glMaterialfv( GL_BACK,  GL_DIFFUSE,  ( GLfloat * 4 )( 1.0, 1.0, 1.0, 1.0 ) )
			
			glutSolidCube( 100 )
			glPopMatrix()
			#glMatrixMode( GL_PROJECTION ); glPopMatrix()
			
	w.AddForeignStimulus( CustomStimulus(), z=0 )	
	""#>
	Shady.AutoFinish( w ) # tidy up, in case we're not running this with `python -m Shady`