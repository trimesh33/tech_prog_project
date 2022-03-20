#version 430

uniform float time;

in vec3 At;
in vec3 camMLoc;
in float width;

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
} M[] = {!(material)};

// Light unit
const int lghCnt = !(lightCnt);
struct light
{
  vec3 c;
  float intensiv;
} L[] = {!(light)};

//// Global const
const float eps = .001;
const float maxDist = 300;

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

float len( vec2 v, int n )
{
  return pow(abs((pow(abs(v.x), n)+pow(abs(v.y), n))), 1./n);
}
float len( vec3 v, int n )
{
  return pow(abs((pow(abs(v.x), n)+pow(abs(v.y), n)+pow(abs(v.z), n))), 1./n);
}

// Tor88
float fSDF( vec3 p, tor88 t )
{
  vec2 q = vec2(len(p.xz, 8) - t.outR, p.y);
  return len(q, 8) - t.inR;
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
vec2 opDis( vec3 tr, vec2 a )
{
  float t = 1.2;
  return vec2(a.x + sin(tr.x*t) + cos(tr.y*t) + cos(tr.z*t), a.y);
}
vec2 opRep1( vec3 p, vec3 c )
{
  vec3 q = mod(p, c) - 0.5 * c;
  return vec2(fSDF(q, sph(.2, vec3(0))), 7);
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

//// Noise module

float noise( vec3 p )
{
  return sin(p.x);// * fract(p.z);
}

#define M_PI 3.14159265358979323846

float rand(vec2 co){return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);}
float rand (vec2 co, float l) {return rand(vec2(rand(co), l));}
float rand (vec2 co, float l, float t) {return rand(vec2(rand(co, l), t));}

float perlin(vec2 p, float dim, float time) {
  vec2 pos = floor(p * dim);
  vec2 posx = pos + vec2(1.0, 0.0);
  vec2 posy = pos + vec2(0.0, 1.0);
  vec2 posxy = pos + vec2(1.0);

  float c = rand(pos, dim, time);
  float cx = rand(posx, dim, time);
  float cy = rand(posy, dim, time);
  float cxy = rand(posxy, dim, time);

  vec2 d = fract(p * dim);
  d = -0.5 * cos(d * M_PI) + 0.5;

  float ccx = mix(c, cx, d.x);
  float cycxy = mix(cy, cxy, d.x);
  float center = mix(ccx, cycxy, d.y);

  return center * 2.0 - 1.0;
}

float turb( vec2 p, int oct )
{
  float val = 0, frac = 1;
  for (int i = 0; i < oct; i++)
  {
    val += perlin(p, 3, 1) / frac;
    p *= 2, frac *= 2;
  }
  return val * (1 << (oct - 1)) / ((1 << oct) - 1);
}


/*//////////////////
//  scene start  //
////////////////*/
vec2 sceneSDF( vec3 tr )
{
  vec2 mint = vec2(maxDist, 0);

  ////-landshaft-from-noise-////
  // mint = opU(mint, vec2(fSDF(tr, plane(vec4(0, 1, 0, perlin(tr.xz/40, 2, 1)*8))), 1));
  ////---------end---------////

  //mint = opU(opU(mint, vec2(fSDF(tr, plane(vec4(0, 1, 0, perlin(tr.xz/40, 2, 1)*8))), 1)),
  //                     vec2(fSDF(tr + vec3(0, -20, 0), tor88(7, 15)), 5));

  !(sceneSDF)

  return mint;
}
/*////////////////
//  scene end  //
//////////////*/


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
      return .2;
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

intr reflTrace( ray r, float min_t, float max_t )
{
  float t = 0;

  while (t < max_t)
  {
    vec3 tr = r.org + r.dir * t;
    vec2 d = sceneSDF(tr);
    if (d.x < min_t)
      return intr(tr, d, true);
    t += d.x;
  }
  return intr(vec3(0), vec2(0), false);
}


vec3 shade2( vec3 p, vec3 n, material m )
{
  int i = 0;
  float diff = 0, spec = 0, sh = 1;
  for (i = 0; i < 1; i++)
  {
    vec3 ld = normalize(L[0].c - p);
    diff += m.kd * L[i].intensiv * max(dot(n, ld), 0);
    spec += m.ks * pow(max(dot(normalize(-reflect(p, n)), ld), 0), m.kp);
#ifdef __hard
    sh = hardShadowTrace(ray(p + n * 0.06, L[0].c - p));
#endif // __hard
#ifdef __soft
    sh = clamp(softShadowTrace(ray(p + n * 0.1, ld), 0.0001, 100, 8), .2, 1.);
#endif // __soft
  }
  return (m.ka + diff + spec) * sh;
}

vec3 shade( vec3 p, vec3 n, material m )
{
  int i = 0;
  float diff = 0, spec = 0, sh = 1;
  vec3 ref = vec3(0);
  for (int j = 0; j < 1; j++)
  {
    for (i = 0; i < 1; i++)
    {
      vec3 ld = normalize(L[0].c - p);
      diff += m.kd * L[i].intensiv * max(dot(n, ld), 0);
      spec += m.ks * pow(max(dot(normalize(-reflect(p, n)), ld), 0), m.kp);
#ifdef __hard
      sh = hardShadowTrace(ray(p + n * 0.06, L[0].c - p));
#endif // __hard
#ifdef __soft
      sh = clamp(softShadowTrace(ray(p + n * 0.001, ld), 0.0001, 2, 8), .2, 1.);
#endif // __soft
    }
    intr obj = reflTrace(ray(p + n * .1, -normalize(reflect(p, n))), 0.01, 100);
    ref = m.ks * mix((normalize(At) + vec3(2)) / 2.0, shade2(obj.tr, sceneNorm(obj.tr),M[int(abs(obj.d.y))]), obj.is);
  }
  return ((ref + m.ka) + diff + spec) * sh;
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
  return intr((-r.dir + vec3(2)) / 2.0, vec2(0), false);
}

void main( void )
{
  ray r = {At + camMLoc, normalize(At)};
  intr i = sphTrace(r);
  // outColor = vec4(sceneNorm(i.tr), 1);
  outColor = vec4(mix(i.tr, shade(i.tr, sceneNorm(i.tr), M[int(abs(i.d.y))]), i.is), 1);
  // float t = perlin(gl_FragCoord.xy/50, 2, 1);
  // outColor = vec4(t, t, t, 1);
}
