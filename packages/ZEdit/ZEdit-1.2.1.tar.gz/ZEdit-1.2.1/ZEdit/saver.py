#!/usr/bin/env python
from all_modules import *

from appdata import *
from rotpoint import Rot, Point
from engine import Model, Lamp, Directory, Link
import engine
from asset import Mesh, Tex, Bulb, id_gen

def castList(types, l):
  casted = [T(a) for T, a in zip(types, l)]
  slack_len = len(types)-len(casted)
  if slack_len:
    casted.extend([None]*slack_len)
  return casted

def zipdir(path, ziph):
  # ziph is zipfile handle
  for root, dirs, files in os.walk(path):
    for file in files:
      absname = os.path.join(root, file)
      arcname = absname[len(path)+1:]
      ziph.write(absname, arcname)

def unzipdir(ziph, path):
  ziph.extractall(path)

def strPosRot(obj):
  return " ".join([repr(fl) for fl in [*obj.pos, *obj.rot]])

def deStrPosRot(s):
  nums = s.split()
  pos = Point(*nums[0:3])
  rot = Rot(*nums[3:6])
  return pos, rot

def strScale(obj):
  return "\'%s\'"%" ".join([repr(fl) for fl in obj.scale])

def deStrScale(s):
  scale = np.array([float(fl) for fl in s.split()])
  if len(scale) == 1:
    return np.array([scale[0], scale[0], scale[0]])
  return scale

class Saver:
  def __init__(self, app):
    self.UE = app.remote.userenv
    self.R = app.remote
    self.app = app
    self.defaultMesh = Mesh("./assets/meshes/_default.obj")
    self.defaultTexture = Tex("./assets/textures/_default.png")
    self.defaultBulb = Bulb()
    self.defaultMesh.delete()
    self.defaultTexture.delete()
    self.defaultBulb.delete()

  def update(self):
    # copy save into tmp, ignoring unused asset files (Even though there should be NO unused asset files)
    # construct a .obj-like file that specifies construction of a userenv
    try:
      shutil.rmtree(datapath("tmp"))
    except:
      pass
    os.mkdir(datapath("tmp"))
    os.mkdir(datapath("tmp/assets"))
    os.mkdir(datapath("tmp/assets/meshes"))
    os.mkdir(datapath("tmp/assets/textures"))
    with dataopen("tmp/blueprint.dat", "w") as f:
      f.write("# 3DBP\n")

      # first, write ambient light data
      R,G,B = self.UE.scene.ambientColor
      power = self.UE.scene.ambientPower
      f.write("AMBIENT %s %s %s %s\n"%(R,G,B, power))
      
      # Placement indicies conform to Wavefront's 1-indexing
      # because having two competing standards is confusing
      meshPlacements = id_gen(1) # yields 1, 2, 3, ...
      texturePlacements = id_gen(1) # yields 1, 2, 3, ...
      bulbPlacements = id_gen(1)
      mDict = ddict(int) # mesh ID -> placement index {1, 2, 3, ...}
      tDict = ddict(int) # texture ID -> placement index {1, 2, 3, ...}
      bDict = ddict(int) # bulb ID -> placement index {1, 2, 3, ...}
      for asset in self.UE.assets:
        if type(asset) is Mesh:
          shutil.copy(datapath("save/assets/meshes/%d.obj"%asset.ID),
                      datapath("tmp/assets/meshes/%d.obj"%asset.ID))
          f.write("m '%s' %d %d\n"%(asset.name, asset.ID,
                                    asset.cullbackface))
          mDict[asset.ID] = next(meshPlacements)
        elif type(asset) is Tex:
          shutil.copy(datapath("save/assets/textures/%d.png"%asset.ID),
                      datapath("tmp/assets/textures/%d.png"%asset.ID))
          f.write("t '%s' %d %s %s %s %s\n"%(asset.name, asset.ID,
                                             asset.diffuse, asset.specular, asset.fresnel,
                                             asset.shininess))
          tDict[asset.ID] = next(texturePlacements)
        elif type(asset) is Bulb:
          f.write("b '%s' %d %s %s %s %s\n"%(asset.name, asset.ID, *asset.color, asset.power))
          bDict[asset.ID] = next(bulbPlacements)

      dirPlacements = id_gen(1)
      dirDict = {None: 0} # directory -> placement index
      def writeRendInfo(rend):
        if type(rend) is Model:
          f.write("model '%s' %d %d %s %s %d\n"%(rend.name, mDict[rend.mesh.ID], tDict[rend.tex.ID],
                                                 strPosRot(rend), strScale(rend),
                                                 rend.visible))
        elif type(rend) is Lamp:
          f.write("lamp '%s' %d %s %s %d\n"%(rend.name, bDict[rend.bulb.ID],
                                             strPosRot(rend), strScale(rend),
                                             rend.visible))
          
        elif type(rend) is Directory:
          dirDict[rend] = next(dirPlacements)
          f.write("DIR '%s' %s %s %d\n"%(rend.name, strPosRot(rend), strScale(rend), rend.visible))
          for child in rend.rends:
            writeRendInfo(child)
          f.write("END\n")

      def writeLinkInfo(rend):
        if type(rend) is Link:
          f.write("SYMLINK '%s' %d %d %s %s %d\n"%(rend.name, dirDict[rend.parent], dirDict[rend.directory],
                                                   strPosRot(rend), strScale(rend), rend.visible))
        elif type(rend) is Directory:
          for child in rend.rends:
            writeLinkInfo(child)
        
      for rend in self.UE.scene:
        writeRendInfo(rend)

      for rend in self.UE.scene:
        writeLinkInfo(rend)
      
      f.write(r"cam %s %s %s"%(strPosRot(self.UE.camera),
                                self.UE.camera.fovy,
                                self.UE.camera.zoom))
      f.write("\n")
      f.close()
      

  def save(self, fn):
    self.update()
    tmppath = datapath("tmp")
    # zip that into fn
    zipf = zipfile.ZipFile(fn, "w", zipfile.ZIP_DEFLATED)
    zipdir(tmppath, zipf)

  def load(self, fn, setGlobals=True): # doesn't clear userenv or app
    tmppath = datapath("tmp")
    
    # clear save folder
    try:
      shutil.rmtree(tmppath)
    except:
      pass
    os.mkdir(tmppath)
    
    # copy zipped contents of fn into save folder
    zipf = zipfile.ZipFile(fn, "r")
    unzipdir(zipf, tmppath)

    try:
      self.load_appdata(setGlobals=setGlobals)
    except Exception as e:
      raise IOError(e)

  def load_appdata(self, setGlobals=True):
    meshes = [self.defaultMesh]
    textures = [self.defaultTexture]
    bulbs = [self.defaultBulb]
    directories = [None] # MainApp.add(app, rend, None) adds rend as toplevel item to the scene
    dirStack = [engine.monoselected]
    for line in dataopen("tmp/blueprint.dat", "r"):
##      print(line, end="")
      words = shlex.split(line)
      if not words:
        continue
      command, *args = words
      
      if command == "#":
        pass

      elif command == "AMBIENT" and setGlobals:
        R,G,B, power = castList([*[float]*3, float], args)
        self.UE.scene.ambientColor = R,G,B
        self.UE.scene.ambientPower = power
      
      elif command == "m": # mesh
        name, ID, cullbackface = castList([str, int, int], args)
        if ID == 0:
          meshes.append(self.defaultMesh)
        else:
          new_mesh = Mesh(datapath("tmp/assets/meshes/%d.obj"%ID), name=name, cullbackface=cullbackface)
          self.app.add(new_mesh)
          meshes.append(new_mesh)
          
      elif command == "t": # texture
        name, ID, diffuse, specular, fresnel, shininess = castList([str, int, *[float]*3, float], args)
        if ID == 0:
          textures.append(self.defaultTexture)
        else:
          new_tex = Tex(datapath("tmp/assets/textures/%d.png"%ID),
                        diffuse=diffuse, specular=specular, fresnel=fresnel,
                        name=name)
          self.app.add(new_tex)
          textures.append(new_tex)

      elif command == "b": # bulb
        name, ID, R,G,B, power = castList([str, int, *[float]*3, float], args)
        if ID == 0:
          bulbs.append(self.defaultBulb)
        else:
          new_bulb = Bulb(color=(R,G,B), power=power, name=name)
          self.app.add(new_bulb)
          bulbs.append(new_bulb)

      elif command == "model":
        name, meshIndex, texIndex, x,y,z,rx,ry,rz, scale, visible\
          = castList([str, int, int, *[float]*6, str, int], args)
        scale = deStrScale(scale)
        new_model = Model(meshes[meshIndex], textures[texIndex],
                          pos=Point(x,y,z), rot=Rot(rx,ry,rz),
                          scale=scale, visible=visible,
                          name=name)
        self.app.add(new_model)

      elif command == "lamp":
        name, bulbIndex, x,y,z,rx,ry,rz, scale, visible\
          = castList([str, int, *[float]*6, str, int], args)
        scale = deStrScale(scale)
        new_lamp = Lamp(bulbs[bulbIndex],
                        pos=Point(x,y,z), rot=Rot(rx,ry,rz),
                        scale=scale, visible=visible,
                        name=name)
        self.app.add(new_lamp)

      elif command == "DIR":
        name, x,y,z,rx,ry,rz, scale, visible\
          = castList([str, *[float]*6, str, int], args)
        scale = deStrScale(scale)
        new_directory = Directory(pos=Point(x,y,z), rot=Rot(rx,ry,rz), scale=scale, visible=visible, name=name)
        self.app.add(new_directory)
        directories.append(new_directory)
        dirStack.append(new_directory)
        self.app.select(dirStack[-1])

      elif command == "END":
        dirStack.pop(-1)
        self.app.select(dirStack[-1])

      elif command == "SYMLINK":
        name, fromIndex, toIndex, x,y,z,rx,ry,rz, scale, visible\
          = castList([str, int, int, *[float]*6, str, int], args)
        scale = deStrScale(scale)
        new_symlink = Link(directories[toIndex], pos=Point(x,y,z), rot=Rot(rx,ry,rz), scale=scale, visible=visible, name=name)
        self.app.add(new_symlink, directory=directories[fromIndex])

      elif command == "cam" and setGlobals:
        x,y,z,rx,ry,rz, fovy, zoom = castList([*[float]*6, float, float], args)
        self.R.configCamera(Point(x,y,z), Rot(rx,ry,rz), fovy, zoom)

  def canRestore(self):
    return os.path.isfile(datapath("tmp/blueprint.dat"))
    
