import trimesh
import numpy as np
import sys
import os
from subprocess import call

mesh = trimesh.load_mesh(sys.argv[1])
print("file loaded")
rej=0
acc=0

def mesh_intersect(old_mesh, new_mesh):
    if (old_mesh.bounds[1][0] < new_mesh.bounds[0][0]): return False
    if (old_mesh.bounds[0][0] > new_mesh.bounds[1][0]): return False
    if (old_mesh.bounds[1][1] < new_mesh.bounds[0][1]): return False
    if (old_mesh.bounds[0][1] > new_mesh.bounds[1][1]): return False
    if (old_mesh.bounds[1][2] < new_mesh.bounds[0][2]): return False
    if (old_mesh.bounds[0][2] > new_mesh.bounds[1][2]): return False
    return True

def does_accept_part(split_mesh, original_mesh):
    if len(split_mesh.triangles) < 4:
#        print("less than 4 triangles, just ",len(split_mesh.triangles))
        return False
    
    number_tri_condition = len(split_mesh.triangles) / len(original_mesh.triangles) >= 0.005
    area_condition = split_mesh.area/original_mesh.area > 0.006
  
 #   print("original",len(original_mesh.triangles),original_mesh.area)
  #  print("number_tri_condition", number_tri_condition)
    
   # print("number of triangles",len(split_mesh.triangles), (len(split_mesh.triangles) / len(original_mesh.triangles)) > 0.01)
          
   # print("area_condition", area_condition, split_mesh.area, original_mesh.area )
    if (number_tri_condition or area_condition):
        return True
    else:
        return False


res = mesh.split(only_watertight=False)
n=0
bad_vertices=0
for i in res:
    r = does_accept_part(i, mesh)
    n+=1
    print("mesh number ",n)
    name = sys.argv[1]
    name = name[1:len(name)-4]
    if r == True:
 	   #trimesh.io.export.export_mesh(i,"%s.stl"%(sys.argv[1][0:len(sys.argv[1])-4]+str(acc)),"stl")
 	  # trimesh.io.export.export_mesh(i,"%s.off"%(sys.argv[1][0:len(sys.argv[1])-4]+str(acc)),"off")
 	   acc+=1
 	   if (acc == 1): 
 	     union_mesh = i
 	     trimesh.io.export.export_mesh(union_mesh,"union.off","off")
 	   else:
 	     if(sys.argv[2] == "cork"):
 	       un_acc = 0
 	       trimesh.io.export.export_mesh(i,"current.off","off")
 	     #  (union_mesh + i).show()
 	       print("Starting Union")
 	       os.system("~/Downloads/Work/cork-master/bin/./cork -union current.off union.off res.off")
 	       print("Union Complete")
 	       union_mesh = trimesh.load_mesh("res.off")
 	       print("Cleaning previous union")
 	       union_split = union_mesh.split(only_watertight = False)
 	       unSpNum = len(union_split)
 	       print("Number of meshes in prev union = ", unSpNum)
 	       if (unSpNum > 1):
 	         for ab in union_split:
 	           unSp = does_accept_part(ab, union_mesh)
 	           if (unSp == True and un_acc == 0):
 	             trimesh.io.export.export_mesh(ab,"union.off","off")
 	             un_acc += 1
 	             print("Accepted parts in union", un_acc)
 	           elif (unSp == True and un_acc > 0):
 	             union_mesh = trimesh.load_mesh("union.off")
 	             union_mesh += ab
 	             trimesh.io.export.export_mesh(union_mesh,"union.off","off")
 	             un_acc += 1
 	             print("Accepted parts in union", un_acc)

 	     else:
 	       if (mesh_intersect(union_mesh, i)==True):
 	     	#  (union_mesh + i).show()
 	     	  print("There is intersection")
 	     	  trimesh.boolean.union([union_mesh,i],engine = sys.argv[2])
 	       else:
 	     #	  (union_mesh + i).show()
 	     	  print("No intersection")
 	     	  union_mesh += i
 	      
 	   print("mesh accepted")
    else:
 	   rej+=1
 	   if (rej == 1): 
 	     bad_mesh = i
 	   else:
 	     bad_mesh += i
 	   bad_vertices += len(i.vertices)
 	   print("REJECT")
    print()

print("Total number of bad vertices ",bad_vertices)
if (rej>0):
  print("Number of bad_mesh vertices",len(bad_mesh.vertices))
  trimesh.io.export.export_mesh(bad_mesh,"bad_meshes.stl","stl")
if (sys.argv[2] == "cork"):
  union_mesh = trimesh.load_mesh("union.off") 
trimesh.io.export.export_mesh(union_mesh,"%s.stl"%(sys.argv[1][0:len(sys.argv[1])-4]+"_out"+"_%s"%sys.argv[2]),"stl")
print("Total number of meshes is",n)
print("Number of accepted meshes is ",acc)
print("Number of rejected meshes is ",rej)
