#include "anim.h"

std::vector<shader> Shaders;

VOID anim::msgRender( VOID )
{
  static DOUBLE oldShdTime = 0;

  input::msgRender(hWnd);
  timer::msgRender(hWnd);

  if (globalTime - oldShdTime > 5)
    Shd.update(), oldShdTime = globalTime;

  if (ClickKeys['T'])
  {
    topMost = topMost ? false : true;
    SendMessage(hWnd, WM_SIZE, NULL, MAKELONG(width, height));
  }

  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  Render();

  glFinish();
}

VOID anim::Render( VOID )
{
  static FLOAT angX = 0, angY = 0, deltX = 0, deltY = 0;

  if (lButtonMouse || Keys[VK_RIGHT] || Keys[VK_LEFT] || Keys[VK_UP] || Keys[VK_DOWN])
    angX += (Mdx + Keys[VK_RIGHT] - Keys[VK_LEFT]) * static_cast<FLOAT>(globalDelteTime) * 30,
    angY += (Mdy + Keys[VK_UP] - Keys[VK_DOWN]) * static_cast<FLOAT>(globalDelteTime) * 30;
  deltX += (Keys['D'] - Keys['A']) * static_cast<FLOAT>(globalDelteTime) * 30;
  deltY += (Keys['W'] - Keys['S']) * static_cast<FLOAT>(globalDelteTime) * 30;

  glUseProgram(Shd.getPrgNo());
  INT loc;

  loc = glGetUniformLocation(Shd.getPrgNo(), "time");
  if (loc != -1)
    glUniform1f(loc, static_cast<GLfloat>(globalTime));
  loc = glGetUniformLocation(Shd.getPrgNo(), "mAngly");
  if (loc != -1)
    glUniform2f(loc, angX, angY);
  loc = glGetUniformLocation(Shd.getPrgNo(), "deltaPos");
  if (loc != -1)
    glUniform2f(loc, deltX, deltY);
  loc = glGetUniformLocation(Shd.getPrgNo(), "mWheel");
  if (loc != -1)
    glUniform1i(loc, Mz);
  loc = glGetUniformLocation(Shd.getPrgNo(), "width");
  if (loc != -1)
    glUniform1i(loc, width);
  loc = glGetUniformLocation(Shd.getPrgNo(), "height");
  if (loc != -1)
    glUniform1i(loc, height);
  loc = glGetUniformLocation(Shd.getPrgNo(), "wP");
  if (loc != -1)
    glUniform1f(loc, Cam.wP);
  loc = glGetUniformLocation(Shd.getPrgNo(), "hP");
  if (loc != -1)
    glUniform1f(loc, Cam.hP);
  loc = glGetUniformLocation(Shd.getPrgNo(), "projDist");
  if (loc != -1)
    glUniform1f(loc, Cam.projDist);
  loc = glGetUniformLocation(Shd.getPrgNo(), "camLoc");
  if (loc != -1)
    glUniform3fv(loc, 1, &Cam.loc.x);
  loc = glGetUniformLocation(Shd.getPrgNo(), "camDir");
  if (loc != -1)
    glUniform3fv(loc, 1, &Cam.dir.x);
  loc = glGetUniformLocation(Shd.getPrgNo(), "camUp");
  if (loc != -1)
    glUniform3fv(loc, 1, &Cam.up.x);
  loc = glGetUniformLocation(Shd.getPrgNo(), "camRight");
  if (loc != -1)
    glUniform3fv(loc, 1, &Cam.right.x);
  loc = glGetUniformLocation(Shd.getPrgNo(), "camAt");
  if (loc != -1)
    glUniform3fv(loc, 1, &Cam.at.x);

  glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

  glUseProgram(0);
}


// Transform text from script language to shader language
std::string shader::loadTxtFragFile( const CHAR *prefix, const CHAR *fileName )
{
  CHAR buf[100]; // Path for file
  
  sprintf(buf, "shaders/%s/%s.glsl", prefix, prefix);

  std::fstream
    f(fileName),                                                                                   // Dummy FRAG shader with all functions
    code(buf);                                                                                     // Script file
  std::string
    realCode = std::string(std::istreambuf_iterator<CHAR>(f), std::istreambuf_iterator<CHAR>()),   // String from dummy frag shader
    psCode = std::string(std::istreambuf_iterator<CHAR>(code), std::istreambuf_iterator<CHAR>());  // String from script file
  int lastCh = 0;                                                                                  // Last prosecced character

  // Seting up enviroment like lights and materials
  auto setUpEnv = [&](std::string envName)
  {
    int
      envR = realCode.find("!(" + envName + ")"),  // Pointer start of material declaration in dummy frag shader
      envPsStr, envPsEns,                          // Pointers to material declaration in script file
      envFind = lastCh,                            // Poiter to finding material declaration
      envCnt = 0;                                  // Conter of writed materials

    realCode.erase(realCode.begin() + envR, realCode.begin() + envR + ("!(" + envName + ")").length());
    while ((envPsStr = psCode.find("#" + envName, envFind)) != -1)
    {
      if (psCode[envPsStr - 1] == '\'')
      {
        lastCh = envFind = psCode.find("\n", envPsStr - 1);
        continue;
      }
      if (envCnt > 0)
        realCode.insert(envR, ",\n"), envR += 2;
      envCnt++;
      envPsStr = psCode.find("{", envFind);
      envPsEns = psCode.find("}", envFind) + 1;
      std::string s(psCode.begin() + envPsStr, psCode.begin() + envPsEns);
      realCode.insert(envR, s);
      envR += s.size();
      envFind = envPsEns + 1;
    }
    lastCh = envFind;

    if (envName == "light")
      if ((envR = realCode.find("!(lightCnt)")) != -1)
      {
        realCode.erase(realCode.begin() + envR, realCode.begin() + envR + std::string("!(lightCnt)").length());
        realCode.insert(envR, std::to_string(envCnt));
      }
  }; // End of 'setUpEnv' lambda function

  // Set up materials
  setUpEnv("material");

  // Set up lights
  setUpEnv("light");

  // Find start of scene in dummy code file
  int sceneR = realCode.find("!(sceneSDF)");
  realCode.erase(realCode.begin() + sceneR, realCode.begin() + sceneR + std::string("!(sceneSDF)").length());

  // Function to convert script function to function in dummy code
  auto findFunc = [&] ()
  {
    int funcPsStr, funcPsEns, mtlNo;
    float k;

    std::string funcStr = "mint = ";

    funcPsStr = psCode.find("#", lastCh);
    funcPsEns = psCode.find("#", funcPsStr + 1);
    std::string func(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns);
    std::string matrFunc, vecPos;


    // Find transforamtion functions
    auto findSubFunc = [&]()
    {
      lastCh = funcPsEns = psCode.find("#", funcPsStr + 1);
      if (std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns).c_str()[0] == 'm')
      {
        funcStr += std::string(psCode.begin() + funcPsStr + 2, psCode.begin() + funcPsEns) + " * tr";
        funcPsStr = funcPsEns;
        lastCh = funcPsEns = psCode.find("#", funcPsEns + 1);
      }
      else
        funcStr += "tr";

      lastCh = funcPsEns = psCode.find("#", funcPsStr + 1);
      if (std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns).c_str()[0] == 'v')
      {
        vecPos = std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns);
        funcStr += "+" + vecPos;
        funcPsStr = funcPsEns;
        lastCh = funcPsEns = psCode.find("#", funcPsEns + 1);
      }
      funcStr += ", ";

      lastCh += sscanf(std::string(psCode.begin() + funcPsEns, psCode.end()).c_str(), "#%i", &mtlNo);
    }; // End of 'findSubFunc' lambda fuction


    if (func == "opU") // Union function
    {
      funcStr += std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns) + "(mint, vec2(fSDF(";
      funcPsStr = funcPsEns;

      findSubFunc();

      funcStr += std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns) + "), " + std::to_string(mtlNo) + "));\n";
    }
    else if (func == "opS" || func == "opI") // Substract and intersection functions
    {
      funcStr += "opU(mint, " + std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns) + "(vec2(fSDF(";
      funcPsStr = funcPsEns;
      findSubFunc();
      funcStr += std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns) + "), " + std::to_string(mtlNo) + "), vec2(fSDF(";

      funcPsStr = lastCh + 1;
      findSubFunc();
      funcStr += std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns) + "), " + std::to_string(mtlNo) + ")));\n";
    }
    else if (func == "opUs") // Smooth union between intesrectioning objects
    {
      funcStr += "opU(mint, " + std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns) + "(vec2(fSDF(";
      funcPsStr = funcPsEns;
      findSubFunc();
      funcStr += std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns) + "), " + std::to_string(mtlNo) + "), vec2(fSDF(";
      funcPsStr = lastCh + 1;

      findSubFunc();
      funcStr += std::string(psCode.begin() + funcPsStr + 1, psCode.begin() + funcPsEns) + "), " + std::to_string(mtlNo) + "), ";
      lastCh++;
      lastCh += sscanf(std::string(psCode.begin() + lastCh, psCode.end()).c_str(), "#k%f", &k);
      funcStr += std::to_string(k) + "));\n";
    }

    return funcStr;
  }; // End of 'findFunc' lambda function

  int
    expresFind = 0,
    exprF[3] = {0};
  std::string
    strFor,
    str;

  // Expression tree build
  while (true)
  {
    exprF[0] = psCode.find("@i", lastCh);
    exprF[1] = psCode.find("#", lastCh);
    exprF[2] = psCode.find("!", lastCh);
    expresFind = exprF[0];

    for (int i = 0; i < 3; i++)
      if (exprF[i] != -1 && (exprF[i] < expresFind || expresFind == -1))
        expresFind = exprF[i];
    if (expresFind == -1)
      break;

    // Find comments that starts with \'
    if (psCode[expresFind - 1] == '\'')
    {
      lastCh = psCode.find("\n", expresFind - 1);
      continue;
    }
    // Defining the expression
    switch (psCode[expresFind])
    {
    case '@':  // 'for' case function with i varible
      int i;
      lastCh = expresFind;
      sscanf(std::string(psCode.begin() + expresFind, psCode.end()).c_str(), "@i%i", &i);
      strFor = "for (int i = 0; i < " + std::to_string(i) + "; i++)\n{\n";

      if ((expresFind = psCode.find("(", expresFind)) == -1)
        throw(std::exception("no '(' for 'for'"));

      /* Functions */
      strFor += findFunc() + "}\n";

      if (psCode[++lastCh] != ')')
        throw(std::exception("no ')' for 'for'"));
      realCode.insert(sceneR, strFor);
      sceneR += strFor.size();
      break;
    case '#':  // Defining a function with #
      if (lastCh == expresFind)
        break;
      lastCh = expresFind - 1;
      str = findFunc();
      realCode.insert(sceneR, str);
      sceneR += str.size();
      break;
    case '!':  // Insert line from script to dummy
      int s, e;
      s = expresFind + 1;
      e = psCode.find("!", expresFind + 1);
      str = std::string(psCode.begin() + s, psCode.begin() + e) + "\n";
      realCode.insert(sceneR, str);
      lastCh = e + 1;
      sceneR += str.size();
      break;
    }
  }

  return realCode;
} // End of 'loadTxtFragFile' function

