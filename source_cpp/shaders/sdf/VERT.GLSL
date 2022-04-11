#version 430

layout(location = 0) in vec3 InPosition;

uniform float projDist;
uniform int width;
uniform int height;
uniform float wP;
uniform float hP;
uniform vec2 mAngly;
uniform vec3 camDir;
uniform vec3 camRight;
uniform vec3 camUp;
uniform vec3 camAt;
uniform vec3 camLoc;
uniform int mWheel;
uniform vec2 deltaPos;

out vec3 At;
out vec3 camMDir;
out vec3 camMRight;
out vec3 camMUp;
out vec3 camMLoc;
out vec3 camMAt;


mat3x3 rotate( float angleInDegree, vec3 v )
{
  angleInDegree /= 2;
  float sinn = sin(radians(angleInDegree)), coss = cos(radians(angleInDegree));

  float len = length(v), x, y, z;
  if (len != 0 && len != 1)
    len = sqrt(len), x = v.x / len, y = v.y / len, z = v.z / len;
  else
    x = v.x, y = v.y, z = v.z;
  x *= sinn;
  y *= sinn;
  z *= sinn;
  return mat3x3(vec3(1 - 2 * (y * y + z * z), 2 * x * y - 2 * coss * z, 2 * coss * y + 2 * x * z),
    vec3(2 * x * y + 2 * coss * z,  1 - 2 * (x * x + z * z), 2 * y * z - 2 * coss * x),
    vec3(2 * x * z - 2 * coss * y, 2 * coss * x + 2 * y * z,  1 - 2 * (x * x + y * y)));
}

void main( void )
{
  // Rrotation around Y
  camMDir = camDir, camMRight = camRight, camMUp = camUp;
  mat3x3 rY = mat3x3(vec3( cos(radians(mAngly.x)), 0, -sin(radians(mAngly.x))),
                     vec3(0, 1, 0),
                     vec3(sin(radians(mAngly.x)), 0, cos(radians(mAngly.x))));
  camMDir = normalize(rY * camDir);
  camMRight = normalize(rY * camRight);
  camMUp = normalize(rY * camUp);

  // Rrotation around right of camera
  // float si = sin(radians(mAngly.y)), co = sin(radians(mAngly.y));
  // mat3x3 rR = mat3x3(vec3(co + camMRight.x * camMRight.x * (1 - co),
  //                         camMRight.x * camMRight.y * (1 - co)- camMRight.z * si,
  //                         camMRight.x * camMRight.z * (1 - co) + camMRight.y * si),
  //                    vec3(camMRight.y * camMRight.x * (1 - co) + camMRight.z * si,
  //                         co + camMRight.y * camMRight.y * (1 - co),
  //                         camMRight.y * camMRight.z * (1 - co) - camMRight.x * si),
  //                    vec3(camMRight.z * camMRight.x * (1 - co) - camMRight.y * si,
  //                         camMRight.z * camMRight.y * (1 - co) + camMRight.x * si,
  //                         co + camMRight.z * camMRight.z * (1 - co)));
  mat3x3 rR = rotate(mAngly.y, camMRight);
  camMDir = normalize(rR * camMDir);
  camMUp = normalize(rR * camMUp);

  camMLoc = camLoc + camMDir * mWheel / 100 +
    camMRight * deltaPos.x / 10. + camMUp * deltaPos.y / 10.;

  vec3[] A =
    {camMDir * projDist + camMRight *         (0.5 - width / 2) * wP / width + camMUp * (0.5 - height / 2) * hP / height,            // vec3(-1, -1, 0)
     camMDir * projDist + camMRight *         (0.5 - width / 2) * wP / width + camMUp * (height + 0.5 - height / 2) * hP / height,   //  vec3(-1, 1, 0)
     camMDir * projDist + camMRight * (width + 0.5 - width / 2) * wP / width + camMUp * (0.5 - height / 2) * hP / height,            //  vec3(1, -1, 0)
     camMDir * projDist + camMRight * (width + 0.5 - width / 2) * wP / width + camMUp * (height + 0.5 - height / 2) * hP / height,}; //   vec3(1, 1, 0)

  gl_Position = vec4(-1 * float(gl_VertexID < 2) + 1 * float(gl_VertexID >= 2), 1 * (gl_VertexID % 2) - 1 * ((gl_VertexID + 1)% 2), 0, 1);
  At = A[gl_VertexID];
}
