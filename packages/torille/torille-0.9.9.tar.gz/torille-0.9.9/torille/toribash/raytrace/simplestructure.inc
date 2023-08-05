/**********************************************************
  Include file for Toribash PovRay rexporter (http://www.toribash.com)
  By Jam0864 2007
  To use this file. Change the include directive in screenshot.pov to "simplestructure.inc"
***********************************************************/

// radiosity (global illumination) settings
global_settings {
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
    //normal on                   // take surface normals into account [off]
    //media on                    // take media into account [off]
    //save_file "file_name"       // save radiosity data
    //load_file "file_name"       // load saved radiosity data
    //always_sample off           // turn sampling in final trace off [on]
    //max_sample 1.0              // maximum brightness of samples
  }
}

// create a box that extends between the 2 specified points
box {
  <-2.5, -2.5, -10>  // one corner position <X1 Y1 Z1>
  < 3.5,  3.5,  0.03>  // other corner position <X2 Y2 Z2> 
  // photon block for an object
  photons{
    target 1.0          // spacing multiplier for photons hitting the object
    refraction on
    reflection on
    //collect off       // ignore photons            
    //pass_through      // do not influence photons


    
}   
}  

// create a box that extends between the 2 specified points
box {
  <-2.5, -2.5, -1>  // one corner position <X1 Y1 Z1>
  < -2.0,  -1.5,  5>  // other corner position <X2 Y2 Z2>
}

// create a box that extends between the 2 specified points
box {
  <3.0, -2.5, -1>  // one corner position <X1 Y1 Z1>
  < 3.5,  -1.5,  5>  // other corner position <X2 Y2 Z2>
}


// create a box that extends between the 2 specified points
box {
  <2.5, 3.5, -1>  // one corner position <X1 Y1 Z1>
  < 3.5,  3.0,  5>  // other corner position <X2 Y2 Z2>
} 

// create a box that extends between the 2 specified points
box {
  <-2.5, 3.5, -1>  // one corner position <X1 Y1 Z1>
  < -1.5,  3.0,  5>  // other corner position <X2 Y2 Z2>
}   

// create a box that extends between the 2 specified points
box {
  <-2.5, -2.5, 5>  // one corner position <X1 Y1 Z1>
  < 3.5,  3.5,  5.5>  // other corner position <X2 Y2 Z2> 
  // photon block for an object
  photons{
    target 1.0          // spacing multiplier for photons hitting the object
    refraction on
    reflection on
    //collect off       // ignore photons            
    //pass_through      // do not influence photons
    
}   
}















   

background { color rgb <1, 1, 1> }
#macro Camera( xpos, ypos, zpos, lookatx, lookaty, lookatz)
camera {
        //ultra_wide_angle
        location <xpos,-ypos, zpos>
        sky <0, 0, 1>
        look_at <lookatx, -lookaty, lookatz>
        //right x*image_width/image_height
        //angle 180

        
}
/* no light source at all */
//light_source { <xpos, -ypos, 1> color rgb <1,1,0>}
#end
  
// JOINTS  
#macro Joint(xpos,ypos,zpos,Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
sphere { <xpos, -ypos, zpos>, Radius
	pigment { color rgb <10/255, 100/255, 255/255> } 
	finish  { 
	        reflection 0.6
	        diffuse .9
	        specular 1
	         
	                        
        } 
}
#end
// BLOOD
#macro Blood (xpos, ypos, zpos, Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
threshold 0.1
sphere {<xpos, -ypos, zpos>, Radius*5, 0.1 
	pigment { color rgb <255/255, 0/255, 0/255 > }
        finish {
                ambient .1
                diffuse .1
                specular 1
                roughness .001
                metallic
                reflection { .75 metallic }
	}
}
#end    
// HEAD
#macro BodySphere (r, g,b, Radius,  rot0, rot3, rot6, rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
sphere {
        <0, 0, 0>, Radius
    	matrix <rot0, -rot1, rot2, 
	        rot3, -rot4, rot5, 
	        rot6, -rot7, rot8, 
	        rot9, -rot10, rot11> 
        pigment { color rgb <10/255, 100/255, 255/255> }
        finish  {
                reflection 0.4   
                specular 0
                phong 0.5
                metallic
	        reflection { .65 metallic }
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
	pigment { color rgb <10/255, 100/255, 255/255> } 
	finish { 
	        reflection 0.0
                ambient .45
                phong 0.1
                specular 0.9
                roughness .001
        }		
}
#end
// BODY PART
#macro Body (r, g, bs, sidex, sidey, sidez, rot0, rot3, rot6,  rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
box {
	<-(sidex*0.5), -(sidey*0.5), -(sidez*0.5)>,
	<sidex*0.5, sidey*0.5, sidez*0.5>
	matrix <rot0, -rot1, rot2, 
	        rot3, -rot4, rot5, 
	        rot6, -rot7, rot8, 
	        rot9, -rot10, rot11>
	pigment { color rgb <10/255, 100/255, 255/255> }
  	finish  { 
  	        reflection 0.1
  	        ambient 0.4
  	        phong .1
  	        specular 0.9 
  	        roughness .001
        }
}
#end
// GROUND
plane { z, 0
pigment { rgb <0.5, 0.3, 0.2> }
	finish {
		ambient .1
			diffuse 1
		specular 1
			roughness .001
	metallic
			reflection {
				.75
					metallic
			}
	}
}

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

// Create an infinite sphere around scene and allow any pigment on it
sky_sphere {
  pigment {
    gradient z
    color_map { [0.0 color rgb <10/255,150/255,255/255>] [1.0 color rgb <10/255,150/255,255/255>] }
  }
        scale 2
        translate -1
}
