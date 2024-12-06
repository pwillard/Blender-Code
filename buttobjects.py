#-------------------------------------------------------------------------------
# Name:        buttobjects
# Purpose:
#
# Author:      willard
#
# Created:     06/12/2024
#-------------------------------------------------------------------------------

import bpy
import mathutils
from mathutils import Vector

def get_edges_world_coordinates(obj):
    """
    Retrieve edges in world-space coordinates.
    """
    edges = []
    mesh = obj.data
    obj_matrix = obj.matrix_world  # Convert to world space

    # Ensure the mesh is up to date
    obj.update_from_editmode()

    for edge in mesh.edges:
        vert1 = obj_matrix @ mesh.vertices[edge.vertices[0]].co
        vert2 = obj_matrix @ mesh.vertices[edge.vertices[1]].co
        edges.append((Vector(vert1), Vector(vert2)))
    return edges

def find_closest_edges(edges1, edges2):
    """
    Find the pair of edges (one from each list) that are closest to each other.
    Returns the two closest edges and their distance.
    """
    closest_distance = float("inf")
    closest_pair = None

    for edge1 in edges1:
        for edge2 in edges2:
            # Compute the minimum distance between all vertices in edge pairs
            for v1 in edge1:
                for v2 in edge2:
                    distance = (v1 - v2).length
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_pair = (edge1, edge2)
    return closest_pair, closest_distance

def compute_edge_midpoint(edge):
    """
    Compute the midpoint of an edge.
    """
    return (edge[0] + edge[1]) / 2

def edge_vector(edge):
    """
    Compute the vector of an edge.
    """
    return edge[1] - edge[0]

def align_object_to_target_no_overlap(obj1, obj2):
    """
    Align obj1 to obj2 so that their closest edges touch but do not overlap.
    """
    # Get edges in world coordinates
    edges1 = get_edges_world_coordinates(obj1)
    edges2 = get_edges_world_coordinates(obj2)

    # Find the closest pair of edges
    closest_edges, closest_distance = find_closest_edges(edges1, edges2)

    if not closest_edges:
        print("No edges found to align.")
        return

    edge1, edge2 = closest_edges

    # Compute midpoints of the closest edges
    midpoint1 = compute_edge_midpoint(edge1)
    midpoint2 = compute_edge_midpoint(edge2)

    # Compute the edge vectors
    vector1 = edge_vector(edge1)
    vector2 = edge_vector(edge2)

    # Compute the direction vector for alignment
    direction = (midpoint2 - midpoint1).normalized()

    # Compute distances to avoid overlap
    edge1_length = vector1.length
    edge2_length = vector2.length
    offset_distance = edge1_length / 2 + edge2_length / 2

    # Move the object by the alignment vector with an offset to prevent overlap
    move_vector = (midpoint2 - midpoint1) + direction * offset_distance

    # Apply the translation to the object in world space
    obj1.location += move_vector
    print(f"Object {obj1.name} moved by {move_vector} to align with {obj2.name} without overlap.")

def main():
    selected_objects = bpy.context.selected_objects
    if len(selected_objects) != 2:
        print("Please select exactly two objects!")
        return

    obj1, obj2 = selected_objects
    align_object_to_target_no_overlap(obj1, obj2)

# Run the script
main()
