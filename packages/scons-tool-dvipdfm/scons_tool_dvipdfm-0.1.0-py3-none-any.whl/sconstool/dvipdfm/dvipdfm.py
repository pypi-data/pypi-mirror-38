"""`SCons.Tool.dvipdfm`

Tool-specific initialization for dvipdfm.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

#
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013 The SCons Foundation
# Copyright (c) 2013 by Pawel Tomulik <ptomulik@meil.pw.edu.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import SCons.Action
import SCons.Builder
import SCons.Defaults
import SCons.Tool
import SCons.Tool.tex
import SCons.Tool.dvipdf
import SCons.Util

def DviPdfmFunction(target = None, source= None, env=None):
    result = SCons.Tool.dvipdf.DviPdfPsFunction(PDFAction,target,source,env)
    return result

def DviPdfmStrFunction(target = None, source= None, env=None):
    """A strfunction for dvipdfm that returns the appropriate
    command string for the no_exec options."""
    if env.GetOption("no_exec"):
        result = env.subst('$DVIPDFMCOM',0,target,source)
    else:
        result = ''
    return result

PDFAction = None
DVIPDFMAction = None
DVIPDFMBuilder = None
DVIPDFMEmitter = SCons.Tool.dvipdf.PDFEmitter

def generate(env):
    """Add Builders and construction variables for dvipdfm to an Environment."""
    global PDFAction
    if PDFAction is None:
        PDFAction = SCons.Action.Action('$DVIPDFMCOM', '$DVIPDFMCOMSTR')

    global DVIPDFMAction
    if DVIPDFMAction is None:
        DVIPDFMAction = SCons.Action.Action(DviPdfmFunction,
                                            strfunction = DviPdfmStrFunction)

    try:
        env['BUILDERS']['DVIPDFM']
    except KeyError:
        global DVIPDFMBuilder
        # DVIPDFMBuilder acts as the PDF builder here. We do this, because
        # the original "suffix rule" '.dvi' -> '.pdf' is already implemented
        # in 'dvipdf' tool and injected into the PDF builder.
        DVIPDFMBuilder = SCons.Builder.Builder(
                            action = {},
                            suffix = '$DVIPDFMSUFFIX',
                            emitter = {},
                            source_scanner = SCons.Tool.PDFLaTeXScanner,
                            source_ext_match = None,
                            single_source = True
        )
        DVIPDFMBuilder.add_action('.dvi', DVIPDFMAction)
        DVIPDFMBuilder.add_emitter('.dvi', DVIPDFMEmitter)
        DVIPDFMBuilder.add_src_builder('DVI')
        env.Append(BUILDERS = {'DVIPDFM' : DVIPDFMBuilder})
        env['DVIPDFM']      = 'dvipdfm'
        env['DVIPDFMFLAGS'] = SCons.Util.CLVar('')
        env['DVIPDFMCOM']   = 'cd ${TARGET.dir} && $DVIPDFM $DVIPDFMFLAGS ' \
                            + '-o ${TARGET.file} ${SOURCE.file}'
        env['DVIPDFMSUFFIX']= '.pdf'

def exists(env):
    SCons.Tool.tex.generate_darwin(env)
    return env.Detect('dvipdfm')

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
