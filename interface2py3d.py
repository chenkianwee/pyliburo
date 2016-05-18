from . import py3dmodel

#==============================================================================================================================
#general functions
#==============================================================================================================================
def pyptlist_frm_occface(occ_face):
    wire_list = py3dmodel.fetch.wires_frm_face(occ_face)
    occpt_list = []
    pt_list = []
    for wire in wire_list:
        occpts = py3dmodel.fetch.points_frm_wire(wire)
        occpt_list.extend(occpts)
        
    for occpt in occpt_list:
        pt = (occpt.X(), occpt.Y(), occpt.Z()) 
        pt_list.append(pt)
    
    normal = py3dmodel.calculate.face_normal(occ_face)
    anticlockwise = py3dmodel.calculate.is_anticlockwise(pt_list, normal)
    if anticlockwise:
        return pt_list
    else:
        pt_list.reverse()
        return pt_list
    
def pyptlist_frm_occwire(occ_wire):
    pt_list = []
    occpt_list = py3dmodel.fetch.points_frm_wire(occ_wire)
    for occpt in occpt_list:
        pt = (occpt.X(), occpt.Y(), occpt.Z()) 
        pt_list.append(pt)
    return pt_list
    
def pypolygons2occsolid(pypolygon_list):
    face_list = []
    for polygon_pts in pypolygon_list:
        face = py3dmodel.construct.make_polygon(polygon_pts)
        face_list.append(face)

    #make shell
    shell = py3dmodel.construct.make_shell_frm_faces(face_list)
    shell = py3dmodel.modify.fix_shell_orientation(shell)
    
    solid = py3dmodel.construct.make_solid(shell)
    solid = py3dmodel.modify.fix_shape(solid)
    volume = py3dmodel.calculate.solid_volume(solid)
    if volume < 0:
        solid.Reverse()
    return solid