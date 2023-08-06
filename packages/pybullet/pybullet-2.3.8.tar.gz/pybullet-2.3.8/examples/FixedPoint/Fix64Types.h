#ifndef FIX64TYPES_H
#define FIX64TYPES_H

#ifdef __GNUC__
        #include <stdint.h>
        typedef int32_t smInt32_t;
        typedef int64_t smInt64_t;
        typedef uint32_t smUint32_t;
        typedef uint64_t smUint64_t;
#elif defined(_MSC_VER)
        typedef __int32 smInt32_t;
        typedef __int64 smInt64_t;
        typedef unsigned __int32 smUint32_t;
        typedef unsigned __int64 smUint64_t;
#else
        typedef int smInt32_t;
        typedef long long int smInt64_t;
        typedef unsigned int smUint32_t;
        typedef unsigned long long int smUint64_t;
#endif


#endif

