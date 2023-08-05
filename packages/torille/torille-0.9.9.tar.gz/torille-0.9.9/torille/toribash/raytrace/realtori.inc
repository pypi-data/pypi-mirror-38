/**********************************************************
  Include file for Toribash PovRay exporter (http://www.toribash.com)
  Radisity Include. Made for Toribash 2.1
  By [Ark]DaMehMan 2006
  To produce a screenshot.pov hit F8 inside toribash
  This file should be rendered with PovRay (http://www.povray.org)
  NOTE! All Y values needs to be negated to match Toribash coordinate system
************************************************************/

// Player A's (red in-game) colour.

#declare playerAr=0.3;
#declare playerAg=0.3;
#declare playerAb=0.3;

// Player B's (blue in-game) colour.

#declare playerBr=0.8;
#declare playerBg=0.3;
#declare playerBb=0.3;

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

#declare reflectiveheads=0;

/*********************/
//                   //
//  END OF SETTINGS  //
//                   //
/*********************/

#declare playerAname=concat(headdir,playerAname);
#declare playerBname=concat(headdir,playerBname);

#declare player=0;
#declare joint=0;

global_settings {
        radiosity {
               pretrace_start 0.08
                pretrace_end   0.01
                 count 500

                nearest_count 10
                error_bound 0.02
                recursion_limit 1

                low_error_factor 0.2
                gray_threshold 0.0
                minimum_reuse 0.015
                brightness 1

                adc_bailout 0.01/2
        }
}
    

background { color rgb <1,1,1> }

#macro Camera( xpos, ypos, zpos, lookatx, lookaty, lookatz)
camera {
        location <xpos,-ypos, zpos>
        sky <0, 0, 1>
        look_at <lookatx, -lookaty, lookatz>
}
light_source 
{ 
   <0, 0, 8> rgb <0.8,0.8,0.8> 
    area_light <1, 0, 0>, <0, 0, 1>, 20, 20
    adaptive 1
    jitter
    circular 
 
}
#end

// JOINTS
#macro Joint(xpos, ypos, zpos, Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
sphere { <xpos, -ypos, zpos>, Radius
	pigment { color rgb <0.7, 0.3, 0> }  
}
#end

// BLOOD
#macro Blood (xpos, ypos, zpos, Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
threshold 0.1
sphere {<xpos, -ypos, zpos>, Radius*5, 0.1 
	pigment { color rgb <0.9, 0.1, 0 > }
}
#end 

// HEAD
#macro BodySphere (r, g, b, Radius,  rot0, rot3, rot6, rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
#declare player=player+1;
union {
	sphere {
        	<0, 0, 0>, Radius
		#if ((player=1 & playerAskin=0) | (player=2 & playerBskin=0))
			pigment { color rgb ( player=1 ? <playerAr,playerAg,playerAb> : <playerBr,playerBg,playerBb> ) }
        		finish  {
				reflection 0.7   
//        		        specular 1
//				phong 0.5
				metallic
				reflection { .65 metallic }
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
					reflection 0.7   
        			        specular 1
					phong 0.5
					metallic
					reflection { .65 metallic }
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
	        
	                pigment { color rgb <r, g, b> }
        finish  {
                reflection 0.7   
                specular 1
                phong 0.5
                metallic
	        reflection { .65 metallic }
        }
	                
        //texture
        texture {   // full texture of tile #2
                pigment {       wood
                                /*
                                checker
                                color rgb <1, 1, 1>,
                                color rgb <0, 1, 0>   
                                */
                                scale 0.05 
                                
                               	matrix <rot0, -rot1, rot2, 
	                        rot3, -rot4, rot5, 
	                        rot6, -rot7, rot8, 
	                        rot9, -rot10, rot11>
                }
                finish { specular 0.3 reflection 0.6 }
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
	pigment { color rgb <1, 1, 1> }
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
   
//GROUND
plane { z, 0
	pigment { rgb <1, 1, 1> }
	finish {
		ambient .1
			diffuse .1
			specular 1
			roughness .001
			metallic
			}
}  			

//Create an infinite sphere around scene and allow any pigment on it
sky_sphere {
  pigment {
    gradient z
    color_map { [0.0 color rgb <180/255,230/255,255/255>] [1.0 color blue 0.5] }
  }
}