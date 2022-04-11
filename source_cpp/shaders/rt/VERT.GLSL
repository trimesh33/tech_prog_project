#version 430

layout(location = 0) in vec3 InPosition; 

out vec3 At;

uniform float projDist;
uniform float width;
uniform float height;
uniform float wP;
uniform float hP;
uniform vec2 mAngly;
uniform vec3 camDir;
uniform vec3 camRight;
uniform vec3 camUp;

void main( void )
{
  mat3x3 rY = mat3x3(vec3(1, 0, 0),
                     vec3(0, cos(radians(mAngly.y)), sin(radians(mAngly.y))),
                     vec3(0, -sin(radians(mAngly.y)), cos(radians(mAngly.y))));
  mat3x3 rX = mat3x3(vec3(cos(radians(mAngly.x)), 0, -sin(radians(mAngly.x))),
                     vec3(0, 1, 0),
                     vec3(sin(radians(mAngly.x)), 0, cos(radians(mAngly.x))));


  vec3 camMDir = camDir * (rY * rX), camMRight = camRight * (rY * rX), camMUp = camUp * (rY * rX);
  vec3[] A =
    {camMDir * projDist + camMRight *         (0.5 - width / 2) * wP / width + camMUp * (0.5 - height / 2) * hP / height,            // vec3(-1, -1, 0)
     camMDir * projDist + camMRight *         (0.5 - width / 2) * wP / width + camMUp * (height + 0.5 - height / 2) * hP / height,   //  vec3(-1, 1, 0)
     camMDir * projDist + camMRight * (width + 0.5 - width / 2) * wP / width + camMUp * (0.5 - height / 2) * hP / height,            //  vec3(1, -1, 0)
     camMDir * projDist + camMRight * (width + 0.5 - width / 2) * wP / width + camMUp * (height + 0.5 - height / 2) * hP / height,}; //   vec3(1, 1, 0)
  gl_Position = vec4(InPosition, 1);
  At = A[gl_VertexID];
}
