#ifndef __win_h_
#define __win_h_

#include "def.h"

#define WND_CLASS "trimesh"

class win
{
public:
  HWND hWnd;            // Windows haldler
  HINSTANCE hInst;      // Instanse handler

  INT width, height;    // Size of window
  const UINT
    initTimer = 30,     // Init timer number
    refreshTimer = 33;  // Delay to refresh
  BOOL IsInit = FALSE;  // Defining statment of window initialization
  // INT mouseWheel;
  BOOL lButtonMouse, rButtonMouse; // Mouse buttons statments
  BOOL topMost = false;    // Paramets for windows position

  // Constructor of 'win' class
  win( HINSTANCE hInst ) : hInst(hInst)
  {
    WNDCLASS wc = {0};

    wc.style = CS_VREDRAW | CS_HREDRAW;
    wc.hInstance = hInst;
    wc.hIcon = LoadIcon(NULL, IDI_WARNING);
    wc.lpszClassName = WND_CLASS;
    wc.lpfnWndProc = winFunc;
    wc.cbWndExtra = sizeof(VOID *);

    if (!RegisterClass(&wc))
    {
      MessageBox(NULL, "Register window class failed.", "Oh!", MB_OK | MB_ICONERROR);
      return;
    }

    width = 1024, height = 512;

    hWnd = CreateWindow(WND_CLASS, "sdf'sch project", WS_VISIBLE | WS_OVERLAPPEDWINDOW,
      CW_USEDEFAULT, CW_USEDEFAULT, width, height, NULL, NULL, hInst, (VOID *)this);
  }

  // Windows processing function
  static LRESULT CALLBACK winFunc( HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam )
  {
    win *Win;
    MINMAXINFO *MinMax;
    HDC hDC;
    PAINTSTRUCT ps;

    switch (msg)
    {
    case WM_CREATE:
      SetWindowLong(hWnd, 0, (DWORD)((CREATESTRUCT *)(lParam))->lpCreateParams);
    default:
      Win = (win *)GetWindowLong(hWnd, 0);
      if (Win != 0)
      {
        switch (msg)
        {
        case WM_GETMINMAXINFO:
          MinMax = (MINMAXINFO *)lParam;
          MinMax->ptMaxTrackSize.y = 
            GetSystemMetrics(SM_CYMAXTRACK) +
            GetSystemMetrics(SM_CYCAPTION) +
            GetSystemMetrics(SM_CYMENU) +
            GetSystemMetrics(SM_CYBORDER) * 2;
          return 0;
        case WM_CREATE:
          Win->hWnd = hWnd;
          Win->OnCreate(hWnd);
          return 0;
        case WM_SIZE:
          Win->OnResize(LOWORD(lParam), HIWORD(lParam));
          SendMessage(hWnd, WM_TIMER, 0, 0);
          return 0;
        case WM_LBUTTONDOWN:
          Win->lButtonMouse = TRUE;
          break;
        case WM_LBUTTONUP:
          Win->lButtonMouse = FALSE;
          break;
        case WM_RBUTTONDOWN:
          Win->rButtonMouse = TRUE;
          break;
        case WM_RBUTTONUP:
          Win->rButtonMouse = FALSE;
          break;
        case WM_MOUSEWHEEL:
          Win->OnMouseWheel((SHORT)HIWORD(wParam));
          return 0;
        case WM_ERASEBKGND:
          return 0;
        case WM_TIMER:
          Win->OnTimer((UINT)wParam);
          InvalidateRect(hWnd, NULL, FALSE);
          return 0;
        case WM_PAINT:
          hDC = BeginPaint(hWnd, &ps);
          Win->OnPaint();
          EndPaint(hWnd, &ps);
          return 0;
        case WM_DESTROY:
          Win->OnDestroy();
          PostQuitMessage(0);
          return 0;
        }
        return DefWindowProc(hWnd, msg, wParam, lParam);
      }
    }
    return DefWindowProc(hWnd, msg, wParam, lParam);
  } // End of 'winFunc' function

  // Loop windows processing function
  VOID Run( VOID )
  {
    MSG msg;

    while (TRUE)
    {
      if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))
      {
        if (msg.message == WM_QUIT)
          break;
        TranslateMessage(&msg);
        DispatchMessage(&msg);
      }
      else
        if (IsInit)
          msgRender();
    }
  }

  VOID OnCreate( HWND hWnd )
  {
    SetTimer(hWnd, initTimer, 1, NULL);
  }

  VOID OnResize( int w, int h)
  {
    msgResize(w, h);
  }

  VOID OnTimer( INT Id )
  {
    if (Id == initTimer)
    {
      KillTimer(hWnd, initTimer);
      IsInit = TRUE;
      msgInit(hWnd);
      InvalidateRect(hWnd, NULL, TRUE);
      SetTimer(hWnd, refreshTimer, 1, NULL);
    }
    if (IsInit)
      msgRender();
  }

  VOID OnPaint( VOID )
  {
    if (IsInit)
      msgCopyFrame();
  }

  VOID OnMouseWheel( INT Mz )
  {
    msgMouseWheel(Mz);
  }

  VOID OnDestroy( VOID )
  {
    if (IsInit)
    {
      IsInit = FALSE;
      KillTimer(hWnd, refreshTimer);
      msgDestroy();
    }
    PostQuitMessage(0);
  }

  virtual VOID msgIdle() {}
  virtual VOID msgInit( HWND hWnd ) { }
  virtual VOID msgResize( int w, int h ) { }
  virtual VOID msgRender() { }
  virtual VOID msgCopyFrame() { }
  virtual VOID msgDestroy() { }
  virtual VOID msgMouseWheel( INT Mz ) { }
};
#endif // __win_h_
