This code uses trimesh library to make a union of all meshes per file to create a new unified object which makes it easier, faster, more reliable for 3d printing.

The code is built in Ubuntu environment.

Usage:-

python union.py <file name> <tool used>

example: python3 union.py r2d2-1.stl blender

files can be {off, obj, stl, STL}
tools can be {blender, gscad, cork}
