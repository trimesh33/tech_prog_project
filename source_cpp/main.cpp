#include "anim.h"

/* Main function. */
INT WINAPI WinMain( HINSTANCE hInst, HINSTANCE hPrevInst, CHAR *cmdLine, INT showCmd )
{
  anim Anim(hInst);

  Anim.Run();
  return 0x21;
} /* End of 'WinMain' fucniton */

// END OF 'main.cpp' FILE
