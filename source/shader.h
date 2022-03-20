#ifndef __shader_h_
#define __shader_h_

#include <fstream>
#include "def.h"

#define MAX_NAME 100


class shader;
extern std::vector<shader> Shaders;

class shader
{
private:
  CHAR name[MAX_NAME];
  UINT prgNo;

public:
  shader() = default;

private:
  /* Put out log of shader function. */
  static VOID logOut( const CHAR *FileName, const CHAR *Stage, const CHAR *Text )
  {
    FILE *F;

    if ((F = fopen("su1{SHAD}33.LOG", "a")) != NULL)
    {
      fprintf(F, "%s\n  %s: %s\n", FileName, Stage, Text);
      fclose(F);
    }
  }

  /* Load flag.glsl file for shader function. */
  static std::string loadTxtFragFile( const CHAR *prefix, const CHAR *fileName );

  /* Load *.glsl (exept flag.glsl) file for shader function. */
  static std::string loadTxtFile( const CHAR *prefix, const CHAR *fileName )
  {
    std::fstream f(fileName);
    return std::string(std::istreambuf_iterator<CHAR>(f), std::istreambuf_iterator<CHAR>());
  }


  /* Load shader with compiling function. */
  static UINT loadShd( const CHAR *FileNamePrefix )
  {
    INT
      i, res,
      shd_type[] =
    {
      GL_VERTEX_SHADER, GL_TESS_CONTROL_SHADER, GL_TESS_EVALUATION_SHADER,
      GL_GEOMETRY_SHADER, GL_FRAGMENT_SHADER
    };
    const CHAR *suff[] = {"VERT", "CTRL", "EVAL", "GEOM", "FRAG"};
    INT NS = sizeof(suff) / sizeof(suff[0]);
    UINT prg = 0, shd[sizeof(suff) / sizeof(suff[0])] = {0};
    BOOL isok = TRUE;
    std::string txt;
    static CHAR buf[500];

    /* Load shaders */
    for (i = 0; isok && i < NS; i++)
    {
      /* Load text file */
      sprintf(buf, "shaders/%s/%s.GLSL", FileNamePrefix, suff[i]);
      if (i == 4) // Only for 'frag' shader
      {
        try
        {
          if ((txt = shader::loadTxtFragFile(FileNamePrefix, buf)).empty())
            continue;
        }
        catch (std::exception &e )
        {
          MessageBeep(MB_OK);
          MessageBox(NULL, e.what(), "FRAG SHADER ERROR!!!", MB_OK);
          exit(0);
        }
      }
      else
        if ((txt = shader::loadTxtFile(FileNamePrefix, buf)).empty())
          continue;

      /* Create shader */
      if ((shd[i] = glCreateShader(shd_type[i])) == 0)
      {
        txt.clear();
        shader::logOut(FileNamePrefix, suff[i], "Error create shader");
        isok = FALSE;
        break;
      }
      /* Attach text to shader  */
      const CHAR *tmp_txt = txt.c_str();
      glShaderSource(shd[i], 1, &tmp_txt, NULL);
      txt.clear();

      /* Compile shader */
      glCompileShader(shd[i]);
      glGetShaderiv(shd[i], GL_COMPILE_STATUS, &res);
      if (res != 1)
      {
        glGetShaderInfoLog(shd[i], sizeof(buf), &res, buf);
        shader::logOut(FileNamePrefix, suff[i], buf);
        isok = FALSE;
        break;
      }
    }

    /* Create program */
    if (isok)
      if ((prg = glCreateProgram()) == 0)
        isok = FALSE;
      else
      {
        /* Attach shaders to program */
        for (i = 0; i < NS; i++)
          if (shd[i] != 0)
            glAttachShader(prg, shd[i]);

        /* Link program */
        glLinkProgram(prg);
        glGetProgramiv(shd[i], GL_LINK_STATUS, &res);
        if (res != 1)
        {
          glGetProgramInfoLog(prg, sizeof(buf), &res, buf);
          shader::logOut(FileNamePrefix, "LINK", buf);
          isok = FALSE;
        }
      }

    /* Error handle */
    if (!isok)
    {
      for (i = 0; i < NS; i++)
        if (shd[i] != 0)
        {
          if (prg != 0)
            glDetachShader(prg, shd[i]);
          glDeleteShader(shd[i]);
        }
      if (prg != 0)
        glDeleteProgram(prg);
      return 0;
    }
    return prg;
  } // End of 'loadShd' function

public:

  UINT getPrgNo( VOID )
  {
    return prgNo;
  }

  VOID freeShd( VOID )
  {
    UINT i, n, shds[5];

    if (prgNo == 0)
      return;
    /* Obtain program shaders count */
    glGetAttachedShaders(prgNo, 5, (GLsizei *)&n, shds);
    for (i = 0; i < n; i++)
    {
      glDetachShader(prgNo, shds[i]);
      glDeleteShader(shds[i]);
    }
    glDeleteProgram(prgNo);
  }

  static shader addShd( const CHAR *FileNamePrefix )
  {
    shader New;
    New.prgNo = loadShd(FileNamePrefix);
    strncpy(New.name, FileNamePrefix, MAX_NAME - 1);
    Shaders.push_back(New);
    return New;
  }

  /* Update all shaders from store table function. */
  VOID update( VOID )
  {
    this->freeShd();
    prgNo = loadShd(name);
  }


};

#endif // __shader_h_
