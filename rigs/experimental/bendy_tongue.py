import bpy

from .chainy_rig import ChainyRig
from .control_layers_generator import ControlLayersGenerator
from ...utils import flip_bone, org, strip_org, copy_bone, put_bone, align_bone_y_axis
from ...utils import create_sphere_widget, create_circle_widget,make_constraints_from_string
from ..widgets import create_ballsocket_widget, create_jaw_widget


class Rig(ChainyRig):

    TWEAK_SCALE = 0.5
    CTRL_SCALE = 0.25

    def __init__(self, obj, bone_name, params):
        super().__init__(obj, bone_name, params, single=True)

        self.layer_generator = ControlLayersGenerator(self)

    def create_mch(self):
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = self.obj.data.edit_bones

        super().create_mch()

        self.bones['tongue_mch'] = {}
        self.bones['tongue_mch']['tongue_tip'] = []

        for i, mch in enumerate(self.bones['mch'][strip_org(self.base_bone)]):
            if i == 0:
                edit_bones[mch].length = edit_bones[self.base_bone].length
                flip_bone(self.obj, mch)
                self.bones['tongue_mch']['tongue_tip'].append(mch)
            elif i == 1:
                put_bone(self.obj, mch, edit_bones[self.base_bone].tail)
                edit_bones[mch].tail = edit_bones[self.base_bone].head
                self.bones['tongue_mch']['tongue_tip'].append(mch)

    def create_controls(self):
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = self.obj.data.edit_bones

        super().create_controls()

        self.bones['tongue_ctrl'] = {}

        tongue_master_name = strip_org(self.base_bone) + '_master'
        tongue_master_name = copy_bone(self.obj, self.base_bone, assign_name=tongue_master_name)
        flip_bone(self.obj, tongue_master_name)
        self.bones['tongue_ctrl']['tongue_master'] = tongue_master_name

    def parent_bones(self):
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = self.obj.data.edit_bones

        super().parent_bones()

        edit_bones[self.bones['tongue_ctrl']['tongue_master']].parent = edit_bones[self.orientation_bone]

        def_chain = self.bones['def'][strip_org(self.base_bone)]
        ctrl_chain = self.bones['ctrl'][strip_org(self.base_bone)]
        mch_chain = self.bones['mch'][strip_org(self.base_bone)]
        org_chain = self.bones['org']

        for ctrl, def_bone in zip(ctrl_chain, def_chain):
            edit_bones[def_bone].parent = edit_bones[ctrl]

        for ctrl, mch in zip(ctrl_chain[1:-1], mch_chain):
            edit_bones[ctrl].parent = edit_bones[mch]
            edit_bones[mch].parent = edit_bones[self.orientation_bone]

        edit_bones[ctrl_chain[0]].parent = edit_bones[self.bones['tongue_ctrl']['tongue_master']]
        edit_bones[ctrl_chain[-1]].parent = edit_bones[self.orientation_bone]

        for ctrl, org_bone in zip(ctrl_chain, org_chain):
            edit_bones[org_bone].use_connect = False
            edit_bones[org_bone].parent = edit_bones[ctrl]

    def assign_layers(self):

        primary_ctrls = []
        primary_ctrls.append(self.bones['tongue_ctrl']['tongue_master'])

        all_ctrls = self.get_all_ctrls()
        self.layer_generator.assign_layer(primary_ctrls, all_ctrls)

    def make_constraints(self):

        bpy.ops.object.mode_set(mode='OBJECT')
        pose_bones = self.obj.pose.bones

        super().make_constraints()

        for def_bone in self.bones['def'][strip_org(self.base_bone)]:
            pose_bones[def_bone].constraints.remove(pose_bones[def_bone].constraints[0])

        influence_step = 1 / len(self.bones['org'])

        for mch in reversed(self.bones['tongue_mch']['tongue_tip']):
            owner = pose_bones[mch]
            subtarget = self.bones['tongue_ctrl']['tongue_master']
            make_constraints_from_string(owner, self.obj, subtarget, "CT%sWW0.0" % influence_step)
            influence_step += influence_step

    def create_widgets(self):

        bpy.ops.object.mode_set(mode='OBJECT')

        tongue_master = self.bones['tongue_ctrl']['tongue_master']
        create_jaw_widget(self.obj, tongue_master)

        super().create_widgets()

    def cleanup(self):
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = self.obj.data.edit_bones

        for mch in self.bones['mch'][strip_org(self.base_bone)]:
            if mch not in self.bones['tongue_mch']['tongue_tip']:
                edit_bones.remove(edit_bones[mch])

    def generate(self):
        return super().generate()


def create_sample(obj):
    # generated by rigify.utils.write_metarig
    bpy.ops.object.mode_set(mode='EDIT')
    arm = obj.data

    bones = {}

    bone = arm.edit_bones.new('tongue')
    bone.head[:] = 0.0000, -0.1354, 1.7946
    bone.tail[:] = 0.0000, -0.1101, 1.8002
    bone.roll = 0.0000
    bone.use_connect = False
    bones['tongue'] = bone.name
    bone = arm.edit_bones.new('tongue.001')
    bone.head[:] = 0.0000, -0.1101, 1.8002
    bone.tail[:] = 0.0000, -0.0761, 1.7949
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['tongue']]
    bones['tongue.001'] = bone.name
    bone = arm.edit_bones.new('tongue.002')
    bone.head[:] = 0.0000, -0.0761, 1.7949
    bone.tail[:] = 0.0000, -0.0538, 1.7673
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['tongue.001']]
    bones['tongue.002'] = bone.name

    bpy.ops.object.mode_set(mode='OBJECT')
    pbone = obj.pose.bones[bones['tongue']]
    pbone.rigify_type = 'experimental.bendy_tongue'
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['tongue.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['tongue.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'

    bpy.ops.object.mode_set(mode='EDIT')
    for bone in arm.edit_bones:
        bone.select = False
        bone.select_head = False
        bone.select_tail = False
    for b in bones:
        bone = arm.edit_bones[bones[b]]
        bone.select = True
        bone.select_head = True
        bone.select_tail = True
        arm.edit_bones.active = bone


def add_parameters(params):
    """ Add the parameters of this rig type to the
        RigifyParameters PropertyGroup
    """

    ControlLayersGenerator.add_layer_parameters(params)


def parameters_ui(layout, params):
    """ Create the ui for the rig parameters."""

    ControlLayersGenerator.add_layers_ui(layout, params)
