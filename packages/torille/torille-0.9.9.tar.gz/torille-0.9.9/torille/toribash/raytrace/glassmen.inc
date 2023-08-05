/* Persistence of Vision Ray Tracer Scene Description File
 File: glassmen.inc
 Vers: 3.6
 Desc: Glassmen - Toribash rendering
 Date: 10/05/2007
 Auth: EvilPNMI
 Contributors : slainveteran, Hampa for their .inc files (yes I copied some parts of them, sorry :p)
 Comments : I've taken (one more time) slainveteran's identify.inc and played around with materials, lights and all. Here is the result. Enjoy :) 
*/

// GENERAL
#version 3.6;

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

background { color rgb <1,1,1> }

#macro Camera( xpos, ypos, zpos, lookatx, lookaty, lookatz)
camera {
location <xpos,-ypos, zpos>
sky <0, 0, 1>
look_at <lookatx, -lookaty, lookatz>
}
light_source { <xpos, -ypos, 1> color rgb <1,1,1>}
#end  

// CAMERA 
#macro Camera( xpos, ypos, zpos, lookatx, lookaty, lookatz)
camera {
location <xpos,-ypos, zpos>
sky <0, 0, 1>
look_at <lookatx, -lookaty, lookatz>
}

/*// ATMOSPHERE
// Commented to ease up rendering, if you want to enable, uncomment !
media {    // atmospheric media sample
  intervals 10
  scattering { 1, rgb 0.03 }
  samples 1, 10
  confidence 0.9999
  variance 1/1000
  ratio 0.9
} */  

/*// AREA LIGHT
// Stronger than the activated one, slower to render too. If you want to enable, uncomment !
light_source {
  0*x                 // light's position (translated below)
  color rgb 1.0       // light's color
  area_light
  <8, 0, 0> <0, 0, 8> // lights spread out across this distance (x * z)
  4, 4                // total number of lights in grid (4x*4z = 16 lights)
  adaptive 0          // 0,1,2,3...
  //jitter              // adds random softening of light
  circular            // make the shape of the light circular
  orient              // orient light
  translate <xpos, -ypos, 40>   // <x y z> position of light
} */

// SPOTLIGHT
light_source {
  0*x                     // light's position (translated below)
  color rgb <1,1,1>       // light's color
  spotlight               // this kind of light source
  translate <xpos, -ypos, 120> // <x y z> position of light
  point_at <0, 0, 0>      // direction of spotlight
  radius 5                // hotspot (inner, in degrees)
  tightness 50            // tightness of falloff (1...100) lower is softer, higher is tighter
  falloff 8               // intensity falloff radius (outer, in degrees)
}


//SKY SPHERE
sky_sphere {
  pigment {
    gradient z
    color_map {
      [0.1 rgb <0.9,0.9,1>]
      [0.7 rgb <0.0,0.1,0.2>]
    }
  }
}   

// GROUND
// plane {<A, B, C>, D } where: A*x + B*y + C*z = D
plane {
  z, // <X Y Z> unit surface normal, vector points "away from surface"
  -1.0 // distance from the origin in the direction of the surface normal
  hollow on // has an inside pigment?
 }
#end

// HEADS part 1
// I'm absolutely cray of including my head into the rendering, thanks fort that slain !

// Player A's (red in-game) colour.

#declare playerAr=0.8;
#declare playerAg=0.3;
#declare playerAb=0.3;

// Player B's (blue in-game) colour.

#declare playerBr=0.3;
#declare playerBg=0.3;
#declare playerBb=0.8;

// Use a head skin and name of skin (takes from the heads folder).
// Player A.

#declare playerAskin=1;
#declare playerAname="head.tga"; // Put your nickname here to change head

// Player B.

#declare playerBskin=1;
#declare playerBname="head.tga";

// heads directory (must include trailing slash ie "dir\\" or "dir/").

#declare headdir="C:/Program Files/Toribash-3.3/raytrace/";

// Are the skinned head reflective (light areas are reflective)

#declare reflectiveheads=1;

#declare playerAname=concat(headdir,playerAname);
#declare playerBname=concat(headdir,playerBname);

#declare player=0;
#declare joint=0;  

// HEADS part 2

#macro BodySphere (r, g, b, Radius,  rot0, rot3, rot6, rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
#declare player=player+1;
union {
	sphere {
        	<0, 0, 0>, Radius
		#if ((player=1 & playerAskin=0) | (player=2 & playerBskin=0))
			pigment { color rgb ( player=1 ? <playerAr,playerAg,playerAb> : <playerBr,playerBg,playerBb> ) }
        		finish  {
				reflection 0.7   
        		        specular 1
				phong 0.5
				metallic
				reflection { .25 metallic }
				}
		#else
			pigment {
				image_map {
					#if (player=1)
						tga playerAname
					#else
						tga playerBname
					#end
				}
				warp {
					spherical
					orientation z
					dist_exp 0
				}
				rotate <90,0,90>
			}
			finish {
				#if (reflectiveheads=1)
					reflection 0.2   
        			        specular 1
					phong 0.5
					metallic
					reflection { .25 metallic }
				#else
					ambient 0.5
				#end
			}
		#end
	}
	#if ((player=1 & playerAskin=0) | (player=2 & playerBskin=0))
		#if (player=1)
			Face (0,0,1, 0.75,0,0, 1,0,0, playerAr*0.25,playerAg*0.25,playerAb*0.25, Radius)
		#else
			Face (0,0,1, 0.75,0,0, 1,0,0, playerBr*0.25,playerBg*0.25,playerBb*0.25, Radius)
		#end
	#end
	matrix <rot0, -rot1, rot2, 
	        rot3, -rot4, rot5, 
	        rot6, -rot7, rot8, 
	        rot9, -rot10, rot11>

}
#end 

// BLOOD from glossy.inc
#macro Blood (xpos, ypos, zpos, Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
threshold 0.1
sphere {<xpos, -ypos, zpos>, Radius*5, 0.1 
	pigment { color rgb <0.8, 0, 0 > }
        finish {
                ambient .1
                diffuse .1
                specular 1
                roughness .001
                reflection { .25 metallic }
	}
}
#end  

// JOINTS
#macro Joint(xpos,ypos,zpos,Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
sphere { <xpos, -ypos, zpos>, Radius
	material { M_Glass }  
	photons {  // photon block for an object
    target 1.0
    refraction on
    reflection on
	}}
#end  


// LEGS
#macro BodyCapsule (r, g, b, Radius, length, rot0, rot3, rot6,  rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
union {
	cylinder { 
		<0,0,-length*0.5>, 
		<0, 0, length - length*0.5>, 
		Radius
	material { M_Glass }  
	photons {  // photon block for an object
    target 1.0
    refraction on
    reflection on
	}	}
	sphere   { <0, 0, -length*0.5>,  Radius 
	material { M_Glass }  
	photons {  // photon block for an object
    target 1.0
    refraction on
    reflection on
	}}
	sphere   { <0, 0, length - length *0.5>, Radius
	material { M_Glass }  
	photons {  // photon block for an object
    target 1.0
    refraction on
    reflection on
	} }

	matrix <rot0, -rot1, rot2, 
	        rot3, -rot4, rot5, 
	        rot6, -rot7, rot8, 
	        rot9, -rot10, rot11>
	/*pigment { color rgb <r, g, b> }*/
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

	material { M_Glass }  
	photons {  // photon block for an object
    target 1.0
    refraction on
    reflection on
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
       

  


