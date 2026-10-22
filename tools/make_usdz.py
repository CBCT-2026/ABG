"""Write an iPhone AR (.usdz) copy of a .glb: same meshes, same colours, no animation.
Usage: python3 tools/make_usdz.py models/abg-placeholder.glb models/abg-placeholder.usdz"""
import sys, os, tempfile, numpy as np, trimesh
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, UsdUtils
src, out = sys.argv[1], sys.argv[2]
scene = trimesh.load(src)
tmp = os.path.join(tempfile.mkdtemp(), 'model.usdc')
stage = Usd.Stage.CreateNew(tmp)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y); UsdGeom.SetStageMetersPerUnit(stage, 1.0)
root = UsdGeom.Xform.Define(stage, '/model'); stage.SetDefaultPrim(root.GetPrim())
for name, g in scene.geometry.items():
    safe = name.replace('-', '_')
    m = UsdGeom.Mesh.Define(stage, f'/model/{safe}')
    m.CreatePointsAttr([Gf.Vec3f(*map(float, v)) for v in g.vertices])
    m.CreateFaceVertexCountsAttr([3] * len(g.faces)); m.CreateFaceVertexIndicesAttr(g.faces.flatten().tolist())
    m.CreateNormalsAttr([Gf.Vec3f(*map(float, n)) for n in g.vertex_normals]); m.SetNormalsInterpolation('vertex')
    m.CreateSubdivisionSchemeAttr('none')
    pm = g.visual.material
    col = pm.baseColorFactor[:3] / 255.0 if pm.baseColorFactor.max() > 1 else pm.baseColorFactor[:3]
    mat = UsdShade.Material.Define(stage, f'/model/mat_{safe}')
    sh = UsdShade.Shader.Define(stage, f'/model/mat_{safe}/surface'); sh.CreateIdAttr('UsdPreviewSurface')
    sh.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(*map(float, col)))
    sh.CreateInput('roughness', Sdf.ValueTypeNames.Float).Set(float(pm.roughnessFactor or 0.6))
    sh.CreateInput('metallic', Sdf.ValueTypeNames.Float).Set(0.0)
    mat.CreateSurfaceOutput().ConnectToSource(sh.ConnectableAPI(), 'surface')
    UsdShade.MaterialBindingAPI.Apply(m.GetPrim()).Bind(mat)
stage.GetRootLayer().Save()
UsdUtils.CreateNewUsdzPackage(Sdf.AssetPath(tmp), out)
print(out, os.path.getsize(out))
