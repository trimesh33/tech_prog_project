#ifndef __anim_h_
#define __anim_h_

#include "win.h"
#include "shader.h"

/* Time class support (now it's worthless: use chrono.lib) */
class timer
{
public:

  DOUBLE globalTime, globalDelteTime;                                         // Time for counting in seconds
  UINT64 startTime, oldTime, oldTimeFPS, pauseTime, timePerSec, frameCounter; // Time for inner counting

  timer( VOID ) : globalTime(0), globalDelteTime(0), startTime(0), oldTime(0), oldTimeFPS(0), pauseTime(0), timePerSec(0), frameCounter(0) {}

  VOID msgInit( VOID )
  {
    LARGE_INTEGER t;

    QueryPerformanceFrequency(&t);
    timePerSec = t.QuadPart;
    QueryPerformanceCounter(&t);
    startTime = oldTime = oldTimeFPS = t.QuadPart;
    pauseTime = 0;
  }

  VOID msgRender( HWND hWnd )
  {
    static DOUBLE fps;
    static CHAR str[100];

    LARGE_INTEGER t;

    frameCounter++;
    QueryPerformanceCounter(&t);
    globalTime = (DOUBLE)(t.QuadPart - startTime) / timePerSec;
    globalDelteTime = (DOUBLE)(t.QuadPart - oldTime) / timePerSec;
    oldTime = t.QuadPart;

    if (t.QuadPart - oldTimeFPS > timePerSec)
    {
      fps = frameCounter * timePerSec / (DOUBLE)(t.QuadPart - oldTimeFPS);
      sprintf(str, "sdf'schl_proj | FPS: %.5f", fps);
      SetWindowText(hWnd, str);
      oldTimeFPS = t.QuadPart;
      frameCounter = 0;
    }
   }
};


// Class for input processing
class input
{
public:
  INT
    Mx, My, Mz,
    Mdy, Mdx;
  BYTE
    Keys[256], OldKeys[256], ClickKeys[256];

  input() = default;

  VOID msgRender( HWND hWnd )
  {
    // Mouse processing
    POINT pt;
    GetCursorPos(&pt);
    ScreenToClient(hWnd, &pt);
    Mdx = pt.x - Mx;
    Mdy = pt.y - My;
    Mx = pt.x;
    My = pt.y;

    // Keyboard processing
    GetKeyboardState(Keys);
    for (int i = 0; i < 256; i++)
    {
      Keys[i] >>= 7;
      if (!OldKeys[i] && Keys[i])
        ClickKeys[i] = TRUE;
      else
        ClickKeys[i] = FALSE;
    }
    memcpy(OldKeys, Keys, 256);
  }

  // Mouse wheel processing
  VOID msgMouseWheel( INT Mdz )
  {
    Mz += Mdz;
  }

};

// Animation class
class anim : private win, timer, input
{
  HDC hDC;                 // Privat context for drawing
  HGLRC hGLRC;             // Constant context for rendering

  shader Shd;              // Schader loader
  mth::camera<FLOAT> Cam;  // Defining a viewpoint

public:
  // Constuctor of 'anim' class
  anim( HINSTANCE hInst ) : win(hInst) {}

  // Animation loop
  VOID Run( VOID )
  {
    win::Run();
  }

private:
  // Initialization of WinAPI, Glut and related devices
  VOID msgInit( HWND hWnd ) override
  {
    this->hWnd = hWnd;

    this->hDC = GetDC(hWnd);

    timer::msgInit();

    PIXELFORMATDESCRIPTOR pfd = {0};
    pfd.nSize = sizeof(PIXELFORMATDESCRIPTOR);
    pfd.nVersion = 1;
    pfd.dwFlags = PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER;
    pfd.iPixelType = PFD_TYPE_RGBA;
    pfd.cColorBits = 32;
    pfd.cDepthBits = 32;
    INT i = ChoosePixelFormat(this->hDC, &pfd);
    DescribePixelFormat(this->hDC, i, sizeof(PIXELFORMATDESCRIPTOR), &pfd);
    SetPixelFormat(this->hDC, i, &pfd);
    hGLRC = wglCreateContext(this->hDC);
    wglMakeCurrent(this->hDC, hGLRC);

    if(glewInit() != GLEW_OK || !(GLEW_ARB_vertex_shader && GLEW_ARB_fragment_shader))
    {
      wglMakeCurrent(NULL, NULL);
      wglDeleteContext(hGLRC);
      ReleaseDC(hWnd, this->hDC);
      MessageBox(NULL, "No OpenGL", "Oh!", MB_OK | MB_ICONERROR);
      return;
    }

    // Shader load
    Shd = shader::addShd("sdf");

    glEnable(GL_DEPTH_TEST);
    glClearColor(static_cast<GLclampf>(0.3), static_cast<GLclampf>(0.5), static_cast<GLclampf>(0.7), 1.);

    Cam.setPos(vec3(0, 5, 5), vec3(0), vec3(0, 1, 0));
    Cam.setProj(1);
    Cam.resize(width, height);
  } // Enf of 'msgInit' function


  VOID msgDestroy( VOID ) override
  {
    // shader reload
    Shd.freeShd();
    wglMakeCurrent(NULL, NULL);
    wglDeleteContext(hGLRC);
    DeleteDC(hDC);
  }

  VOID msgResize( int w, int h ) override
  {
    RECT rc;
    GetWindowRect(hWnd, &rc);
    SetWindowPos(hWnd, topMost ? HWND_TOPMOST : HWND_NOTOPMOST, rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top, NULL);

    width = w, height = h;
    glViewport(0, 0, w, h);
    Cam.resize(w, h);
  }


  VOID msgCopyFrame( VOID ) override
  {
    SwapBuffers(this->hDC);
  }


  VOID msgRender( VOID ) override;

  VOID msgMouseWheel( INT Mz ) override
  {
     input::msgMouseWheel(Mz);
  }

  VOID msgIdle( VOID ) override
  {
    Render();
  }

  VOID Render( VOID );
};

#endif // __anim_h_
