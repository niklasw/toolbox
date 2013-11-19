# Worked for ensight data at least...
print "------------------"
fh=open('nozzleTemperatures.dat','w')
pdi = self.GetInput()
nbp = pdi.GetNumberOfPoints()
vals = pdi.GetPointData().GetScalars("temperature")
for i in range(0,nbp):
  fh.write("%d %e\n" % (i,vals.GetValue(i)))
fh.close()
print "------ done ----------"

print "------------------"
fh=open('nozzleVelocity.dat','w')
pdi = self.GetInput()
nbp = pdi.GetNumberOfPoints()
vals = pdi.GetPointData().GetScalars("velocity")
for i in range(2,3*nbp,3):
  vec=vals.GetValue(i)
  fh.write("%d %e\n" % (i,vec))
fh.close()
print "------ done ----------"
