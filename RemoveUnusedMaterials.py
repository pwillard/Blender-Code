#-------------------------------------------------------------------------------
# Name:        RemoveUnusedMaterials.py
# Purpose:     Remove Unused Materials from a Blender file
#
# Author:      willard
#
# Created:     06/12/2024
#-------------------------------------------------------------------------------



import bpy
intCounter = 0
# Grab list of selected objects
lstSelectedObjects = bpy.context.selected_objects

# Loop over collection of selected objects
for Object in lstSelectedObjects:
# Set current object as active object
    bpy.context.view_layer.objects.active = Object
# Find if there's a material index with the slot name of empty string '' and set it active
    key = ''
    try:
        Object.active_material_index = Object.material_slots[''].slot_index
    except KeyError:
        print(f"{Object.name} doesn't contain an empty material slot.  Continuing...")
        continue
# Run the remove slot function on active slot
    bpy.ops.object.material_slot_remove()
    intCounter += 1

print(f"Empty slots removed from {intCounter} object(s).")
print("Script completed successfully.")