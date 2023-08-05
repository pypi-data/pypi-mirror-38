/**********************************************************
  Include file for Toribash PovRay exporter (http://www.toribash.com)
  By Hampa 2006
  To produce a screenshot.pov hit F8 inside toribash
  This file should be rendered with PovRay (http://www.povray.org)
  NOTE! All Y values needs to be negated to match Toribash coordinate system
************************************************************/

global_settings {
  assumed_gamma 1.0
    radiosity {
      pretrace_start 0.08           // start pretrace at this size
      pretrace_end   0.04           // end pretrace at this size
      count 35                      // higher -> higher quality (1..1600) [35]
      nearest_count 5               // higher -> higher quality (1..10) [5]
      error_bound 1.8               // higher -> smoother, less accurate [1.8]
      recursion_limit 3             // how much interreflections are calculated (1..5+) [3]
      low_error_factor .5           // reduce error_bound during last pretrace step
      gray_threshold 0.0            // increase for weakening colors (0..1) [0]
      minimum_reuse 0.015           // reuse of old radiosity samples [0.015]
      brightness 1                  // brightness of radiosity effects (0..1) [1]
      adc_bailout 0.01/2
    }
}
#default {
  texture {
    pigment {rgb 1}
      finish {
        ambient 0.0
        diffuse 0.6
        specular 0.3
      }
  }
}

background { color rgb <1,1,1> }

#macro Camera( xpos, ypos, zpos, lookatx, lookaty, lookatz)
camera {
location <xpos,-ypos, zpos>
sky <0, 0, 1>
look_at <lookatx, -lookaty, lookatz>
}
light_source { <xpos, -ypos, 1> color rgb <1,1,1>}
#end

  
/*
sky_sphere {
  pigment {
    gradient z
    color_map {
      [0.0 rgb <0.6,0.7,1.0>]
      [0.7 rgb <0.0,0.1,0.8>]
    }
  }
} 
*/



// JOINTS
#macro Joint(xpos,ypos,zpos,Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
sphere { <xpos, -ypos, zpos>, Radius
	pigment { color rgb <1, 1, 1> }
	finish  { reflection 0.4       }
}
#end

// BLOOD
#macro Blood (xpos, ypos, zpos, Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
sphere {<xpos, -ypos, zpos>, Radius*5, 1 
	pigment { color rgb <0.8, 0, 0 > }
	finish  { reflection 0.4       }
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
        pigment { color rgb <r, g, b> }
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
	pigment { color rgb <r, g, b> }
}
#end

// BODY PART
#macro Body (r, g, b, sidex, sidey, sidez, rot0, rot3, rot6,  rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
box {
	<-(sidex*0.5), -(sidey*0.5), -(sidez*0.5)>,
	<sidex*0.5, sidey*0.5, sidez*0.5>

	matrix <
	rot0, -rot1, rot2, 
	rot3, -rot4, rot5, 
	rot6, -rot7, rot8, 
	rot9, -rot10, rot11> // y == x

	pigment { color rgb <r, g, b> }

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
	pigment { rgb <1,1,1> }
	/*
	finish {
		ambient .1
			diffuse .1
			specular 1
			roughness .001
			metallic
			reflection {
				.75
					metallic
			}
	}  
	*/
}



