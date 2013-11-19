#
# PowerCASE 4.2c.433z Recorded Script
# Date: Fri Sep 17 09:12:42 2010
#

case0 = getCurrentCase()

period = '100 timestep'
diameter = '0.02 m'
averaging = '10 timestep'

name = 'rear_lhs'
case0_Dialog = case0.add("Points")
case0_Dialog.setText("Name", "point_"+name)
case0_Dialog.setText("With Respect to Coordinate System", "Frame_Front")
case0_Dialog.set("X", "0.6 m")
case0_Dialog.set("Y", "-0.25 m")
case0_Dialog.set("Z", "0.75 m")
case0_Dialog.set("Displayed Size", ".5 m")
case0_Dialog.ok()

case0_Dialog = case0.add("Measurements")
case0_Dialog.setType("Probe")
case0_Dialog.setText("Window Name", "probe_"+name)
case0_Dialog.setText("Point", "point_"+name)
case0_Dialog.set("Period", period)
case0_Dialog.setText("Probe Type", "Fluid")
case0_Dialog.set("Probe Diameter", diameter)
case0_Dialog.set("Averaging Interval", averaging)
case0_Dialog.ok()

#  ----
name = 'rear_rhs'
case0_Dialog = case0.add("Points")
case0_Dialog.setText("Name", "point_"+name)
case0_Dialog.setText("With Respect to Coordinate System", "Frame_Front")
case0_Dialog.set("X", "0.6 m")
case0_Dialog.set("Y", "0.25 m")
case0_Dialog.set("Z", "0.75 m")
case0_Dialog.set("Displayed Size", ".5 m")
case0_Dialog.ok()

case0_Dialog = case0.add("Measurements")
case0_Dialog.setType("Probe")
case0_Dialog.setText("Window Name", "probe_"+name)
case0_Dialog.setText("Point", "point_"+name)
case0_Dialog.set("Period", period)
case0_Dialog.setText("Probe Type", "Fluid")
case0_Dialog.set("Probe Diameter", diameter)
case0_Dialog.set("Averaging Interval", averaging)
case0_Dialog.ok()

#  ----
name = 'fwd_CU'
case0_Dialog = case0.add("Points")
case0_Dialog.setText("Name", "point_"+name)
case0_Dialog.setText("With Respect to Coordinate System", "Frame_Front")
case0_Dialog.set("X", "-0.4 m")
case0_Dialog.set("Y", "0.25 m")
case0_Dialog.set("Z", "0.85 m")
case0_Dialog.set("Displayed Size", ".5 m")
case0_Dialog.ok()

case0_Dialog = case0.add("Measurements")
case0_Dialog.setType("Probe")
case0_Dialog.setText("Window Name", "probe_"+name)
case0_Dialog.setText("Point", "point_"+name)
case0_Dialog.set("Period", period)
case0_Dialog.setText("Probe Type", "Fluid")
case0_Dialog.set("Probe Diameter", diameter)
case0_Dialog.set("Averaging Interval", averaging)
case0_Dialog.ok()

#  ----

