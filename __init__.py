import bpy

class EasyRigidBodies(bpy.types.Panel):
    bl_idname = "easyrigidbodytools"
    bl_label = "Easy Rigid Body Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Easy Rigid Body Tools"

    def draw(self, context):
        self.layout.label(text="Add rigid bodies")
        button1 = self.layout.operator("rigidbody.objects_add", text="Add Active")
        button1.type = 'ACTIVE'
        button2 = self.layout.operator("rigidbody.objects_add", text="Add passive")
        button2.type = 'PASSIVE'
        self.layout.label(text="Remove rigid bodies")
        button3 = self.layout.operator("rigidbody.objects_remove", text="Remove")
        self.layout.label(text="Copy rigid body settings from active object")
        button4 = self.layout.operator("rigidbody.object_settings_copy", text="Copy")
        self.layout.label(text="Set collision shape of selected rigid bodies")
        row = self.layout.row()
        row.enabled = OBJECT_OT_rigidbody_collision_shape_set.poll(context) #corrected line
        row.prop(context.scene, "collision_shape_enum", text="")
        row.operator("object.rigidbody_collision_shape_set", text="Set")

class OBJECT_OT_rigidbody_collision_shape_set(bpy.types.Operator):
    bl_idname = "object.rigidbody_collision_shape_set"
    bl_label = "Set Collision Shape"

    def execute(self, context):
        shape = context.scene.collision_shape_enum
        for obj in bpy.context.selected_objects:
            if obj.rigid_body:
                obj.rigid_body.collision_shape = shape
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        for obj in bpy.context.selected_objects:
            if obj.rigid_body:
                return True
        return False

def register():
    bpy.types.Scene.collision_shape_enum = bpy.props.EnumProperty(
        items=[
            ('CONVEX_HULL', "Convex Hull", "Convex Hull"),
            ('BOX', "Box", "Box"),
            ('SPHERE', "Sphere", "Sphere"),
            ('CAPSULE', "Capsule", "Capsule"),
            ('CYLINDER', "Cylinder", "Cylinder"),
            ('CONE', "Cone", "Cone"),
            ('MESH', "Mesh", "Mesh"),
        ],
        name="Collision Shape",
        description="Choose the collision shape",
        default='CONVEX_HULL',
    )
    bpy.utils.register_class(EasyRigidBodies)
    bpy.utils.register_class(OBJECT_OT_rigidbody_collision_shape_set)

def unregister():
    del bpy.types.Scene.collision_shape_enum
    bpy.utils.unregister_class(EasyRigidBodies)
    bpy.utils.unregister_class(OBJECT_OT_rigidbody_collision_shape_set)

if __name__ == "__main__":
    register()
