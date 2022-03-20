#version 430

uniform float time;
uniform vec3 camLoc;
uniform vec2 Md;

in vec3 At;
out vec4 outColor;

struct material
{
  vec3 kd;
  float l;
};

struct light
{
  vec3 p;
  float intensiv;
};

struct sph
{
  float r;
  vec3 c;
  material m;
};

struct intr
{
  bool is;
  float t;
  vec3 N;
};


const int sphCnt = 3, lightCnt = 1;

material M[] = {{vec3(0.7, 0.6, 0), 0},
                {vec3(1, 0, 0), 0}};
sph S[] = {{ 1, vec3(1, 0, 0), M[0]},
           {.3, vec3(-1, 0, 0), M[0]},
           {0.1, vec3(0, 2, 0), M[1]}};
light L[] = {{vec3(0, 5, 0), 1},
             {vec3(0, 0, 0), 0.6}};

intr sphInt( sph s, vec3 org, vec3 dir )
{
  float t;
  vec3 N;
  intr ii = {false, -1, vec3(0)};
  vec4 color = vec4(.3, .5, .7, 1);
  vec3 a = s.c - org;
  float
    oc2 = dot(a, a),
    ok = dot(a, dir),
    ok2 = ok * ok,
    h2 = s.r * s.r - (oc2 - ok2);

  if (oc2 < s.r * s.r)
  {
    intr i = {true, ok + sqrt(h2), normalize(s.c - (org + dir * t))};
    return i;
  }
  if (ok < 0)
    return ii;
  if (h2 < 0)
    return ii;
  intr i = {true, ok - sqrt(h2), normalize(s.c - (org + dir * t))};
  return i;
}

float planeIntr( vec3 N, vec3 P, vec3 Dir, vec3 Org )
{
  if (dot(N, Dir) != 0)
    return (-dot(N, Org) + dot(P, N)) / dot(N, Dir);
  return -1;
}

vec4 sphIntrAll( vec3 org, vec3 dir )
{
  int i;
  intr mint = {false, 1000, vec3(0)};
  material mm;
  vec4 color = vec4(0.3, 0.5, 0.7, 1);

  for (i = 0; i < sphCnt; i++)
  {
    intr intersect = sphInt(S[i], org, dir);
    if (intersect.is && intersect.t < mint.t)
      mint = intersect, mm = S[i].m, color = vec4(mm.kd, 1);
  }

  if (mint.is)
  {
    float difInt = 0;
    for (i = 0; i < lightCnt; i++)
    {
      vec3 ld = L[i].p - normalize((org + dir * mint.t));
      difInt += L[i].intensiv * max(0., dot(ld, mint.N));
    }
    color = vec4(mm.kd * difInt, 1);
  }

  return color;
}

void main( void )
{
  float t, mint = 1000, Treshold = 0.0001;

  outColor = vec4(.3, .5, .7, 1);

  vec3 Org = camLoc + At, Dir = normalize(At);

  outColor = sphIntrAll( Org, Dir);
  // outColor = vec4(Md, 0, 1);
  // if ((t = sphIntr(s[0], Org, Dir)) != -1 && t < mint && t > Treshold)
  // {
  //   mint = t;
  //   outColor = vec4(0, 1, 0, 1);
  // }
  // if ((t = sphIntr(s[1], Org, Dir)) != -1 && t < mint && t > Treshold)
  // {
  //   mint = t;
  //   outColor = vec4(0, 1, 0, 1);
  // }
  // if ((t = planeIntr(vec3(0, -1, 0), vec3(0, -2, 0), Dir, Org)) != -1 && t < mint && t > Treshold)
  // {
  //   mint = t;
  //   outColor = vec4(1, 0, 0, 1);
  // }
}


