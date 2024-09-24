# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Text explaining script usage
# Parameters:
#  o_lat_deg: Latitude of SEZ origin in deg
#  o_lon_deg: Longitude of SEZ origin in deg
#   o_hae_km: Height above reference ellipsoid of SEZ origin in km
#       s_km: South component of SEZ frame in km
#       e_km: East component of SEZ frame in km
#       z_km: Zenith component of SEZ frame in km
# Output:
#  Outputs ECEF coordinates (x, y, z)
#
# Written by Sean Rockett
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
import math
import sys # argv

# constants
R_E_KM = 6378.1363
E_E = 0.081819221456

# helper functions

def calc_denom(ecc,lat_rad):
    return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad))**2)

# initialize script arguments
o_lat_deg=float('nan')
o_lon_deg=float('nan')
o_hae_km=float('nan')
s_km=float('nan')
e_km=float('nan')
z_km=float('nan')

# parse script arguments
if len(sys.argv)==7:
  o_lat_deg = float(sys.argv[1])
  o_lon_deg = float(sys.argv[2])
  o_hae_km = float(sys.argv[3])
  s_km = float(sys.argv[4])
  e_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 sez_to_ecef o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
  )
  exit()

# write script below this line

# convert SEZ origin into ECEF coordinates
o_lat_rad = o_lat_deg*math.pi/180
o_lon_rad = o_lon_deg*math.pi/180

cos_lat = math.cos(o_lat_rad)
cos_lon = math.cos(o_lon_rad)
sin_lat = math.sin(o_lat_rad)
sin_lon = math.sin(o_lon_rad)

denom = calc_denom(E_E,o_lat_rad)
C_E = R_E_KM/denom
S_E = R_E_KM*(1-E_E*E_E)/denom

o_r_x_km = (C_E+o_hae_km)*cos_lat*cos_lon
o_r_y_km = (C_E+o_hae_km)*cos_lat*sin_lon
o_r_z_km = (S_E+o_hae_km)*sin_lat

# convert SEZ coordinates to local ECEF coordinates
x_km = cos_lon*sin_lat*s_km + cos_lon*cos_lat*z_km - sin_lon*e_km
y_km = sin_lon*sin_lat*s_km + sin_lon*cos_lat*z_km + cos_lon*e_km
z_km = -cos_lat*s_km + sin_lat*z_km

# adding local ECEF coordinates to origin ECEF coordinates
ecef_x_km = x_km+o_r_x_km
ecef_y_km = x_km+o_r_y_km
ecef_z_km = x_km+o_r_z_km

# print output
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)