/**********************************************************
  Include file for Toribash PovRay rexporter (http://www.toribash.com)
  By Nokturnal 2006
  To use this file. Change the include directive in screenshot.pov to "glossy.inc"
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


// JOINTS  
#macro Joint(xpos,ypos,zpos,Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
sphere { <xpos, -ypos, zpos>, Radius
	pigment { color rgb <0/255, 0/255, 0/255> }
//	pigment { color rgb <10/255, 10/255, 10/255> } 
	finish  { 
	        reflection 0.0
//	        reflection 0.5
	        diffuse .1
	        specular 1 
	        diffuse .1
        } 
}
#end

// BLOOD
#macro Blood (xpos, ypos, zpos, Radius, xvel, yvel, zvel, xavel, yavel, zavel, r, g, b)
threshold 0.1
sphere {<xpos, -ypos, zpos>, Radius*5, 0.1 
	pigment { color rgb <0.8, 0, 0 > }
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
#macro BodySphere (r, g, b, Radius,  rot0, rot3, rot6, rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
sphere {
        <0, 0, 0>, Radius
    	matrix <rot0, -rot1, rot2, 
	        rot3, -rot4, rot5, 
	        rot6, -rot7, rot8, 
	        rot9, -rot10, rot11>    
         
//        pigment { color rgb <r, g, b> }        
        pigment { color rgb <235/255, 0/255, 0/255> }
        finish  {
//                reflection 0.7  
                reflection 0.0  
                specular 1
                phong 0.5
                metallic
//	        reflection { .65 metallic }
        }        
        //texture
//        texture {   // full texture of tile #2
//                pigment {       wood
//                               /*
//                                checker
//                                color rgb <1, 1, 1>,
//                                color rgb <0, 1, 0>   
//                                */
//                                scale 0.05 
//                                
//                               	matrix <rot0, -rot1, rot2, 
//	                        rot3, -rot4, rot5, 
//	                        rot6, -rot7, rot8, 
//	                        rot9, -rot10, rot11>
//                }
//                finish { specular 0.3 reflection 0.6 }
//        }         
//        
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
//	pigment { color rgb <r, g, b> }
	pigment { color rgb <235/255, 0/255, 0/255> } 
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
#macro Body (r, g, b, sidex, sidey, sidez, rot0, rot3, rot6,  rot1, rot4, rot7,  rot2, rot5, rot8,  rot9, rot10, rot11, xvel, yvel, zvel, xavel, yavel, zavel)
box {
	<-(sidex*0.5), -(sidey*0.5), -(sidez*0.5)>,
	<sidex*0.5, sidey*0.5, sidez*0.5>

	matrix <rot0, -rot1, rot2, 
	        rot3, -rot4, rot5, 
	        rot6, -rot7, rot8, 
	        rot9, -rot10, rot11>

	pigment { color rgb <235/255, 0/255, 0/255> }
//	pigment { color rgb <235/255, 235/255, 235/255> }
  	finish  { 
  	        reflection 0.4
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
	pigment { rgb <1, 1, 1> }
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
}


// Create an infinite sphere around scene and allow any pigment on it
sky_sphere {
  pigment {
    gradient z
    color_map { [0.0 color rgb <180/255,230/255,255/255>] [1.0 color blue 0.5] }
  }
}




