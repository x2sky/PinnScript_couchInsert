####################################
#couchTB_Insert.py
#create subscript that generates the trubeam couch in Pinnacle
#
#Modified:
#2015 12 v1 Becket Hui
#2016 01 v2 Becket Hui add lateral shift
#2016 02 v2.1 Becket Hui change couch density from 0.7 to empirical 0.8
#2016 02 v3 Becket Hui no change in py, Script version changed
#2016 04 v4 Becket Hui change names
####################################
#make sure this file and all other subfiles are stored in script home in main script: couchTB_Insert.py
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
 
 #write scripts to create Truebeam couch
 #heading
 f = open(ptFolder+'createcouchTB.Script','w')

 f.write('////////////////////////\n')
 f.write('//createcouchTB.Script//\n')
 f.write('////////////////////////\n')
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
 f.write('RoiList.Last.Name = \"couchTrueBeam\";\n')
 f.write('RoiList.Last.EditCurve = {\n')
 f.write(' SliceCoordinate = %.3f;\n' %z0)
 f.write(' Curve = {\n')
 f.write('  NumberOfPoints = 82;\n')
 f.write('  Points[] = {\n')
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.137+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-16.758+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-8.379+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(0+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(8.379+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(16.758+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.137+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.488+x_m+xSh,x0,dx), ctcoor(-0.032+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.84+x_m+xSh,x0,dx), ctcoor(-0.150+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.128+x_m+xSh,x0,dx), ctcoor(-0.358+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.191+x_m+xSh,x0,dx), ctcoor(-0.420+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.379+x_m+xSh,x0,dx), ctcoor(-0.710+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.479+x_m+xSh,x0,dx), ctcoor(-1.061+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.474+x_m+xSh,x0,dx), ctcoor(-1.413+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.351+x_m+xSh,x0,dx), ctcoor(-1.764+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.191+x_m+xSh,x0,dx), ctcoor(-2.059+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.857+x_m+xSh,x0,dx), ctcoor(-2.468+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.553+x_m+xSh,x0,dx), ctcoor(-2.819+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.223+x_m+xSh,x0,dx), ctcoor(-3.171+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(24.849+x_m+xSh,x0,dx), ctcoor(-3.522+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(24.434+x_m+xSh,x0,dx), ctcoor(-3.893+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(24.082+x_m+xSh,x0,dx), ctcoor(-4.163+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(23.73+x_m+xSh,x0,dx), ctcoor(-4.415+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(23.457+x_m+xSh,x0,dx), ctcoor(-4.577+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(23.027+x_m+xSh,x0,dx), ctcoor(-4.827+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(22.676+x_m+xSh,x0,dx), ctcoor(-4.995+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(22.324+x_m+xSh,x0,dx), ctcoor(-5.139+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(21.621+x_m+xSh,x0,dx), ctcoor(-5.375+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(20.918+x_m+xSh,x0,dx), ctcoor(-5.547+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(20.566+x_m+xSh,x0,dx), ctcoor(-5.620+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(20.215+x_m+xSh,x0,dx), ctcoor(-5.699+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(19.863+x_m+xSh,x0,dx), ctcoor(-5.768+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(19.512+x_m+xSh,x0,dx), ctcoor(-5.834+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(19.16+x_m+xSh,x0,dx), ctcoor(-5.897+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(18.809+x_m+xSh,x0,dx), ctcoor(-5.949+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(18.457+x_m+xSh,x0,dx), ctcoor(-6.001+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(18.105+x_m+xSh,x0,dx), ctcoor(-6.051+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(17.402+x_m+xSh,x0,dx), ctcoor(-6.131+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(16.699+x_m+xSh,x0,dx), ctcoor(-6.191+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(15.996+x_m+xSh,x0,dx), ctcoor(-6.228+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(15.293+x_m+xSh,x0,dx), ctcoor(-6.246+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(14.59+x_m+xSh,x0,dx), ctcoor(-6.250+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(8.754+x_m+xSh,x0,dx), ctcoor(-6.250+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(2.918+x_m+xSh,x0,dx), ctcoor(-6.250+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-2.918+x_m+xSh,x0,dx), ctcoor(-6.250+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-8.754+x_m+xSh,x0,dx), ctcoor(-6.250+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-14.59+x_m+xSh,x0,dx), ctcoor(-6.250+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-15.293+x_m+xSh,x0,dx), ctcoor(-6.246+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-15.996+x_m+xSh,x0,dx), ctcoor(-6.228+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-16.699+x_m+xSh,x0,dx), ctcoor(-6.191+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-17.402+x_m+xSh,x0,dx), ctcoor(-6.131+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-18.105+x_m+xSh,x0,dx), ctcoor(-6.051+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-18.457+x_m+xSh,x0,dx), ctcoor(-6.001+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-18.809+x_m+xSh,x0,dx), ctcoor(-5.949+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-19.16+x_m+xSh,x0,dx), ctcoor(-5.897+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-19.512+x_m+xSh,x0,dx), ctcoor(-5.834+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-19.863+x_m+xSh,x0,dx), ctcoor(-5.768+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-20.215+x_m+xSh,x0,dx), ctcoor(-5.699+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-20.566+x_m+xSh,x0,dx), ctcoor(-5.620+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-20.918+x_m+xSh,x0,dx), ctcoor(-5.547+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-21.621+x_m+xSh,x0,dx), ctcoor(-5.375+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-22.324+x_m+xSh,x0,dx), ctcoor(-5.139+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-22.676+x_m+xSh,x0,dx), ctcoor(-4.995+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-23.027+x_m+xSh,x0,dx), ctcoor(-4.827+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-23.457+x_m+xSh,x0,dx), ctcoor(-4.577+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-23.73+x_m+xSh,x0,dx), ctcoor(-4.415+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-24.082+x_m+xSh,x0,dx), ctcoor(-4.163+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-24.434+x_m+xSh,x0,dx), ctcoor(-3.893+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-24.849+x_m+xSh,x0,dx), ctcoor(-3.522+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.223+x_m+xSh,x0,dx), ctcoor(-3.171+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.553+x_m+xSh,x0,dx), ctcoor(-2.819+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.857+x_m+xSh,x0,dx), ctcoor(-2.468+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.191+x_m+xSh,x0,dx), ctcoor(-2.059+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.351+x_m+xSh,x0,dx), ctcoor(-1.764+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.474+x_m+xSh,x0,dx), ctcoor(-1.413+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.479+x_m+xSh,x0,dx), ctcoor(-1.061+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.379+x_m+xSh,x0,dx), ctcoor(-0.710+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.191+x_m+xSh,x0,dx), ctcoor(-0.420+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.128+x_m+xSh,x0,dx), ctcoor(-0.358+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.84+x_m+xSh,x0,dx), ctcoor(-0.150+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.488+x_m+xSh,x0,dx), ctcoor(-0.032+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f\n' %(ctcoor(-25.137+x_m+xSh,x0,dx), ctcoor(0.000+CouchRemoveY,y0,dy)))
 f.write('  };\n')
 f.write(' };\n')
 f.write('};\n')
 f.write('RoiList.Last.CopyEditCurveToNewCurveAndClear = \"\";\n')
 f.write('\n')

 f.write('//shell inner contour//\n')
 f.write('RoiList.Last.EditCurve = {\n')
 f.write(' SliceCoordinate = %.3f;\n' %z0)
 f.write(' Curve = {\n')
 f.write('  NumberOfPoints = 68;\n')
 f.write('  Points[] = {\n')
 f.write('  %.3f, %.3f,\n' %(ctcoor(24.785+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(14.871+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(4.957+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-4.957+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-14.871+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-24.785+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.488+x_m+xSh,x0,dx), ctcoor(-0.467+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.857+x_m+xSh,x0,dx), ctcoor(-0.710+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-26.021+x_m+xSh,x0,dx), ctcoor(-1.413+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.84+x_m+xSh,x0,dx), ctcoor(-1.803+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.488+x_m+xSh,x0,dx), ctcoor(-2.241+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-25.295+x_m+xSh,x0,dx), ctcoor(-2.468+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-24.97+x_m+xSh,x0,dx), ctcoor(-2.819+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-24.785+x_m+xSh,x0,dx), ctcoor(-3.002+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-24.434+x_m+xSh,x0,dx), ctcoor(-3.337+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-24.082+x_m+xSh,x0,dx), ctcoor(-3.640+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-23.764+x_m+xSh,x0,dx), ctcoor(-3.874+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-23.379+x_m+xSh,x0,dx), ctcoor(-4.137+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-23.237+x_m+xSh,x0,dx), ctcoor(-4.225+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-22.57+x_m+xSh,x0,dx), ctcoor(-4.577+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-21.973+x_m+xSh,x0,dx), ctcoor(-4.818+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-21.624+x_m+xSh,x0,dx), ctcoor(-4.928+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-21.27+x_m+xSh,x0,dx), ctcoor(-5.027+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-20.918+x_m+xSh,x0,dx), ctcoor(-5.111+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-20.566+x_m+xSh,x0,dx), ctcoor(-5.191+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-20.156+x_m+xSh,x0,dx), ctcoor(-5.280+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-19.512+x_m+xSh,x0,dx), ctcoor(-5.407+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-19.16+x_m+xSh,x0,dx), ctcoor(-5.472+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-18.809+x_m+xSh,x0,dx), ctcoor(-5.532+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-18.132+x_m+xSh,x0,dx), ctcoor(-5.632+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-17.754+x_m+xSh,x0,dx), ctcoor(-5.681+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-17.051+x_m+xSh,x0,dx), ctcoor(-5.752+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-16.348+x_m+xSh,x0,dx), ctcoor(-5.806+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-15.645+x_m+xSh,x0,dx), ctcoor(-5.838+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-14.941+x_m+xSh,x0,dx), ctcoor(-5.850+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(-7.471+x_m+xSh,x0,dx), ctcoor(-5.850+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(0+x_m+xSh,x0,dx), ctcoor(-5.850+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(7.471+x_m+xSh,x0,dx), ctcoor(-5.850+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(14.941+x_m+xSh,x0,dx), ctcoor(-5.850+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(15.645+x_m+xSh,x0,dx), ctcoor(-5.838+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(16.348+x_m+xSh,x0,dx), ctcoor(-5.806+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(17.051+x_m+xSh,x0,dx), ctcoor(-5.752+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(17.754+x_m+xSh,x0,dx), ctcoor(-5.681+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(18.132+x_m+xSh,x0,dx), ctcoor(-5.632+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(18.809+x_m+xSh,x0,dx), ctcoor(-5.532+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(19.16+x_m+xSh,x0,dx), ctcoor(-5.472+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(19.512+x_m+xSh,x0,dx), ctcoor(-5.407+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(20.156+x_m+xSh,x0,dx), ctcoor(-5.280+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(20.566+x_m+xSh,x0,dx), ctcoor(-5.191+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(20.918+x_m+xSh,x0,dx), ctcoor(-5.111+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(21.27+x_m+xSh,x0,dx), ctcoor(-5.027+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(21.624+x_m+xSh,x0,dx), ctcoor(-4.928+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(21.973+x_m+xSh,x0,dx), ctcoor(-4.818+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(22.57+x_m+xSh,x0,dx), ctcoor(-4.577+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(23.237+x_m+xSh,x0,dx), ctcoor(-4.225+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(23.379+x_m+xSh,x0,dx), ctcoor(-4.137+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(23.764+x_m+xSh,x0,dx), ctcoor(-3.874+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(24.082+x_m+xSh,x0,dx), ctcoor(-3.640+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(24.434+x_m+xSh,x0,dx), ctcoor(-3.337+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(24.785+x_m+xSh,x0,dx), ctcoor(-3.002+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(24.97+x_m+xSh,x0,dx), ctcoor(-2.819+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.295+x_m+xSh,x0,dx), ctcoor(-2.468+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.488+x_m+xSh,x0,dx), ctcoor(-2.241+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.84+x_m+xSh,x0,dx), ctcoor(-1.803+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(26.021+x_m+xSh,x0,dx), ctcoor(-1.413+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.857+x_m+xSh,x0,dx), ctcoor(-0.710+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f,\n' %(ctcoor(25.488+x_m+xSh,x0,dx), ctcoor(-0.467+CouchRemoveY,y0,dy)))
 f.write('  %.3f, %.3f\n' %(ctcoor(24.785+x_m+xSh,x0,dx), ctcoor(-0.400+CouchRemoveY,y0,dy)))
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
 f.write('RoiList.Last.Density = \".8\";\n')
 f.write('RoiList.Last.AutoUpdateContours = 1;\n')
 f.write('\n')

 #finish writing ROI

 f.write('\n')
 f.close()

if __name__ == "__main__":
 ptFolder = str(sys.argv[1])
 createTable(ptFolder)
