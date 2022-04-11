// materials + objects
#material{            vec3(0),  0,  0,   0}   // [0] none (black)
#material{  vec3(.5, .45, .3), .4, .1,  60}   // [1] dry sand
#material{   vec3(.3, .5, .5), .4, .001, 70}  // [2] blue sky
#material{   vec3(.7, .3, .2), .4, .1,  70}   // [3] red rose
#material{   vec3(.8, 1, .55), .1, .1,  70}   // [4] yellow-green sun
#material{   vec3(.4, 1, .81), .3, .1,  70}   // [5] ocean blue
#material{vec3(.62, .36, .83), .2, .4,  90}   // [6] purple flower
#material{           vec3(.1), .4, .6, 100}   // [7] ?silver

#light{vec3(5, 30, 45), 1}
#light{vec3(5), 1.5}

'! #define __soft!

'@i10(#opU#sph(1, vec3(sin(i * radians(360/10)) * 5, 10, cos(i * radians(360/10))* 5))#7)
'@i8(#opU#sph(0.5, vec3(sin(time + 2 * i), i, cos(time + 3 * i)))#7)

'#opUs#mrotateX(60)#box(vec3(0, 0, 0), vec3(3 * abs(cos(time)), 3, 3 * abs(sin(time))))#1#mrotateX(30)#sph(2, vec3(0, abs(cos(time)), 0))#1#k4
'#opI#mrotateX(60)#box(vec3(0, 5, 0), vec3(3 * abs(cos(time)), 3, 3 * abs(sin(time))))#1#mrotateX(30)#sph(2, vec3(0, 5 + abs(cos(time)), 0))#1


'#opU#sph(1, vec3(0, 2, 0))#3
'#opU#tor88(1.7, 4)#1
'#opU#vec3(0, -3, 0)#tor88(7, 15)#7

//// landshaft from noise
'#opU#plane(vec4(0, 1, 0, -7 + turb(tr.xz/40, 4)*8 + 10))#1
//// end ////

/// cube with hole
#opU#cylinder(vec2(4), 1.2)#2
#opU#mrotateX(90)#cylinder(vec2(4), 1.2 )#2
#opU#mrotateZ(90)#cylinder(vec2(-4, 4), 1.2)#2
!mint = opS(vec2(fSDF(tr, sph(2, vec3(4, 4, 4))), 5), mint);!
/// end ///

/// many reflection in sphere
'!mint = opRep1(tr, vec3(2));!
/// end ///

/// Axis
'@i8(#opU#sph(0.1, vec3(i, 0, 0))#0)
'@i8(#opU#sph(0.1, vec3(0, i, 0))#0)
'@i8(#opU#sph(0.1, vec3(0, 0, i))#0)
/// end ///

/// cgsg
// c
'@i10(#opU#sph(1, vec3(sin(i * radians(360/15) + radians(160)) * 5, 10, cos(i * radians(360/15) + radians(160))* 5))#7)
// g
'@i15(#opU#sph(1, vec3(10 + sin(i * radians(360/15)) * 5, 10, cos(i * radians(360/15))* 5))#3)
'@i6(#opU#sph(1, vec3(10 + sin(i * radians(360/15) - radians(30)) * 5, 10, 10 + cos(i * radians(360/15) - radians(30))* 5))#3)
'@i8(#opU#sph(1, vec3(15, 10, -6.5 + i * 2))#3)
// s
'@i7(#opU#sph(1, vec3(23 + sin(i * radians(360/10) - radians(190)) * 3, 10, cos(i * radians(360/10) - radians(190)) * 3 - 3))#7)
'@i7(#opU#sph(1, vec3(23 + sin(i * radians(360/10) ) * 3, 10, cos(i * radians(360/10)) * 3 + 3))#7)


/// end ///

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
