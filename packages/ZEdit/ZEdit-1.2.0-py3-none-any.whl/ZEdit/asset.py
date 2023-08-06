#!/usr/bin/env python

'''
asset.py
original source: https://github.com/edward344/PyOpenGL-sample/blob/master/graphics.py
changes:
    - texture coordinates specific to each face are taken into account
    - made more pythonic with split and by removing unnecessary ifs
    - render_scene and render_texture is merged into one function
    - Immediate mode -> VBO

thanks edward344!
'''
from all_modules import *
from appdata import datapath
from shader import *

def id_gen(start=1):
    '''Generator that yields consecutive numbers'''
    next_id = start
    while True:
        yield next_id
        next_id += 1

def gentexcoord(f):
    '''Generates texcoord for missing texcoord vertices--UNUSED'''
    X = (sin(f*tau)+1)/2
    Y = (cos(f*tau)+1)/2
    return (X, Y)

def standardizeImage(filename):
    '''Resized image to standard size (1024, 1024) and converts it into RGBA'''
    return Image.open(filename).resize((1024, 1024)).convert("RGBA")

def load_texture(filename):
    '''Loads OpenGL TexImage object from filename
       and Returns the id for the texture'''
    textureSurface = standardizeImage(filename)
    textureData = textureSurface.tobytes("raw")
    IM = Image.frombytes("RGBA", textureSurface.size, textureData)
    width, height = textureSurface.size
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,ID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,
                 0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)
    return ID

def load_thumbnail(filename):
    '''Resizes image from filename to (150, 150) and returns it.'''
    im = Image.open(filename)
    return im.resize((150, 150))

def im2pixmap(im):
    '''Turns PIL image im into a Qt pixmap.'''
    qim = ImageQt(im)
    pixmap = QPixmap.fromImage(qim)
    return pixmap

def im2qim(im):
    '''Turns PIL image into an ImageQt.'''
    qim = ImageQt(im)
    return qim

class Asset:
    '''An object expected to be used repeatedly among multiple renderables'''
    name = "asset0"


class Tex(Asset):
    '''Describes a texture with an image and shading properties'''
    IDs = id_gen(1)
    texDict = dict()
    def __init__(self, filename, diffuse=1.0, specular=0.0, fresnel=0.0, shininess=10.0, name=None):
        self.ID = next(Tex.IDs)
        self._clear()
        self.diffuse = diffuse
        self.specular = specular
        self.fresnel = fresnel
        self.shininess = shininess
        self.filename = filename
        if name is None:
            name = os.path.basename(filename)
        self.name = name
        self.thumbnail = None
        self.thumbnailQt = None
        self._load()
        Tex.texDict[self.ID] = self

    def _clear(self):
        self.deleted = False
        self.texID = None

    def _load(self):
        self.texID = load_texture(self.filename)
        self.thumbnail = load_thumbnail(self.filename) # 100x100 res
        self.thumbnailQt = im2qim(self.thumbnail)
        self.tmpFilename = datapath("save/assets/textures/%d.png"%self.ID)
        standardizeImage(self.filename).save(self.tmpFilename, "PNG")

    def delete(self):
        self.deleted = True
        glDeleteTextures([self.texID]) # Removes this texture's image from memory
        self.texID = 0 # OpenGL's default texture, white
        self.filename = None
        self.name = None
        self.diffuse = 0.0
        self.specular = 0.0
        self.fresnel = 0.0
        self.shininess = 0.0
        del Tex.texDict[self.ID]

    def __copy__(self):
        return Tex(self.tmpFilename, diffuse=self.diffuse, specular=self.specular, fresnel=self.fresnel, shininess=self.shininess,name=self.name)

    def __deepcopy__(self, memo):
        return copy.copy(self)

class Mesh(Asset):
    '''Describes a mesh with geometry and rendering specifications'''
    IDs = id_gen(1)
    meshDict = dict()
    def __init__(self, filename, name=None, cullbackface=True):
        self.ID = next(Mesh.IDs)
        self._clear()
        self.filename = filename
        self.cullbackface = cullbackface
        if name is None:
            name = os.path.basename(filename)
        self.name = name
        try:
            self._load()
        except Exception as e:
            raise IOError("Bad mesh file. More info:\n"+str(e))
        else:
            self.tmpFilename = datapath("save/assets/meshes/%d.obj"%self.ID)
            shutil.copyfile(self.filename, self.tmpFilename)
            Mesh.meshDict[self.ID] = self

    def _clear(self):
        self.deleted = False
        
        # cullbackface
        #   OFF: show both front and back of each polygon
        #   ON:  show only front face of each polygon
        self.cullbackface = True # modify this as you please
        
        self.vertices = [(0.0, 0.0, 0.0)] # 1-indexing
        self.texcoords = [(0.0, 0.0)] # 1-indexing, accounts for no-texcoord polygons
        self.normals = [(0.0, 0.0, 1.0)] # 1-indexing
        self.edges = set()
        self.tri_faces = []
        self.quad_faces = []
        self.poly_faces = []

        self.vbo_bufferlen = 0
        self.vbo_vertices = []
        self.vbo_texcoords = []
        self.vbo_normals = []
        self.vbo_tri_indices = []
        self.vbo_line_indices = []
        self.vbo_buffers = []

        self.min_xyz = [None, None, None]
        self.max_xyz = [None, None, None]

    def _load(self):
        '''Load from .obj file'''
        filename = self.filename
        f = open(filename)
        for line in f:
            words = line.split()
            if not words:
                continue
            command = words[0]
            if command == "v":
                vertex = tuple(float(word) for word in words[1:4])
                self.vertices.append(vertex)
                self._update_bbox(vertex)

            elif command == "vt":
                texcoord = tuple(float(word) for word in words[1:3])
                self.texcoords.append(texcoord)

            elif command == "vn":
                normal = tuple(float(word) for word in words[1:4])
                self.normals.append(normal)
                
            elif command == "f":
                face = []

                # face := [(v0, vt0, vn0), (v1, vt1, vn1), (v2, vt2, vn2), ...]
                for word in words[1:]:
                    word = word.replace("//", "/0/")
                    nums = [int(strint) for strint in word.split("/")]
                    nums += [0]*(3-len(nums))
                    face.append(tuple(nums)) # v, vt, vn
                
                for i in range(-1, len(face)-1): # Add new (A, B) pairs into self.edges
                    edge = (face[i][0], face[i+1][0])
                    if edge in self.edges or edge[::-1] in self.edges:
                        continue
                    self.edges.add(edge)

                N_v = len(face)
                
                if N_v == 3:
                    self.tri_faces.append(face)
                elif N_v == 4:
                    self.quad_faces.append(face)
                else:
                    self.poly_faces.append(face)
                    
        f.close()
        self._gen_normals()
        self._gen_vbo_arrays()
        self._gen_vbo_buffers()

    def _update_bbox(self, v):
        for i, (minn, maxn, n) in enumerate(zip(self.min_xyz, self.max_xyz, v)):
            if minn is None or n < minn:
                self.min_xyz[i] = n
            if maxn is None or n > maxn:
                self.max_xyz[i] = n
        

    def _gen_normals(self):
        '''Generate missing normal vectors'''
        for face in chain(self.tri_faces, self.quad_faces, self.poly_faces):
            if face[0][2] != 0:
                continue
            A = self.vertices[face[0][0]]
            B = self.vertices[face[1][0]]
            C = self.vertices[face[2][0]]
            AB = tuple(Bn-An for An, Bn in zip(A, B))
            AC = tuple(Cn-An for An, Cn in zip(A, C))
            x, y, z = normal = np.cross(AC, AB)
            self.normals.append(tuple(normal))
            normal_index = len(self.normals)-1
            for i, (v, vt, vn) in enumerate(face):
                face[i] = (v, vt, normal_index)
            

    def _gen_vbo_arrays(self):
        '''Generate VBO arrays'''
        # TRIS
        for face in chain(self.tri_faces, self.quad_faces, self.poly_faces):
            di = self.vbo_bufferlen
            N_v = len(face)
            for v, vt, vn in face:
                self.vbo_vertices.extend(self.vertices[v])
                self.vbo_texcoords.extend(self.texcoords[vt])
                self.vbo_normals.extend(self.normals[vn])
            Ai = di
            for Bi, Ci in zip(range(di+1,di+N_v-1), range(di+2,di+N_v)):
                self.vbo_tri_indices.extend((Ai, Bi, Ci))
                self.vbo_line_indices.extend((Ai, Bi, Bi, Ci, Ci, Ai))
            self.vbo_bufferlen += N_v

    def _gen_vbo_buffers(self):
        '''Make buffers from VBO arrays'''
        # vertices, texcoords, normals, indices for tris
        buffers = glGenBuffers(5)

        # vertices [x, y, z, x, y, z, ...]
        glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.vbo_vertices)*4,
                     (ctypes.c_float*len(self.vbo_vertices))(*self.vbo_vertices),
                     GL_STATIC_DRAW)

        # texcoords [X, Y, X, Y, X, Y, ...]
        glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.vbo_texcoords)*4,
                     (ctypes.c_float*len(self.vbo_texcoords))(*self.vbo_texcoords),
                     GL_STATIC_DRAW)

        # normals [dx, dy, dz, dx, dy, dz, ...]
        glBindBuffer(GL_ARRAY_BUFFER, buffers[2])
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.vbo_normals)*4,
                     (ctypes.c_float*len(self.vbo_normals))(*self.vbo_normals),
                     GL_STATIC_DRAW)

        # vertex indices for tris [Ai, Bi, Ci, Ai, Bi, Ci, ...]
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[3])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     len(self.vbo_tri_indices)*4,
                     (ctypes.c_uint*len(self.vbo_tri_indices))(*self.vbo_tri_indices),
                     GL_STATIC_DRAW)

        # wireframe lines (has redundancies, but gets the job done)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[4])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     len(self.vbo_line_indices)*4,
                     (ctypes.c_uint*len(self.vbo_line_indices))(*self.vbo_line_indices),
                     GL_STATIC_DRAW)

        self.vbo_buffers = buffers

    def __repr__(self):
        return "Mesh(%s)"%self.filename
            
    def render(self, tex): # GPU-powered rendering!
        '''Render mesh into buffers with texture from textureID.'''
        glEnable(GL_TEXTURE_2D)
        if self.cullbackface:
            glEnable(GL_CULL_FACE)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex.texID)
        glUniform1i(Shader.current.uniformLocs["texture"], 0)
        glUniform1f(Shader.current.uniformLocs["diffuse"], tex.diffuse)
        glUniform1f(Shader.current.uniformLocs["specular"], tex.specular)
        glUniform1f(Shader.current.uniformLocs["fresnel"], tex.fresnel)
        glUniform1f(Shader.current.uniformLocs["shininess"], tex.shininess)

        #====VBO (STANDARD, GPU PIPELINE)====
        V, TC, N, TRI_I, _ = self.vbo_buffers
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        
        glBindBuffer(GL_ARRAY_BUFFER, V)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, TC)
        glTexCoordPointer(2, GL_FLOAT, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, N)
        glNormalPointer(GL_FLOAT, 0, None)

        # WE SHOULD TAKE RENDERING JOBS
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, TRI_I)
        # AND PUSH IT TO THE GPU PIPELINE
        glDrawElements(GL_TRIANGLES, len(self.vbo_tri_indices), GL_UNSIGNED_INT, None)
        
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)

    def render_wireframe(self):
        V, _, _, _, LINE_I = self.vbo_buffers
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, V)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, LINE_I)
        glDrawElements(GL_LINES, len(self.vbo_line_indices), GL_UNSIGNED_INT, None)
        glDisableClientState(GL_VERTEX_ARRAY)

    def delete(self):
        '''Unload self, turning into a cube'''
        self._clear()
        self.filename = r"./assets/meshes/_default.obj"
        self.name = None
        self._load()
        self.deleted = True
        del Mesh.meshDict[self.ID]

    def __copy__(self):
        return Mesh(self.tmpFilename, cullbackface=self.cullbackface, name=self.name)

    def __deepcopy__(self, memo):
        return copy.copy(self)

class Bulb(Asset):
    '''Describes a bulb with power and color specifications.'''
    IDs = id_gen()
    bulbDict = dict()
    def __init__(self, power=1.0, color=(1.0, 1.0, 1.0), name=None):
        self.ID = next(Bulb.IDs)
        self._clear()
        self.power = power
        self.color = color
        if name is None:
            name = "bulb0"
        self.name = name

    def _clear(self):
        self.deleted = False
        self.power = 0.0
        self.color = (0.0, 0.0, 0.0)

    def delete(self):
        self._clear()
        self.deleted = True
        self.name = None

    def __copy__(self):
        return Bulb(power=self.power, color=self.color, name=self.name)

    def __deepcopy__(self, memo):
        return copy.copy(self)

    
        
