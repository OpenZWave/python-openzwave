#define STRINGIZER(arg)     #arg
#define STR_VALUE(arg)      STRINGIZER(arg)
#define PY_LIB_VERSION_STRING STR_VALUE(PY_LIB_VERSION)
