import numpy as np
import EditorLib

slicer.modules.NeedleFinderInstance
slicer.modules.needlefinder.widgetRepresentation()

editUtil = EditorLib.EditUtil.EditUtil()
parameterNode = editUtil.getParameterNode()
sliceLogic = editUtil.getSliceLogic()
lm = slicer.app.layoutManager()
sliceWidget = lm.sliceWidget('Red')
islandsEffect = EditorLib.IdentifyIslandsEffectOptions()
islandsEffect.setMRMLDefaults()
islandsEffect.__del__()
islandTool = EditorLib.IdentifyIslandsEffectLogic(sliceLogic)
parameterNode.SetParameter("IslandEffect,minimumSize",'20')
islandTool.removeIslands()

ar = slicer.util.array('DBScan_post_filter_028')
ar = np.swapaxes(ar, 0, 2)

w = slicer.modules.NeedleFinderWidget
l = w.logic

# create the template limit with the postion "templateLimit"
templateLimit = [0,0,-67]   # in RAS coordinates. use l.ijk2ras if you need to do the conversion from IJK to RAS
l.fiducialNode = slicer.mrmlScene.CreateNodeByClass('vtkMRMLAnnotationFiducialNode')
l.fiducialNode.Initialize(slicer.mrmlScene)
l.fiducialNode.SetName('template slice position')
l.fiducialNode.SetFiducialCoordinates(templateLimit)
fd = l.fiducialNode.GetDisplayNode()
fd.SetVisibility(1)
fd.SetColor([0, 1, 0])

tips = []
names = []

for i in range(int(ar.max())):
    names.append(str(i))
    
    coord = np.where(ar==i)
    max_z = max(coord[2])
    list_index = np.where(coord[2]==max_z)[0][0]
    x = coord[0][list_index]
    y = coord[1][list_index]
    tips.append([x,y, max_z])

m = vtk.vtkMatrix4x4()
volumeNode = slicer.app.layoutManager().sliceWidget("Red").sliceLogic().GetBackgroundLayer().GetVolumeNode()
volumeNode.GetIJKToRASMatrix(m)
imageData = volumeNode.GetImageData()
spacing = volumeNode.GetSpacing()
l.needleDetectionThread(tips, imageData, spacing=spacing, script=False, names=names)

