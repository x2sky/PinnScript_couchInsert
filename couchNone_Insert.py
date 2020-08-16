####################################
#couchNone_Insert.py
#create subscript that generates air with no couch in Pinnacle
#
#Modified:
#2016 03 v1 Becket Hui
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
 
 #write scripts to create air
 #heading
 f = open(ptFolder+'createcouchNone.Script','w')

 f.write('//////////////////////////\n')
 f.write('//createcouchNone.Script//\n')
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

 #finish writing ROI

 f.write('\n')
 f.close()

if __name__ == "__main__":
 ptFolder = str(sys.argv[1])
 createTable(ptFolder)
