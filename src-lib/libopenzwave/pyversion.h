#define STRINGIZER(arg)     #arg
#define STR_VALUE(arg)      STRINGIZER(arg)
#ifdef PY_LIB_VERSION
#define PY_LIB_VERSION_STRING STR_VALUE(PY_LIB_VERSION)
#endif
#ifndef PY_LIB_VERSION
#define PY_LIB_VERSION_STRING STR_VALUE("Undef")
#endif
