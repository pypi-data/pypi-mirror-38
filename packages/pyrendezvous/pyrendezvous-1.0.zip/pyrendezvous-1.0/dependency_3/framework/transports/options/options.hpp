#pragma once

#include <cstddef>


namespace framework {
    
/**
 * @brief Provides base transport options.
 */    
struct options
{
    /**
     * @brief The maximum socket read size.
     * 
     * @details
     * This setting is used to allocate an internal buffer within a transport 
     * into which data will be received from the underlying socket. The buffer is 
     * exposed to the client in data reception socket.
     */
    size_t read_buffer_size {2048};
    
    /**
     * @brief The send buffer size.
     * 
     * @details
     * Size of internal ring buffer used by transport to store send requests for 
     * on dispatch sends. Due to the implementation size of the actual buffer 
     * allocated by the transport will be rounded to the closest multiplication of 
     * memory page size.
     */
    size_t send_buffer_size {4096}; 
    
    /**
     * @brief The maximum socket receive buffer in bytes.
     * 
     * @details
     * The kernel doubles this value (to allow space for bookkeeping
     * overhead) when it is set using setsockopt(2), and this doubled
     * value is returned by getsockopt(2).  The default value is set
     * by the /proc/sys/net/core/rmem_default file, and the maximum
     * allowed value is set by the /proc/sys/net/core/rmem_max file.
     * The minimum (doubled) value for this option is 256.
     */
    size_t sp_rcvbuf {1500};
    
    /**
     * @brief The maximum socket send buffer in bytes.
     * 
     * @details
     * The kernel doubles this value (to allow space for bookkeeping
     * overhead) when it is set using setsockopt(2), and this doubled
     * value is returned by getsockopt(2).  The default value is set
     * by the /proc/sys/net/core/rmem_default file, and the maximum
     * allowed value is set by the /proc/sys/net/core/rmem_max file.
     * The minimum (doubled) value for this option is 256.
     */
    size_t sp_sndbuf {1500};
};
    
}


