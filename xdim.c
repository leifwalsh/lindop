#!/usr/bin/tcc -run -lX11 -lXxf86vm

   /* -*- c -*-
      Change brightness of default display's default screen.
      Requires the libxxf86vm-dev package.

      Based on code by Trent W. Buck.
    */

#include <stdlib.h>
#include <assert.h>
#include <X11/Xlib.h>
#include <X11/extensions/xf86vmode.h>

#define MAX 256

int main(int argc, char **argv) {
   Display *dpy;
   int screen, len, i;
   float mult = -1;
   unsigned short rgb[MAX];

   assert(argc == 2);
   mult = atof(argv[1]);
   assert(mult > 0.1 && mult <= 1);
   dpy = XOpenDisplay(NULL);
   assert(dpy);
   screen = DefaultScreen(dpy);
   XF86VidModeGetGammaRampSize(dpy, screen, &len);
   assert(len <= MAX);

   for (i = 0; i < len; i++)
      rgb[i] = mult * i * 65535 / (len-1);

   XF86VidModeSetGammaRamp(dpy, screen, len, rgb, rgb, rgb);
   XCloseDisplay(dpy);
   return 0;
}
