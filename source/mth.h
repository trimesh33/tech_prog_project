#ifndef __camera_h_
#define __camera_h_

#include <cstdlib>
#include <cstring>
#include <cmath>
#include <cassert>
#include <windows.h>

/* math support */
namespace mth
{
  static long double Dgr2Rad = 0.01745329251994329576L; // deegre to radian convert (multiply)
  static long double Pi = 3.14159265358979323846L;      // pi const

  template<class type> class matr;
  /* math vector class support */
  template<class type>
    class vec3
    {
      friend class matr<type>;

    private:
    public:
      type x, y, z;


      vec3() = default;
      vec3( type x, type y, type z ) : x(x), y(y), z(z) {}
      vec3( type a ) : x(a), y(a), z(a) {}
      vec3( const vec3 &n ) : x(n.x), y(n.y), z(n.z) {}

      vec3 operator-( const vec3 &v ) const
      {
        return vec3(x - v.x, y - v.y, z - v.z);
      }

      type operator&( const vec3 &v ) const
      {
        return x * v.x + y * v.y + z * v.z;
      }

      vec3 operator%( const vec3 &v ) const
      {
        return vec3(y * v.z - z * v.y, z * v.x - x * v.z, x * v.y - y * v.x);
      }

      vec3 normalizing( VOID ) const
      {
        type len = *this & *this;
        if (len != 0 && len != 1)
        {
          len = sqrt(len);
          return vec3(x / len, y / len, z / len);
        }
        return *this;
      }
    }; /* End of 'vec3' class */

  /* camera class support */
  template<class type>
    class camera
    {
    private:
    public:
      vec3<type> loc, dir, right, up, at;
      type wP, hP, projDist;

      /* Setup camera orientation and position in space function. */
      camera & setPos( const vec3<type> &loc, const vec3<type> &at, const vec3<type> &up1 )
      {
        this->loc = loc;
        dir = ((this->at = at) - loc).normalizing();
        right = (dir % up1).normalizing();
        up = right % dir;
        return *this;
      } /* End of 'setPos' function */

      /* Setup camera projection data function. */
      camera & setProj( /* type wP, type hP,*/ type projDist )
      {
        this->projDist = projDist;
        return *this;
      } /* End of 'setProj' function */

      VOID resize( INT width, INT height )
      {
        FLOAT size = 0.5, ratioX = 1, ratioY = 1;

        if (width >= height)
          ratioX *= (FLOAT)width / height;
        else
          ratioY *= (FLOAT)height / width;

        wP = size * ratioX;
        hP = size * ratioY;
      }

    }; /* End of 'camera' class */

  template<class type>
    class matr
    {
    private:
      type a[4][4];

    public:
      /* Constructor function. */
      matr( VOID ) = default;

      matr( type a00, type a01, type a02, type a03,
        type a10, type a11, type a12, type a13,
        type a20, type a21, type a22, type a23,
        type a30, type a31, type a32, type a33 )
      {
        a[0][0] = a00; a[0][1] = a01; a[0][2] = a02; a[0][3] = a03;
        a[1][0] = a10; a[1][1] = a11; a[1][2] = a12; a[1][3] = a13;
        a[2][0] = a20; a[2][1] = a21; a[2][2] = a22; a[2][3] = a23;
        a[3][0] = a30; a[3][1] = a31; a[3][2] = a32; a[3][3] = a33;
      }


      /* Constructor function. */
      matr( type R[4][4] )
      {
        memcpy(a, R, sizeof(a));
      }

      /* Copy constructor function. */
      matr( const matr &m )
      {
        memcpy(a, m.a, sizeof(a));
      }

      /* Get access to the matrix vector function. */
      operator type *( VOID )
      {
        return a[0];
      }

      /* Identity matrix function. */
      static matr identity( VOID )
      {
        return matr({{1, 0, 0, 0},{0, 1, 0, 0},{0, 0, 1, 0},{0, 0, 0, 1}});
      }

      /* Rotate around random vec function. */
      static matr rotate( type angleInDegree, const vec3<type> &v )
      {
        angleInDegree /= 2;
        type sinn = std::sin(angleInDegree * Dgr2Rad), coss = std::cos(angleInDegree * Dgr2Rad);

        type len = v & v, x, y, z;
        if (len != 0 && len != 1)
          len = sqrt(len), x = v.x / len, y = v.y / len, z = v.z / len;
        else
          x = v.x, y = v.y, z = v.z;
        x *= sinn;
        y *= sinn;
        z *= sinn;
        return matr({{ 1 - 2 * (y * y + z * z), 2 * x * y - 2 * coss * z, 2 * coss * y + 2 * x * z, 0},
                     {2 * x * y + 2 * coss * z,  1 - 2 * (x * x + z * z), 2 * y * z - 2 * coss * x, 0},
                     {2 * x * z - 2 * coss * y, 2 * coss * x + 2 * y * z,  1 - 2 * (x * x + y * y), 0},
                     {                       0,                        0,                           1}});
      }

      /* Ratate around X */
      static matr rotateX( type angleInDegree )
      {
        type sinn = std::sin(angleInDegree * Dgr2Rad), coss = std::cos(angleInDegree * Dgr2Rad);

        return matr(1,     0,    0, 0,
                    0,  coss, sinn, 0,
                    0, -sinn, coss, 0,
                    0,     0,    0, 1);
      }

      /* Ratate around Y */
      static matr rotateY( type angleInDegree )
      {
        type sinn = (type)std::sin(angleInDegree * Dgr2Rad), coss = (type)std::cos(angleInDegree * Dgr2Rad);
      
        return matr(coss, 0, -sinn, 0,
                    0,    1,     0, 0,
                    sinn, 0,  coss, 0,
                    0,    0,     0, 1);
      }

      /* Ratate around Z */
      static matr RotateZ( type AngleInDegree )
      {
        type sinn = std::sin(AngleInDegree * Dgr2Rad), coss = std::cos(AngleInDegree * Dgr2Rad);
      
        return matr({{ coss, sinn, 0, 0},
                     {-sinn, coss, 0, 0},
                     {    0,    0, 1, 0},
                     {    0,    0, 0, 1}});
      }

      vec3<type> transformPoint( const vec3<type> &p ) const
      {
        return vec3<type>(p.x * a[0][0] + p.y * a[1][0] + p.z * a[2][0] + a[3][0],
          p.x * a[0][1] + p.y * a[1][1] + p.z * a[2][1] + a[3][1],
          p.x * a[0][2] + p.y * a[1][2] + p.z * a[2][2] + a[3][2]);
      }

      vec3<type> transformPointPerspective( const vec3<type> &p ) const
      {
        type w = p.x * a[0][3] + p.y * a[1][3] + p.z * a[2][3] + a[3][3];

        return vec3<type>((p.x * a[0][0] + p.y * a[1][0] + p.z * a[2][0] + a[3][0]) / w,
          (p.x * a[0][1] + p.y * a[1][1] + p.z * a[2][1] + a[3][1]) / w,
          (p.x * a[0][2] + p.y * a[1][2] + p.z * a[2][2] + a[3][2]) / w);
      }

      vec3<type> transformVector( const vec3<type> &v ) const
      {
        return vec3<type>(v.x * a[0][0] + v.y * a[1][0] + v.z * a[2][0],
          v.x * a[0][1] + v.y * a[1][1] + v.z * a[2][1],
          v.x * a[0][2] + v.y * a[1][2] + v.z * a[2][2]);
      }

      /* Multiply two matrix function. */
      matr operator*( const matr &m ) const
      {
        type r[4][4] = {0};

        for (INT i = 0; i < 4; i++)
          for (INT j = 0; j < 4; j++)
            for (INT k = 0; k < 4; k++)
              r[i][j] += a[i][k] * m.a[k][j];
        return matr(r);
      }
  }; /* End of 'matr' class */

} /* end of 'mth' namespace */

#endif // __camera_h_
