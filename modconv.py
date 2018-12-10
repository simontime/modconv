from pyassimp import *
import datetime
import sys
import numpy
print("modconv - mountainflaw")
if (len(sys.argv) > 4):
    print("Usage: python3 modconv.py PATHTOMODEL OUTPUTNAME SCALE")
    exit()
fileName = str(sys.argv[1])
fileNameOut = str(sys.argv[2])
scale = int(sys.argv[3])

print(fileNameOut)

#initalizing common variables
loopCount = 0
scene = load(fileName)
mesh = scene.meshes[0]
vertexCount = len(mesh.vertices)
vertexheader = open(fileNameOut + ".s", "w")

# Check for vertex colors.
print("Checking for vertex colors...")
try:
    assert len(mesh.colors[0])
    usingvrgba = True
    print("There are vertex colors.")
except:
    print("There are no vertex colors.")
    usingvrgba = False

vertexGroupCount = 0 # Starting position for vertex group

# Generate vertices

vertexheader.write("# Vertices generated by modconv\n")
while (loopCount != vertexCount): # Generate vertex group for every 15 vertices
    if (loopCount % 15 == 0):
         vertexheader.write("\n" + fileNameOut + "_vertex_" + str(vertexGroupCount) + ":\n")
         vertexGroupCount += 1
    print("Generating vertex " + str(loopCount))
    vertX = str(int(mesh.vertices[loopCount][0]) * scale)
    vertY = str(int(mesh.vertices[loopCount][1]) * scale)
    vertZ = str(int(mesh.vertices[loopCount][2]) * scale)

    # Vertex RGBA

    if(usingvrgba == True):
        rgbaR = hex(int(mesh.colors[0][loopCount][0] * 255))
        rgbaG = hex(int(mesh.colors[0][loopCount][1] * 255))
        rgbaB = hex(int(mesh.colors[0][loopCount][2] * 255))
        rgbaA = hex(int(mesh.colors[0][loopCount][3] * 255))
    else:
        rgbaR = "0x00"
        rgbaG = "0x00"
        rgbaB = "0x00"
        rgbaA = "0x00"
# UV mapping

    vertU = str(int(mesh.texturecoords[0][loopCount][0] * scale))
    vertV = str(int(mesh.texturecoords[0][loopCount][1] * scale))

    vertexheader.write("vertex     " + vertX + ",     " + vertY + ",     " + vertZ + ",     " + vertU +",     " + vertV + ",  " + rgbaR + "," + rgbaG + "," + rgbaB + "," + rgbaA + "\n")
    loopCount += 1

loopCount = 0
vertBufferCount = -1
vertexGenCount = 0
triCount = 0
print("OK.")
print("Generating DLs.")
vertexheader.write("\n# Display list generated by modconv\n")
vertexheader.write("glabel " + fileNameOut + "_dl\n")
while (loopCount != vertexCount):
    
    if (vertexGenCount % 5 == 0):
        vertexGenCount = 0
        vertBufferCount += 1
        print("Generating gsSPVertex " + str(vertBufferCount))
        vertexheader.write("gsSPVertex " + fileNameOut + "_vertex_" + str(vertBufferCount) + "\n")
    print("Generating triangle " + str(triCount))
    vertexheader.write("gsSP1Triangle " + str(vertexGenCount) + ", ")
    vertexGenCount += 1
    loopCount += 1
    vertexheader.write(str(vertexGenCount) + ", ")
    vertexGenCount += 1
    loopCount += 1
    vertexheader.write(str(vertexGenCount) + ", 0x00\n")
    vertexGenCount += 1
    loopCount += 1
    triCount += 1
vertexheader.write("gsSPEndDisplayList")
print("OK.\nFinished generating DL.")


