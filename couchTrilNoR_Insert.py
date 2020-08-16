####################################
#couchTrilNoR_Insert.py
#create subscript that generates the trilogy couch w/ no rail in Pinnacle
#
#Modified:
#2016 02 v1 Becket Hui
#2016 03 v1.1 Becket Hui change density after study
#2016 04 v2 Becket Hui change names
####################################
#make sure this file and all other subfiles are stored in script home in the main Script
import sys, re, math

def readMe(line,m):
 """!
 @brief return the value after equal sign a line read from Pinnacle Store file
 @param line line read from Pinnacle Store file
 @param m mode of the value - 'f' being number and 's' being string
 """
 if m=='f':
  linesp = re.split(r';|\s+',line)
  for i in range(len(linesp)):
   if linesp[i] == '=':
    return float(linesp[i+1])
 if m=='s':
  linesp = re.split(r'\"|;',line)
  for i in range(len(linesp)):
   if re.search('=',linesp[i]):
    return linesp[i+1]

def ctcoor(x,x0,dx):
 """!
 @brief compute the nearest coordinate to the allowed CT coordinate
 @param x input coordinate
 @param x0 CT in-plane origin
 @param dx CT in-plane resolution
 """
 xc = round((x-x0)/dx)*dx+x0

 return xc

def createTable(ptFolder):
 """!
 @brief read the information from Store.Couch to create score card script
 @param savFolder location of the patient folder, where all the intermediate files located
 """
 #read the parameters from the store file
 with open(ptFolder+'Store.Couch', 'r') as f:
  for line in f:
   if re.search('.CouchRemoveY = Float',line):
    line2 = f.next()
    CouchRemoveY = readMe(line2,'f')
   if re.search('.X0 = Float',line):
    line2 = f.next()
    x0 = readMe(line2,'f')
   if re.search('.NX = Float',line):
    line2 = f.next()
    Nx = int(readMe(line2,'f'))
   if re.search('.dX = Float',line):
    line2 = f.next()
    dx = readMe(line2,'f')
   if re.search('.Y0 = Float',line):
    line2 = f.next()
    y0 = readMe(line2,'f')
   if re.search('.NY = Float',line):
    line2 = f.next()
    Ny = int(readMe(line2,'f'))
   if re.search('.dY = Float',line):
    line2 = f.next()
    dy = readMe(line2,'f')
   if re.search('.Z0 = Float',line):
    line2 = f.next()
    z0 = readMe(line2,'f')
   if re.search('.NZ = Float',line):
    line2 = f.next()
    Nz = int(readMe(line2,'f'))
   if re.search('.dZ = Float',line):
    line2 = f.next()
    dz = readMe(line2,'f')
   if re.search('.XShift = Float',line):
    line2 = f.next()
    xSh = readMe(line2,'f')

 x_m = x0+0.5*(Nx*dx) #mid-point of the couch is mid-point of image
 CouchRemoveY = math.floor((CouchRemoveY-y0)/dy)*dy+y0 #redefine couch remove coor to ct coor
 
 #write scripts to create Trilioly couch
 #heading
 f = open(ptFolder+'createcouchTril.Script','w')

 f.write('//////////////////////////\n')
 f.write('//createcouchTril.Script//\n')
 f.write('//////////////////////////\n')
 f.write('\n')
 f.write('//clear current couch//\n')
 f.write('\n')


 #start writing ROI
 f.write('//create ROI//\n')
 f.write('IF.CtSimLayout.Is.#\"!Orthogonal\".THEN.ViewWindowList.CtSimOrthoTop.MakeCurrent = \"OrthoLayoutIcon\";\n')
 f.write('CtSimLayout = \"Orthogonal\";\n')
 f.write('ViewWindowList.Current = \"CtSimOrthoTop\";\n')
 f.write('ViewWindowList.Current.Enter2dMode = \"Enter 2D Mode\";\n')
 f.write('ViewWindowList.Current.Orientation.MakeTransverse = \"Transverse\";\n')

 f.write('ViewWindowList.Current.SliceNumber = \"1\";\n')
 f.write('//air contour//\n')
 f.write('CreateNewROI = \"Add ROI\";\n')
 f.write('RoiList.Last.Name = \"couchAirOverride\";\n')
 f.write('RoiList.Last.EditCurve = {\n')
 f.write(' SliceCoordinate = %.3f;\n' %z0)
 f.write(' Curve = {\n')
 f.write('  NumberOfPoints = 5;\n')
 f.write('  Points[] = {\n')
 f.write('  %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f\n' %(x0+dx, ctcoor(CouchRemoveY,y0,dy), x0+float(Nx)*dx-dx, ctcoor(CouchRemoveY,y0,dy), x0+float(Nx)*dx-dx, y0+dy, x0+dx, y0+dy, x0+dx, ctcoor(CouchRemoveY,y0,dy)))
 f.write('  };\n')
 f.write(' };\n')
 f.write('};\n')
 f.write('RoiList.Last.CopyEditCurveToNewCurveAndClear = \"\";\n')
 f.write('//write to last slice//\n')
 f.write('ViewWindowList.Current.SliceNumber = \"%i\";\n' %Nz)
 f.write('RoiList.Last.CopyCurvesOnLastSliceToSlice = ViewWindowList.Current.Address;\n')
 f.write('//interpolate between first and last slice//\n')
 f.write('RoiList.Last.InterpolateContours = \"Interpolate between contours\";\n')
 f.write('RoiList.Last.Line2dWidth = \"1\";\n')
 f.write('RoiList.Last.EditCurve.BoxSize = \"3\";\n')
 f.write('RoiList.Last.Color = \"grey\";\n')
 f.write('RoiList.Last.RoiInterpretedType = \"SUPPORT\";\n')
 f.write('RoiList.Last.OverrideDensity = 1;\n')
 f.write('RoiList.Last.Density = \"0\";\n')
 f.write('RoiList.Last.Display2d = \"Off\";\n')
 f.write('\n')

 f.write('ViewWindowList.Current.SliceNumber = \"1\";\n')
 f.write('//shell outer contour//\n')
 f.write('CreateNewROI = \"Add ROI\";\n')
 f.write('RoiList.Last.Name = \"couchTrilogy\";\n')
 f.write('RoiList.Last.EditCurve = {\n')
 f.write(' SliceCoordinate = %.3f;\n' %z0)
 f.write(' Curve = {\n')
 f.write('  NumberOfPoints = 44;\n')
 f.write('  Points[] = {\n')
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.503+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-19.128+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-12.752+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-6.376+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(0+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(6.376+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(12.752+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(19.128+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.503+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.708+x_m+xSh,x0,dx), ctcoor(-0.024+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.916+x_m+xSh,x0,dx), ctcoor(-0.095+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.118+x_m+xSh,x0,dx), ctcoor(-0.217+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.271+x_m+xSh,x0,dx), ctcoor(-0.364+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.328+x_m+xSh,x0,dx), ctcoor(-0.446+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.411+x_m+xSh,x0,dx), ctcoor(-0.597+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.491+x_m+xSh,x0,dx), ctcoor(-0.891+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.5+x_m+xSh,x0,dx), ctcoor(-0.997+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.5+x_m+xSh,x0,dx), ctcoor(-1.448+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.5+x_m+xSh,x0,dx), ctcoor(-1.899+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.481+x_m+xSh,x0,dx), ctcoor(-1.998+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.418+x_m+xSh,x0,dx), ctcoor(-2.104+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.2+x_m+xSh,x0,dx), ctcoor(-2.200+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(19.65+x_m+xSh,x0,dx), ctcoor(-2.200+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(13.1+x_m+xSh,x0,dx), ctcoor(-2.200+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(6.55+x_m+xSh,x0,dx), ctcoor(-2.200+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(0+x_m+xSh,x0,dx), ctcoor(-2.200+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-6.55+x_m+xSh,x0,dx), ctcoor(-2.200+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-13.1+x_m+xSh,x0,dx), ctcoor(-2.200+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-19.65+x_m+xSh,x0,dx), ctcoor(-2.200+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.2+x_m+xSh,x0,dx), ctcoor(-2.200+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.418+x_m+xSh,x0,dx), ctcoor(-2.104+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.481+x_m+xSh,x0,dx), ctcoor(-1.998+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.5+x_m+xSh,x0,dx), ctcoor(-1.899+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.5+x_m+xSh,x0,dx), ctcoor(-1.448+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.5+x_m+xSh,x0,dx), ctcoor(-0.997+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.491+x_m+xSh,x0,dx), ctcoor(-0.891+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.411+x_m+xSh,x0,dx), ctcoor(-0.597+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.328+x_m+xSh,x0,dx), ctcoor(-0.446+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.271+x_m+xSh,x0,dx), ctcoor(-0.364+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.118+x_m+xSh,x0,dx), ctcoor(-0.217+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.916+x_m+xSh,x0,dx), ctcoor(-0.095+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.011+x_m+xSh,x0,dx), ctcoor(-0.141+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.708+x_m+xSh,x0,dx), ctcoor(-0.024+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f\n' %(ctcoor(-25.503+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  };\n')
 f.write(' };\n')
 f.write('};\n')
 f.write('RoiList.Last.CopyEditCurveToNewCurveAndClear = \"\";\n')
 f.write('\n')

 f.write('//shell inner contour//\n')
 f.write('RoiList.Last.EditCurve = {\n')
 f.write(' SliceCoordinate = %.3f;\n' %z0)
 f.write(' Curve = {\n')
 f.write('  NumberOfPoints = 32;\n')
 f.write('  Points[] = {\n')
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.503+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(15.302+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(5.101+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-5.101+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-15.302+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.503+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.79+x_m+xSh,x0,dx), ctcoor(-0.475+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.925+x_m+xSh,x0,dx), ctcoor(-0.579+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.041+x_m+xSh,x0,dx), ctcoor(-0.745+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.096+x_m+xSh,x0,dx), ctcoor(-0.956+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.1+x_m+xSh,x0,dx), ctcoor(-0.997+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.1+x_m+xSh,x0,dx), ctcoor(-1.349+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.1+x_m+xSh,x0,dx), ctcoor(-1.700+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.089+x_m+xSh,x0,dx), ctcoor(-1.744+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.054+x_m+xSh,x0,dx), ctcoor(-1.784+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.001+x_m+xSh,x0,dx), ctcoor(-1.800+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-17.334+x_m+xSh,x0,dx), ctcoor(-1.800+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-8.667+x_m+xSh,x0,dx), ctcoor(-1.800+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(0+x_m+xSh,x0,dx), ctcoor(-1.800+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(8.667+x_m+xSh,x0,dx), ctcoor(-1.800+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(17.334+x_m+xSh,x0,dx), ctcoor(-1.800+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.001+x_m+xSh,x0,dx), ctcoor(-1.800+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.054+x_m+xSh,x0,dx), ctcoor(-1.784+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.089+x_m+xSh,x0,dx), ctcoor(-1.744+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.1+x_m+xSh,x0,dx), ctcoor(-1.700+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.1+x_m+xSh,x0,dx), ctcoor(-1.349+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.1+x_m+xSh,x0,dx), ctcoor(-0.997+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.096+x_m+xSh,x0,dx), ctcoor(-0.956+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.041+x_m+xSh,x0,dx), ctcoor(-0.745+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.925+x_m+xSh,x0,dx), ctcoor(-0.579+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.79+x_m+xSh,x0,dx), ctcoor(-0.475+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f\n' %(ctcoor(25.503+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  };\n')
 f.write(' };\n')
 f.write('};\n')
 f.write('RoiList.Last.CopyEditCurveToNewCurveAndClear = \"\";\n')
 f.write('//write to last slice//\n')
 f.write('ViewWindowList.Current.SliceNumber = \"%i\";\n' %Nz)
 f.write('RoiList.Last.CopyCurvesOnLastSliceToSlice = ViewWindowList.Current.Address;\n')
 f.write('//interpolate between first and last slice//\n')
 f.write('RoiList.Last.InterpolateContours = \"Interpolate between contours\";\n')
 f.write('RoiList.Last.Display2dWithMeshCheck = \"Poly\";\n')
 f.write('RoiList.Last.Line2dWidth = \"1\";\n')
 f.write('RoiList.Last.EditCurve.BoxSize = \"3\";\n')
 f.write('RoiList.Last.RoiInterpretedType = \"SUPPORT\";\n')
 f.write('RoiList.Last.Color = \"yellow\";\n')
 f.write('RoiList.Last.OverrideDensity = 1;\n')
 f.write('RoiList.Last.Density = \".6\";\n')
 f.write('RoiList.Last.AutoUpdateContours = 1;\n')
 f.write('\n')

 #finish writing ROI

 f.write('\n')
 f.close()

if __name__ == "__main__":
 ptFolder = str(sys.argv[1])
 createTable(ptFolder)
