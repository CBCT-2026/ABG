"""Prepare a stage model exported from Blender for the web page.
Usage: python3 tools/prepare_model.py <export.glb> models/<name>.glb
The export must not be Draco-compressed (decode first: npx @gltf-transform/cli@4.1.1 cp in.glb plain.glb).
Keeps the meshes as exported and names the nodes and materials by part (bone, teeth, graft, soft-tissue, canine,
braces, option-implant, option-bridge, option-denture, option-none); site.js finds the parts by material name. Parts with the
site's fixed colours get them; parts that carry their own colours (braces, options) keep them. Adds the gum
animations "remove" / "replace" (the soft-tissue node slides down off the jaw) that site.js plays.
Then: npx @gltf-transform/cli@4.1.1 draco models/<name>.glb models/<name>.glb
      python3 tools/make_usdz.py <plain export> models/<name>.usdz
      node tools/poster.js models/<name>.glb models/<name>-poster.webp"""
import sys, copy, numpy as np, pygltflib
src, out = sys.argv[1], sys.argv[2]
def lin(h):
    v = np.array([int(h[i:i+2], 16) / 255 for i in (1, 3, 5)])
    return [float(x) for x in np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)] + [1.0]
FIXED = {'bone': ('#D3C29E', 0.9), 'teeth': ('#F3EFE4', 0.3), 'gum': ('#D9817F', 0.5), 'graft': ('#C9A86A', 1.0), 'canine': ('#F3EFE4', 0.3)}
OWN = ['option-implant', 'option-bridge', 'option-denture', 'option-none', 'braces']  # keep the colours from the export
ALIAS = {'soft-tissue': 'gum', 'overlay': 'gum', 'maxilla': 'bone'}
def classify(name):
    base = name.split('.')[0].lower()
    for k in OWN:
        if k in base: return k
    for k in FIXED:
        if k in base: return k
    for k, v in ALIAS.items():
        if k in base: return v
    raise SystemExit(f'cannot classify node {name!r}; name nodes bone/teeth/graft/soft-tissue/canine/braces/option-*')
G = pygltflib.GLTF2().load(src)
assert not any('KHR_draco_mesh_compression' in (p.extensions or {}) for m in G.meshes for p in m.primitives), 'decode Draco first'
used = {}
for node in G.nodes:
    if node.mesh is None: continue
    if 'option-substitution' in (node.name or '').lower():  # the substitution arch ships as its own file (models/abg-3b-substitution.glb)
        node.mesh = None; continue
    key = classify(node.name or G.meshes[node.mesh].name or '')
    node.name = 'soft-tissue' if key == 'gum' else key
    G.meshes[node.mesh].name = node.name
    for prim in G.meshes[node.mesh].primitives:
        m = copy.deepcopy(G.materials[prim.material]) if prim.material is not None else pygltflib.Material(pbrMetallicRoughness=pygltflib.PbrMetallicRoughness())
        m.name = key
        if key in FIXED:
            col, r = FIXED[key]
            m.pbrMetallicRoughness.baseColorFactor = lin(col); m.pbrMetallicRoughness.metallicFactor = 0.0; m.pbrMetallicRoughness.roughnessFactor = r
        m.alphaMode = 'OPAQUE'
        G.materials.append(m); prim.material = len(G.materials) - 1
        used[key] = used.get(key, 0) + 1
# Drop materials no longer referenced.
keep = sorted({p.material for m in G.meshes for p in m.primitives})
remap = {old: i for i, old in enumerate(keep)}
G.materials = [G.materials[i] for i in keep]
for m in G.meshes:
    for p in m.primitives: p.material = remap[p.material]
# Gum animations: each clip moves the part over 1.4 s then holds its final pose for a long tail, so pausing anywhere
# after 1.4 s keeps the part where it ended (a clip that simply finishes would snap back to its first frame).
node = [i for i, n in enumerate(G.nodes) if n.name == 'soft-tissue'][0]
blob = G.binary_blob()
off = [0, -0.03, 0.008]; mid = [0, -0.004, 0.001]; home = [0, 0, 0]
times = np.array([0, 0.4, 1.4, 60], 'f4')
fwd = np.array([home, mid, off, off], 'f4'); back = np.array([off, mid, home, home], 'f4')
def add(arr, typ):
    global blob
    pad = (-len(blob)) % 4; blob += b'\0' * pad
    G.bufferViews.append(pygltflib.BufferView(buffer=0, byteOffset=len(blob), byteLength=arr.nbytes))
    blob += arr.tobytes()
    acc = pygltflib.Accessor(bufferView=len(G.bufferViews) - 1, componentType=5126, count=len(arr), type=typ)
    if typ == 'SCALAR': acc.min, acc.max = [float(arr.min())], [float(arr.max())]
    G.accessors.append(acc); return len(G.accessors) - 1
G.animations = []
t = add(times, 'SCALAR')
for name, vals in (('remove', fwd), ('replace', back)):
    v = add(vals, 'VEC3')
    G.animations.append(pygltflib.Animation(name=name,
        samplers=[pygltflib.AnimationSampler(input=t, output=v, interpolation='LINEAR')],
        channels=[pygltflib.AnimationChannel(sampler=0, target=pygltflib.AnimationChannelTarget(node=node, path='translation'))]))
G.buffers[0].byteLength = len(blob); G.set_binary_blob(blob); G.save(out)
print('ok', sorted(used), [m.name for m in G.materials])
