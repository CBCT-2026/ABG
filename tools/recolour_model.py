"""Recolour the placeholder pre-op model (bone, teeth, gum) and add the gum take-off animation.
Usage: python3 tools/recolour_model.py ABG-pre-op-example.glb models/abg-placeholder.glb"""
import trimesh, numpy as np, sys, struct, json
from trimesh.visual.material import PBRMaterial
import pygltflib
src, out = sys.argv[1], sys.argv[2]
s = trimesh.load(src)
mx = s.geometry['ABG-skull-model-v4.002'].copy(); st = s.geometry['ABG-skull-model-v4.001'].copy()
for g in (mx, st): g.merge_vertices(merge_tex=True, merge_norm=True, digits_vertex=5)
cc = mx.split(only_watertight=False)
teeth = [c for c in cc if c.is_watertight and len(c.faces) > 500 and c.bounds[0][1] < -0.01]
rest = [c for c in cc if not any(c is t for t in teeth)]
B = trimesh.util.concatenate(rest)
# The left central incisor is fused to the bone part: its crown is the bone below the gum line.
c = B.triangles_center
fused = (c[:, 0] > 0.003) & (c[:, 0] < 0.0185) & (c[:, 1] < -0.002) & (c[:, 2] > 0.012)
T = trimesh.util.concatenate(teeth + [B.submesh([np.where(fused)[0]], append=True)])
B = B.submesh([np.where(~fused)[0]], append=True)
def lin(h):  # sRGB hex -> linear
    v = np.array([int(h[i:i+2], 16) / 255 for i in (1, 3, 5)])
    return list(np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)) + [1.0]
mats = {'bone': (lin('#D3C29E'), 0.9), 'teeth': (lin('#F3EFE4'), 0.3), 'gum': (lin('#D9817F'), 0.5)}
sc = trimesh.Scene()
for g, n, node in ((B, 'bone', 'bone'), (T, 'teeth', 'teeth'), (st, 'gum', 'soft-tissue')):
    col, r = mats[n]
    g.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(name=n, baseColorFactor=col, metallicFactor=0.0, roughnessFactor=r))
    sc.add_geometry(g, node_name=node, geom_name=node)
sc.export(out)
# Add two animations that move the gum overlay down off the model and back.
G = pygltflib.GLTF2().load(out)
node = [i for i, n in enumerate(G.nodes) if n.name == 'soft-tissue'][0]
blob = G.binary_blob()
off = np.array([0, -0.03, 0.008], 'f4')
times = np.array([0, 0.4, 1.4], 'f4')
fwd = np.array([[0, 0, 0], [0, -0.004, 0.001], off], 'f4')
def add(arr, typ):
    global blob
    pad = (-len(blob)) % 4; blob += b'\0' * pad
    G.bufferViews.append(pygltflib.BufferView(buffer=0, byteOffset=len(blob), byteLength=arr.nbytes))
    blob += arr.tobytes()
    acc = pygltflib.Accessor(bufferView=len(G.bufferViews) - 1, componentType=5126, count=len(arr), type=typ)
    if typ == 'SCALAR': acc.min, acc.max = [float(arr.min())], [float(arr.max())]
    G.accessors.append(acc); return len(G.accessors) - 1
t = add(times, 'SCALAR')
for name, vals in (('remove', fwd), ('replace', fwd[::-1].copy())):
    v = add(vals, 'VEC3')
    G.animations.append(pygltflib.Animation(name=name,
        samplers=[pygltflib.AnimationSampler(input=t, output=v, interpolation='LINEAR')],
        channels=[pygltflib.AnimationChannel(sampler=0, target=pygltflib.AnimationChannelTarget(node=node, path='translation'))]))
G.buffers[0].byteLength = len(blob); G.set_binary_blob(blob); G.save(out)
print('ok', len(teeth), int(fused.sum()))
