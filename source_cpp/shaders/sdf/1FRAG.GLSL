#version 430

uniform float time;

in vec3 At;
in vec3 camMLoc;

out vec4 outColor;


//// Helper
// Ray struct
struct ray
{
  vec3 org, dir;
};
// Material unit
struct material
{
  vec3 ka;
  float kd, ks, kp;
} M[] = {{vec3(0), 0, 0, 0},                 // [0] none (black)
         {   vec3(.5, .45, .3), .4, .1, 60}, // [1] sand
         {   vec3(.3, .5, .5), .4, .1, 70},  // [2] blue sky
         {   vec3(.7, .3, .2), .4, .1, 70},  // [3] red rose
         {   vec3(.8, 1, .55), .1, .1, 70},  // [4] yellow-green
         {   vec3(.4, 1, .81), .4, .1, 70},  // [5] sea blue
         {vec3(.62, .36, .83), .2, .8, 90},  // [6] purple flower
         {           vec3(.1), .4, .1, 100}};

// Light unit
const int lghCnt = 1;
struct light
{
  vec3 c;
  float intensiv;
} L[] = {{vec3(5, 30, 45), 1},
         {vec3(5), 1.5}};

//// Global const
const float eps = .001;
const float maxDist = 80;

//// Firgures
// Sphere unit
struct sph
{
  float r;
  vec3 c;
};
struct box
{
  vec3 p, size;
};
struct cylinder
{
  vec2 p;
  float r;
};
struct cylinderCapped
{
  float r, h;
};
struct cone
{
  float r, h;
  vec3 c;
};
struct plane
{
  vec4 k;
};
struct tor
{
  float inR, outR;
};
struct tor88
{
  float inR, outR;
};



// Sphere
float fSDF( vec3 p, sph s )
{
  return length(p - s.c) - s.r;
}
// Box
float fSDF( vec3 p, box b )
{
  b.size /= 2;
  vec3 d = abs(p - b.p - b.size) - b.size;
  return length(max(d, 0)) + min(max(d.x, max(d.y, d.z)), 0);
}
// Cylinder
float fSDF( vec3 p, cylinder c )
{
  return length(p.xz - c.p.xy) - c.r;
}
// Cylinder capped
float fSDF( vec3 p, cylinderCapped c )
{
  vec2 d = abs(vec2(length(p.xz), p.y)) - c.h;
  return min(max(d.x, d.y), 0.) + length(max(d, 0.));
}
// Cone
float fSDF( vec3 p, cone c )
{
  p += c.c;
  float phi = atan(c.r / c.h);
  return max(sqrt(p.x * p.x + p.z * p.z) * cos(phi) - abs(p.y) * sin(phi), max(p.y - c.h, -p.y));
}
// Plane
float fSDF( vec3 p, plane c )
{
  return dot(p, c.k.xyz) + c.k.w;
}
// Tor
float fSDF( vec3 p, tor t )
{
  vec2 q = vec2(length(p.xz) - t.outR, p.y);
  return length(q) - t.inR;
}
// Tor88
float fSDF( vec3 p, tor88 t )
{
  vec2 q = vec2(pow(length(p.xz), 1/8) - t.outR, p.y);
  return length(q) - t.inR;
}

//// Intersection module
vec2 opU( vec2 a, vec2 b )
{
  return mix(a, b, a.x > b.x);
}
vec2 opUs( vec2 a, vec2 b, float k )
{
  float j = clamp(.5 + .5 * (b.x - a.x) / k, 0, 1);
  return vec2(mix(b.x, a.x, j) - j * k * (1 - j), a.y);
}
vec2 opS( vec2 b, vec2 a )
{
  return mix(b, -a, -a.x > b.x);
}
vec2 opI( vec2 a, vec2 b )
{
  return mix(b, a, a.x > b.x);
}

mat3x3 rotateX( float ang )
{
  ang = radians(ang);
  return mat3x3(vec3(1,         0,        0),
                vec3(0,  cos(ang), sin(ang)),
                vec3(0, -sin(ang), cos(ang)));
}

mat3x3 rotateY( float ang )
{
  ang = radians(ang);
  return mat3x3(vec3(cos(ang), 0, -sin(ang)),
                vec3(0, 1, 0),
                vec3(sin(ang), 0, cos(ang)));
}

mat3x3 rotateZ( float ang )
{
  ang = radians(ang);
  return mat3x3(vec3(cos(ang), sin(ang), 0),
                vec3(-sin(ang), cos(ang), 0),
                vec3(0, 0, 1));
}

/* start: scene 0 * /
vec2 sceneSDF( vec3 tr )
{
  vec2 mint = vec2(maxDist, 0);

  // for (int i = 0; i < 10; i++)
  //   mint = opU(mint, vec2(fSDF(tr, sph(0.5, vec3(sin(time + 2 * i), i + 4, cos(time + 3 * i)))), 3));

  float l = 5;
  for (int i = 0; i < 10; i++)
    mint = opU(mint, vec2(fSDF(tr, sph(1,
      vec3(sin(i * radians(360/10)) * l, 3, cos(i * radians(360/10))* l ))), 1));
  // mint = opU(mint, vec2(fSDF(tr, tor88(1, 10)), 4));
  mint = opU(mint, vec2(fSDF(tr, sph(2, vec3(0))), 7));
  // mint = opU(mint, vec2(fSDF(tr, plane(vec4(0, 1, 0, 0))), 0));
  return mint;
}
/* end: scene 0 */


/* start: scene 1 * /
vec2 opRep1( vec3 p, vec3 c )
{
  vec3 q = mod(p, c) - 0.5 * c;
  return vec2(fSDF(q, sph(.2, vec3(0))), 0);
}
vec2 sceneSDF( vec3 tr )
{
  vec2 mint = vec2(maxDist, 0);
  mint = opRep1(tr, vec3(2));
  return mint;
}
/* end: scene 1 */

/* start: scene 2 * /
vec2 sceneSDF( vec3 tr )
{
  vec2 mint = vec2(maxDist, 0);

  for (int i = 0; i < 30; i++)
    mint = opU(mint, vec2(fSDF(tr, sph(0.5, vec3(sin(time + 2 * i), i + 4, cos(time + 3 * i)))), max(1, i % 6)));

  float ang = radians(180);
  mat3x3 rX = mat3x3(vec3(1,         0,        0),
                     vec3(0,  cos(ang), sin(ang)),
                     vec3(0, -sin(ang), cos(ang)));
  mint = opU(mint, vec2(fSDF(rX * tr, cone(1, 1, vec3(0, 2, 0))), 3));
  // mint = opU(mint, opS(vec2(fSDF(tr, box(vec3(0), vec3(3))), 1), vec2(fSDF(tr, sph(2, vec3(0))), 1)));
  mint = opU(mint, vec2(fSDF(tr, plane(vec4(0, 1, 0, 0))), 5));
  return mint;
}
/* end: scene 2 */

/* start: scene 3 */
vec2 sceneSDF( vec3 tr )
{
  vec2 mint = vec2(maxDist, 0);

  for (int i = 0; i < 10; i++)
    mint = opU(mint, vec2(fSDF(tr, sph(0.5, vec3(0, 0, i))), max(1, i % 6)));


  // mint = opU(mint,
  //   opI(vec2(fSDF(tr, box(vec3(0, 0, 0), vec3(3 * abs(sin(time)), 3, 3 * abs(cos(time))))), 1),
  //       vec2(fSDF(tr, sph(2, vec3(0, sin(time), 0))), 1)));

  mint = opU(mint,
    opS(opS(opS(vec2(fSDF(tr, sph(2, vec3(4, 4, 4))), 3),
            vec2(fSDF(              tr,     cylinder(vec2(4), 1.2 * abs(sin(time)))), 2)),
            vec2(fSDF(rotateX(90) * tr,     cylinder(vec2(4), 1.2 * abs(sin(time)))), 2)),
            vec2(fSDF(rotateZ(90) * tr, cylinder(vec2(-4, 4), 1.2 * abs(sin(time)))), 2)));

  mint = opU(mint, opUs(vec2(fSDF(tr, box(vec3(0, 0, 0), vec3(3))), 1),
                       vec2(fSDF(tr, sph(2, vec3(0, 0, 3))), 1), .5));

  // mint = opU(mint, vec2(fSDF(tr, plane(vec4(0, 1, 0, 0))), 5));
  return mint;
}
/* end: scene 3 */

/* start: scene 4 * /
vec2 sceneSDF( vec3 tr )
{
  vec2 mint = vec2(maxDist, 0);

  mint = opU(vec2(fSDF(tr, sph(1, vec3(0, 1.5, 0))), 3),
             opU(vec2(fSDF(tr, box(vec3(1, 0, 0), vec3(3))),  7),
                 vec2(fSDF(tr, box(vec3(-4, 0, 0), vec3(3))), 7)));
  return mint;
}
/* end: scene 4 */

vec3 sceneNorm( vec3 r )
{
  return normalize(vec3(sceneSDF(vec3(r.x + eps, r.yz)).x - sceneSDF(vec3(r.x - eps, r.yz)).x,
                        sceneSDF(vec3(r.x, r.y + eps, r.z)).x - sceneSDF(vec3(r.x, r.y - eps, r.z)).x,
                        sceneSDF(vec3(r.xy, r.z + eps)).x     - sceneSDF(vec3(r.xy, r.z - eps)).x));
}

struct intr
{
  vec3 tr;
  vec2 d;
  bool is;
};

intr sphTrace( ray r );

float hardShadowTrace( ray r )
{
  float t = 0, max_t = length(r.dir);
  r.dir = normalize(r.dir);

  while (t < max_t)
  {
    vec3 tr = r.org + r.dir * t;
    vec2 d = sceneSDF(tr);
    if (d.x < eps)
      return .4;
    t += d.x;
  }
  return 1;
}

float softShadowTrace( ray r, float min_t, float max_t, float k )
{
  float t = min_t, shd = 1.;

  while (t < max_t)
  {
    vec2 d = sceneSDF(r.org + r.dir * t);
    if (d.x < min_t)
      return 0.;
    shd = min(shd, k * d.x / t);
    t += d.x;
  }
  return shd;
}


vec3 shade2( vec3 p, vec3 n, material m )
{
  int i = 0;
  float diff = 0, spec = 0, sh = 0;

  for (i = 0; i < 1; i++)
  {
    vec3 ld = normalize(L[0].c - p);
    diff += m.kd * L[i].intensiv * max(dot(n, ld), 0);
    spec += m.ks * pow(max(dot(normalize(-reflect(p, n)), ld), 0), m.kp);
    // sh = hardShadowTrace(ray(p + n * 0.006, L[0].c - p));
    // sh = softShadowTrace(ray(p + n * 0.006, ld), 0.0001, 100, 5);
  }
  return m.ka * sh + diff + spec;
}

vec3 shade( vec3 p, vec3 n, material m )
{
  int i = 0;
  float diff = 0, spec = 0, sh = 1;
  vec3 ref = vec3(0);
  for (i = 0; i < 1; i++)
  {
    vec3 ld = normalize(L[0].c - p);
    diff += m.kd * L[i].intensiv * max(dot(n, ld), 0);
    spec += m.ks * pow(max(dot(normalize(-reflect(p, n)), ld), 0), m.kp);
    // sh = hardShadowTrace(ray(p + n * 0.006, L[0].c - p));
    sh = softShadowTrace(ray(p + n * 0.006, ld), 0.0001, 100, 5);
  }
  // intr obj = sphTrace(ray(p + n * 0.1, normalize(reflect(p, n))));
  // ref = m.ks * mix(vec3(0), M[int(abs(obj.d.y))].ka, obj.is);
  return (m.ka + ref) * sh + diff + spec;
}

intr sphTrace( ray r )
{
  float t = 0;

  while (t < maxDist)
  {
    vec3 tr = r.org + r.dir * t;
    vec2 d = sceneSDF(tr);
    if (d.x < eps)
      return intr(tr, d, true);
    t += d.x;
  }
  return intr((r.dir + vec3(2)) / 2.0, vec2(0), false);
}

void main( void )
{
  ray r = {At + camMLoc, normalize(At)};
  intr i = sphTrace(r);
  outColor = vec4(mix(i.tr, shade(i.tr, sceneNorm(i.tr), M[int(abs(i.d.y))]), i.is), 1);
}
