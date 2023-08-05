/**********************************************************
  Include file for Toribash PovRay rexporter (http://www.toribash.com)
  By Jam0864 2007
  To use this file. Change the include directive in screenshot.pov to "darkimproved.inc"
***********************************************************/

background { color rgb <1, 1, 1> }

#macro Camera( xpos, ypos, zpos, lookatx, lookaty, lookatz)
camera {
        location <xpos,-ypos, zpos>
        sky <0, 0, 1>
        look_at <lookatx, -lookaty, lookatz>
}
light_source { <xpos, -ypos, 3> rgb <1,1,1> }
#end

  // create a rainbow arc
rainbow {                      
  angle 30         // degrees
  width 6          // degrees
  distance 1000
  direction <0,-0.5,1>    
  jitter 0.01
  arc_angle 180    // degrees
  falloff_angle 60 // degrees
  // up <UP>
  color_map {
    [0.000 color rgbf <1.0, 0.5, 1.0, 1.0> ]
    [0.100 color rgbf <1.0, 0.5, 1.0, 0.8> ]
    [0.214 color rgbf <0.5, 0.5, 1.0, 0.8> ]
    [0.328 color rgbf <0.2, 0.2, 1.0, 0.8> ]
    [0.442 color rgbf <0.2, 1.0, 1.0, 0.8> ]
    [0.556 color rgbf <0.2, 1.0, 0.2, 0.8> ]
    [0.670 color rgbf <1.0, 1.0, 0.2, 0.8> ]
    [0.784 color rgbf <1.0, 0.5, 0.2, 0.8> ]
    [0.900 color rgbf <1.0, 0.2, 0.2, 0.8> ]
  }
}

#declare M_Glass=    // Glass material (template from POV-Ray 3.6)
material {
  texture {
    pigment {rgbt 1}
    finish {
      ambient 0.0
      diffuse 0.05
      specular 0.6
      roughness 0.005
      reflection {
        0.1, 1.0
        fresnel on
      }
      conserve_energy
    }
  }
  interior {
    ior 1.5
    fade_power 1001
    fade_distance 0.9
    fade_color <0.5,0.8,0.6>
  }
}
       
  
  // create a point "spotlight" (conical directed) light source
light_source {
  0*x                     // light's position (translated below)
  color rgb <1,0,0>       // light's color
  spotlight               // this kind of light source
  translate <40, 80, -40> // <x y z> position of light
  point_at <0, 0, 0>      // direction of spotlight
  radius 1                // hotspot (inner, in degrees)
  tightness 50            // tightness of falloff (1...100) lower is softer, higher is tighter
  falloff 8               // intensity falloff radius (outer, in degrees)
}

// set global atmospheric fog effect in the scene.
// at the fog distance, there will be 85% visibility
fog {
  fog_type 1               // 1=constant, 2=ground_fog
  distance 15
  color rgb <10/255, 10/255, 120/255> }               // can also have 'filter' and 'transmit'
  // (---turbulence---)
  //turbulence <0.25, 0.25, 0.5>
  //turb_depth 0.25
  //omega 0.25
  //lambda 1.0
  //octaves 3
  // (---ground fog---)
  //fog_offset 0.4         // height of constant fog
  //fog_alt 0.4            // at fog_offset+fog_alt: density=2%

// An area light (creates soft shadows)
// WARNING: This special light can significantly slow down rendering times!
light_source {
  0*x                 // light's position (translated below)
  color rgb <200/255, 10/255, 10/255>       // light's color
  area_light
  <8, 0, 0> <0, 0, 8> // lights spread out across this distance (x * z)
  4, 4                // total number of lights in grid (4x*4z = 16 lights)
  adaptive 0          // 0,1,2,3...
  jitter              // adds random softening of light
  circular            // make the shape of the light circular
  orient              // orient light
  translate <40, 80, -40>   // <x y z> position of light
}


// Use a head skin and name of skin (takes from the heads folder).
// Player A.

#declare playerAskin=1;
#declare playerAname="head.tga";

// Player B.

#declare playerBskin=1;
#declare playerBname="head.tga";

// heads directory (must include trailing slash ie "dir\\" or "dir/").

#declare headdir="C:/Program Files/Toribash-3.3/raytrace/";

// Are the skinned head reflective (light areas are reflective)

#declare reflectiveheads=1;

// JOINTS  
#macro Joint(xpos,ypos,zpos,Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
sphere { <xpos, -ypos, zpos>, Radius
	pigment { color rgb <10/255, 10/255, 120/255> } 
	finish  { 
	        reflection 2
	        diffuse .1
	        specular 1 
	        diffuse .1
        } 
}
#end

// BLOOD
#macro Blood (xpos, ypos, zpos, Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
threshold 0.005
sphere {<xpos, -ypos, zpos>, Radius*3, 0.01 
	pigment { color rgb <0.7, 0, 0 > }
        finish {
                ambient .1
                diffuse .1
                specular 1
                roughness .001
                metallic
                reflection { 1.5 metallic }
	}
}
#end    


// HEAD
#macro BodySphere (r, g, b, Radius,  rot0, rot3, rot6, rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
sphere {
        <0, 0, 0>, Radius
    	matrix <rot0, -rot1, rot2, 
	        rot3, -rot4, rot5, 
	        rot6, -rot7, rot8, 
	        rot9, -rot10, rot11> 
        pigment { color rgb  <10/255, 10/255, 10/255> }
        finish  {
                reflection 1
                specular 0
                phong 0.5
                metallic
	        reflection { 10 metallic }
        }
}
#end
// LEGS
#macro BodyCapsule (r, g, b, Radius, length, rot0, rot3, rot6,  rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
union {
	cylinder { 
		<0,0,-length*0.5>, 
		<0, 0, length - length*0.5>, 
		Radius
	}
	sphere   { <0, 0, -length*0.5>,  Radius }
	sphere   { <0, 0, length - length *0.5>, Radius }

	matrix <rot0, -rot1, rot2, 
	        rot3, -rot4, rot5, 
	        rot6, -rot7, rot8, 
	        rot9, -rot10, rot11>
	pigment { color rgb <50/255, 50/255, 50/255> }
	finish { 
	        reflection 1
                ambient .45
                phong 0.1
                specular 0.9
                roughness .001
        }		
}
#end

// BODY PART
#macro Body (r, g, b, sidex, sidey, sidez, rot0, rot3, rot6,  rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
box {
	<-(sidex*0.5), -(sidey*0.5), -(sidez*0.5)>,
	<sidex*0.5, sidey*0.5, sidez*0.5>

	matrix <rot0, -rot1, rot2, 
	        rot3, -rot4, rot5, 
	        rot6, -rot7, rot8, 
	        rot9, -rot10, rot11>

	pigment { color rgb <50/255, 50/255, 50/255> }
  	finish  { 
  	        reflection 1
  	        ambient 0.5
  	        phong .5
  	        specular 0.1 
  	        roughness .001
        }
}
#end

#macro EnvBox (r, g, b, a, sidex, sidey, sidez, rot0, rot3, rot6,  rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11)
box {   
        <-(sidex*0.5), -(sidey*0.5), -(sidez*0.5)>,
        <sidex*0.5, sidey*0.5, sidez*0.5>
                
        matrix <rot0, -rot1, rot2, 
                rot3, -rot4, rot5, 
                rot6, -rot7, rot8, 
                rot9, -rot10, rot11>

	//Need Texture for this alpha
        pigment { color rgbf <r, g, b, a> }
	finish  {
                reflection 0.4  
                ambient 0.5     
                phong .5        
                specular 0.1    
                roughness .001
        }       
}  
#end

#macro EnvCapsule (r, g, b, a, Radius, length, rot0, rot3, rot6,  rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11)
union {
        cylinder {
                <0,0,-length*0.5>,
                <0, 0, length - length*0.5>,
                Radius
        }
        sphere   { <0, 0, -length*0.5>,  Radius }
        sphere   { <0, 0, length - length *0.5>, Radius }

        matrix <rot0, -rot1, rot2,
                rot3, -rot4, rot5,
                rot6, -rot7, rot8,
                rot9, -rot10, rot11>
	
	//Need Texture for this alpha
        pigment { color rgbf <r, g, b, a> }
        finish {
                reflection 0.4
                ambient 0.5
                phong .5
                specular 0.1
                roughness .001
        }
}
#end


#macro EnvSphere (r, g, b, a, Radius, rot0, rot3, rot6,  rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11)
sphere {
        <0, 0, 0>, Radius
        matrix <rot0, -rot1, rot2,
                rot3, -rot4, rot5,
                rot6, -rot7, rot8,
                rot9, -rot10, rot11>

	//Need Texture for this alpha
        pigment { color rgbf <r, g, b, a> }
        finish  {
                reflection 0.4
		ambient 0.5
		phong .5
                specular 0.1
                reflection .001
        }
}
#end

#macro Impact (xpos, ypos, zpos, Radius, time, r, g, b, a)
torus {
        Radius, 0.5
	scale <1, 0.05, 1>
	rotate <90, 0, 90>
	translate <xpos, -ypos, zpos>
	
        pigment { 
		color rgb <r, g, b>
		filter (1-a)	//aka alpha 		
	}

        finish  {
       		reflection 0.2
               	ambient 0.5
               	phong .5
               	specular 0.1
               	refraction 1
       	}
}
#end


// GROUND
plane { z, 0
	pigment { rgb <0, 0, 0> }
	finish {
		ambient .1
			diffuse .1
			specular 1
			roughness 100000
			metallic
			reflection {
				10
					metallic
			}
	}
}


// Create an infinite sphere around scene and allow any pigment on it
sky_sphere {
  pigment {
    gradient z
    color_map { [0.0 color rgb <150/255,50/255,25/255>] [1.0 color red 0.5] }
  }
}




