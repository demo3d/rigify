#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

import bpy
import imp
from .. import super_limb
from .  import arm

imp.reload(super_limb)

script = """

"""

class Rig:

    def __init__(self, obj, bone, params):
        self.obj    = obj
        self.params = params
        self.limb   = super_limb.Rig( obj, bone, params )
        self.arm    = arm.Rig( obj, bone, params )
        
    def generate(self):
        limb = self.limb.generate()
        arm  = self.arm.generate()

def add_parameters(params):
    """ Add the parameters of this rig type to the
        RigifyParameters PropertyGroup

    """
