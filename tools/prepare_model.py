"""Prepare a stage model exported from Blender for the web page.
Usage: python3 tools/prepare_model.py <export.glb> models/<name>.glb
Keeps the nodes as exported (bone, teeth, graft, soft-tissue, canine ...), sets the site's PBR colours by node name,
and adds the gum animations "remove" / "replace" (the soft-tissue node slides down off the jaw) that site.js plays.
Then: npx @gltf-transform/cli@4.1.1 draco models/<name>.glb models/<name>.glb
      python3 tools/make_usdz.py models/<name>.glb models/<name>.usdz
      python3 tools/poster.py models/<name>.glb models/<name>-poster.webp"""
import sys, numpy as np, trimesh, pygltflib
from trimesh.visual.material import PBRMaterial
src, out = sys.argv[1], sys.argv[2]
def lin(h):
    v = np.array([int(h[i:i+2], 16) / 255 for i in (1, 3, 5)])
    return list(np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)) + [1.0]
MATS = {'bone': ('#D3C29E', 0.9), 'teeth': ('#F3EFE4', 0.3), 'gum': ('#D9817F', 0.5), 'graft': ('#E3CFA6', 1.0), 'canine': ('#F3EFE4', 0.3), 'braces': ('#B8BCC2', 0.35)}
ALIAS = {'soft-tissue': 'gum', 'overlay': 'gum', 'maxilla': 'bone'}
s = trimesh.load(src, force='scene')
sc = trimesh.Scene()
for name, g in s.geometry.items():
    g = g.copy()
    T = s.graph.get(name)[0] if name in s.graph.nodes else None
    # find the node transform that references this geometry
    for node in s.graph.nodes_geometry:
        if s.graph[node][1] == name: g.apply_transform(s.graph[node][0]); node_name = node; break
    else: node_name = name
    base = node_name.split('.')[0].lower()
    key = next((k for k in MATS if k in base), None) or ALIAS.get(base) or next((v for k, v in ALIAS.items() if k in base), None)
    assert key, f'cannot classify node {node_name!r}; name nodes bone/teeth/graft/soft-tissue/canine'
    col, r = MATS[key]
    g.visual = trimesh.visual.TextureVisuals(material=PBRMaterial(name=key, baseColorFactor=lin(col), metallicFactor=0.0, roughnessFactor=r))
    nn = 'soft-tissue' if key == 'gum' else key
    sc.add_geometry(g, node_name=nn, geom_name=nn)
ext = sc.bounds[1] - sc.bounds[0]
assert 0.05 < ext.max() < 0.3, f'model extent {ext} m: expected metres (about 0.1 m)'
sc.export(out)
G = pygltflib.GLTF2().load(out)
node = [i for i, n in enumerate(G.nodes) if n.name == 'soft-tissue'][0]
blob = G.binary_blob()
off = np.array([0, -0.03, 0.008], 'f4'); times = np.array([0, 0.4, 1.4], 'f4')
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
print('ok', [n.name for n in G.nodes], 'extent m', ext.round(3))
