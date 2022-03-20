#ifndef __def_h_
#define __def_h_

#include <iostream>
#include <vector>
#include <string>
#include <exception>

#define GLEW_STATIC
#include <glew.h>
#include <gl/GL.h>
#include <gl/GLU.h>

#pragma comment(lib, "glew32s")
#pragma comment(lib, "opengl32")
#pragma comment(lib, "glu32")

#include "mth.h"

typedef unsigned char byte;

typedef mth::vec3<FLOAT> vec3;
typedef mth::matr<FLOAT> matr;


#endif // __def_h_
