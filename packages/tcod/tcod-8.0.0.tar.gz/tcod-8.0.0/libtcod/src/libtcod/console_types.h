/* libtcod
 * Copyright © 2008-2018 Jice and the libtcod contributers.
 * All rights reserved.
 *
 * libtcod 'The Doryen library' is a cross-platform C/C++ library for roguelike
 * developers.
 * Its source code is available from:
 * https://github.com/libtcod/libtcod
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * The name of copyright holder nor the names of its contributors may not
 *       be used to endorse or promote products derived from this software
 *       without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 * TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 * ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
#ifndef _TCOD_CONSOLE_TYPES_H
#define _TCOD_CONSOLE_TYPES_H

#include "portability.h"
#include "color.h"

typedef enum {
	TCODK_NONE,
	TCODK_ESCAPE,
	TCODK_BACKSPACE,
	TCODK_TAB,
	TCODK_ENTER,
	TCODK_SHIFT,
	TCODK_CONTROL,
	TCODK_ALT,
	TCODK_PAUSE,
	TCODK_CAPSLOCK,
	TCODK_PAGEUP,
	TCODK_PAGEDOWN,
	TCODK_END,
	TCODK_HOME,
	TCODK_UP,
	TCODK_LEFT,
	TCODK_RIGHT,
	TCODK_DOWN,
	TCODK_PRINTSCREEN,
	TCODK_INSERT,
	TCODK_DELETE,
	TCODK_LWIN,
	TCODK_RWIN,
	TCODK_APPS,
	TCODK_0,
	TCODK_1,
	TCODK_2,
	TCODK_3,
	TCODK_4,
	TCODK_5,
	TCODK_6,
	TCODK_7,
	TCODK_8,
	TCODK_9,
	TCODK_KP0,
	TCODK_KP1,
	TCODK_KP2,
	TCODK_KP3,
	TCODK_KP4,
	TCODK_KP5,
	TCODK_KP6,
	TCODK_KP7,
	TCODK_KP8,
	TCODK_KP9,
	TCODK_KPADD,
	TCODK_KPSUB,
	TCODK_KPDIV,
	TCODK_KPMUL,
	TCODK_KPDEC,
	TCODK_KPENTER,
	TCODK_F1,
	TCODK_F2,
	TCODK_F3,
	TCODK_F4,
	TCODK_F5,
	TCODK_F6,
	TCODK_F7,
	TCODK_F8,
	TCODK_F9,
	TCODK_F10,
	TCODK_F11,
	TCODK_F12,
	TCODK_NUMLOCK,
	TCODK_SCROLLLOCK,
	TCODK_SPACE,
	TCODK_CHAR,
	TCODK_TEXT
} TCOD_keycode_t;

#define TCOD_KEY_TEXT_SIZE 32

/* key data : special code or character or text */
typedef struct {
	TCOD_keycode_t vk; /*  key code */
	char c; /* character if vk == TCODK_CHAR else 0 */
	char text[TCOD_KEY_TEXT_SIZE]; /* text if vk == TCODK_TEXT else text[0] == '\0' */
	bool pressed ; /* does this correspond to a key press or key release event ? */
	bool lalt ;
	bool lctrl ;
	bool lmeta ;
	bool ralt ;
	bool rctrl ;
	bool rmeta ;
	bool shift ;
} TCOD_key_t;

typedef enum {
	/* single walls */
	TCOD_CHAR_HLINE=196,
	TCOD_CHAR_VLINE=179,
	TCOD_CHAR_NE=191,
	TCOD_CHAR_NW=218,
	TCOD_CHAR_SE=217,
	TCOD_CHAR_SW=192,
	TCOD_CHAR_TEEW=180,
	TCOD_CHAR_TEEE=195,
	TCOD_CHAR_TEEN=193,
	TCOD_CHAR_TEES=194,
	TCOD_CHAR_CROSS=197,
	/* double walls */
	TCOD_CHAR_DHLINE=205,
	TCOD_CHAR_DVLINE=186,
	TCOD_CHAR_DNE=187,
	TCOD_CHAR_DNW=201,
	TCOD_CHAR_DSE=188,
	TCOD_CHAR_DSW=200,
	TCOD_CHAR_DTEEW=185,
	TCOD_CHAR_DTEEE=204,
	TCOD_CHAR_DTEEN=202,
	TCOD_CHAR_DTEES=203,
	TCOD_CHAR_DCROSS=206,
	/* blocks */
	TCOD_CHAR_BLOCK1=176,
	TCOD_CHAR_BLOCK2=177,
	TCOD_CHAR_BLOCK3=178,
	/* arrows */
	TCOD_CHAR_ARROW_N=24,
	TCOD_CHAR_ARROW_S=25,
	TCOD_CHAR_ARROW_E=26,
	TCOD_CHAR_ARROW_W=27,
	/* arrows without tail */
	TCOD_CHAR_ARROW2_N=30,
	TCOD_CHAR_ARROW2_S=31,
	TCOD_CHAR_ARROW2_E=16,
	TCOD_CHAR_ARROW2_W=17,
	/* double arrows */
	TCOD_CHAR_DARROW_H=29,
	TCOD_CHAR_DARROW_V=18,
	/* GUI stuff */
	TCOD_CHAR_CHECKBOX_UNSET=224,
	TCOD_CHAR_CHECKBOX_SET=225,
	TCOD_CHAR_RADIO_UNSET=9,
	TCOD_CHAR_RADIO_SET=10,
	/* sub-pixel resolution kit */
	TCOD_CHAR_SUBP_NW=226,
	TCOD_CHAR_SUBP_NE=227,
	TCOD_CHAR_SUBP_N=228,
	TCOD_CHAR_SUBP_SE=229,
	TCOD_CHAR_SUBP_DIAG=230,
	TCOD_CHAR_SUBP_E=231,
	TCOD_CHAR_SUBP_SW=232,
	/* miscellaneous */
	TCOD_CHAR_SMILIE = 1,
	TCOD_CHAR_SMILIE_INV = 2,
	TCOD_CHAR_HEART = 3,
	TCOD_CHAR_DIAMOND = 4,
	TCOD_CHAR_CLUB = 5,
	TCOD_CHAR_SPADE = 6,
	TCOD_CHAR_BULLET = 7,
	TCOD_CHAR_BULLET_INV = 8,
	TCOD_CHAR_MALE = 11,
	TCOD_CHAR_FEMALE = 12,
	TCOD_CHAR_NOTE = 13,
	TCOD_CHAR_NOTE_DOUBLE = 14,
	TCOD_CHAR_LIGHT = 15,
	TCOD_CHAR_EXCLAM_DOUBLE = 19,
	TCOD_CHAR_PILCROW = 20,
	TCOD_CHAR_SECTION = 21,
	TCOD_CHAR_POUND = 156,
	TCOD_CHAR_MULTIPLICATION = 158,
	TCOD_CHAR_FUNCTION = 159,
	TCOD_CHAR_RESERVED = 169,
	TCOD_CHAR_HALF = 171,
	TCOD_CHAR_ONE_QUARTER = 172,
	TCOD_CHAR_COPYRIGHT = 184,
	TCOD_CHAR_CENT = 189,
	TCOD_CHAR_YEN = 190,
	TCOD_CHAR_CURRENCY = 207,
	TCOD_CHAR_THREE_QUARTERS = 243,
	TCOD_CHAR_DIVISION = 246,
	TCOD_CHAR_GRADE = 248,
	TCOD_CHAR_UMLAUT = 249,
	TCOD_CHAR_POW1 = 251,
	TCOD_CHAR_POW3 = 252,
	TCOD_CHAR_POW2 = 253,
	TCOD_CHAR_BULLET_SQUARE = 254,
	/* diacritics */
} TCOD_chars_t;

typedef enum {
	TCOD_COLCTRL_1 = 1,
	TCOD_COLCTRL_2,
	TCOD_COLCTRL_3,
	TCOD_COLCTRL_4,
	TCOD_COLCTRL_5,
	TCOD_COLCTRL_NUMBER=5,
	TCOD_COLCTRL_FORE_RGB,
	TCOD_COLCTRL_BACK_RGB,
	TCOD_COLCTRL_STOP
} TCOD_colctrl_t;

typedef enum {
	TCOD_BKGND_NONE,
	TCOD_BKGND_SET,
	TCOD_BKGND_MULTIPLY,
	TCOD_BKGND_LIGHTEN,
	TCOD_BKGND_DARKEN,
	TCOD_BKGND_SCREEN,
	TCOD_BKGND_COLOR_DODGE,
	TCOD_BKGND_COLOR_BURN,
	TCOD_BKGND_ADD,
	TCOD_BKGND_ADDA,
	TCOD_BKGND_BURN,
	TCOD_BKGND_OVERLAY,
	TCOD_BKGND_ALPH,
	TCOD_BKGND_DEFAULT
} TCOD_bkgnd_flag_t;

typedef enum {
	TCOD_KEY_PRESSED=1,
	TCOD_KEY_RELEASED=2,
} TCOD_key_status_t;

/**
 *  These font flags can be OR'd together into a bit-field and passed to
 *  TCOD_console_set_custom_font
 */
typedef enum {
  /** Tiles are arranged in column-major order.
   *
   *       0 3 6
   *       1 4 7
   *       2 5 8
   */
  TCOD_FONT_LAYOUT_ASCII_INCOL=1,
  /** Tiles are arranged in row-major order.
   *
   *       0 1 2
   *       3 4 5
   *       6 7 8
   */
  TCOD_FONT_LAYOUT_ASCII_INROW=2,
  /** Converts all tiles into a monochrome gradient. */
  TCOD_FONT_TYPE_GREYSCALE=4,
  TCOD_FONT_TYPE_GRAYSCALE=4,
  /** A unique layout used by some of libtcod's fonts. */
  TCOD_FONT_LAYOUT_TCOD=8,
} TCOD_font_flags_t;
/**
 *  The available renderers.
 */
typedef enum {
  /** An OpenGL implementation using a shader. */
  TCOD_RENDERER_GLSL,
  /**
   *  An OpenGL implementation without a shader.
   *
   *  Performs worse than TCOD_RENDERER_GLSL without many benefits.
   */
  TCOD_RENDERER_OPENGL,
  /**
   *  A software based renderer.
   *
   *  The font file is loaded into RAM instead of VRAM in this implementation.
   */
  TCOD_RENDERER_SDL,
  /**
   *  A new SDL2 renderer.  Allows the window to be resized.
   *  \rst
   *  .. versionadded:: 1.8
   *  \endrst
   */
  TCOD_RENDERER_SDL2,
  /**
   *  A new OpenGL 2.1 renderer.  Allows the window to be resized.
   *  \rst
   *  .. versionadded:: 1.9
   *  \endrst
   */
  TCOD_RENDERER_OPENGL2,
  TCOD_NB_RENDERERS,
} TCOD_renderer_t;

/**
 *  \enum TCOD_alignment_t
 *
 *  Print justification options.
 */
typedef enum {
	TCOD_LEFT,
	TCOD_RIGHT,
	TCOD_CENTER
} TCOD_alignment_t;

/** Private console struct. */
typedef struct TCOD_Console {
  /** Character code array. */
  int *ch_array;
  /** Pointers to arrays of TCOD_color_t colors. */
  TCOD_color_t *fg_array, *bg_array;
  /** Console width and height (in characters, not pixels.) */
  int w,h;
  /** Default background operator for print & print_rect functions. */
  TCOD_bkgnd_flag_t bkgnd_flag;
  /** Default alignment for print & print_rect functions. */
  TCOD_alignment_t alignment;
  /** Foreground (text) and background colors. */
  TCOD_color_t fore, back;
  /** True if a key color is being used. */
  bool has_key_color;
  /** The current key color for this console. */
  TCOD_color_t key_color;
} TCOD_Console;
typedef TCOD_Console *TCOD_console_t;
#endif /* _TCOD_CONSOLE_TYPES_H */
