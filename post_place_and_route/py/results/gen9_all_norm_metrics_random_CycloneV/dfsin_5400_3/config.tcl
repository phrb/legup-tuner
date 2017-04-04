source ../../legup.tcl
source ../config.tcl
set_parameter LOCAL_RAMS 1
set_parameter GROUP_RAMS 1
set_parameter GROUP_RAMS_SIMPLE_OFFSET 1
set_parameter CASE_FSM 1
set_operation_latency altfp_add_32 2
set_operation_latency altfp_divide_16 5
set_resource_constraint unsigned_add_32 6
set_operation_latency mem_dual_port 5
set_resource_constraint altfp_add_8 5
set_operation_latency altfp_truncate_16 0
set_resource_constraint unsigned_modulus_64 8
set_parameter NO_ROMS 1
set_operation_latency signed_modulus_8 5
set_parameter PIPELINE_ALL 0
set_parameter SDC_NO_CHAINING 0
set_resource_constraint signed_multiply_8 3
set_resource_constraint altfp_add_32 1
set_parameter PS_MIN_WIDTH 16
set_operation_latency altfp_subtract_8 7
set_resource_constraint unsigned_modulus_16 4
set_operation_latency signed_multiply_8 1
set_resource_constraint mem_dual_port 2
set_resource_constraint altfp_divide_64 8
set_operation_latency altfp_extend_64 8
set_operation_latency unsigned_multiply_32 8
set_resource_constraint shared_mem_dual_port 7
set_operation_latency local_mem_dual_port 1
set_operation_latency altfp_subtract_64 4
set_resource_constraint signed_divide_32 1
set_resource_constraint signed_multiply_32 2
set_resource_constraint altfp_multiply_64 7
set_operation_latency unsigned_divide_16 0
set_operation_latency signed_multiply_16 5
set_operation_latency signed_divide_16 1
set_operation_latency signed_modulus_32 0
set_operation_latency altfp_divide_8 0
set_operation_latency signed_multiply_32 4
set_operation_latency signed_multiply_64 1
set_parameter PATTERN_SHARE_BITOPS 0
set_operation_latency altfp_add_64 0
set_operation_latency altfp_fptosi 2
set_resource_constraint signed_add_8 1
set_parameter SDC_PRIORITY 1
set_parameter PS_MIN_SIZE 2
set_resource_constraint altfp_multiply_32 8
set_resource_constraint altfp_add_64 4
set_operation_latency altfp_multiply_64 3
set_operation_latency unsigned_add_64 2
set_operation_latency unsigned_multiply_8 0
set_resource_constraint signed_modulus_16 1
set_operation_latency unsigned_add_32 6
set_operation_latency altfp_truncate_8 5
set_resource_constraint signed_multiply_64 1
set_resource_constraint unsigned_modulus_32 5
set_operation_latency signed_divide_64 5
set_resource_constraint altfp_subtract_16 6
set_parameter MB_MINIMIZE_HW 0
set_parameter PATTERN_SHARE_ADD 0
set_operation_latency signed_comp_o 1
set_resource_constraint altfp_subtract_64 6
set_resource_constraint signed_add_16 1
set_parameter PS_MAX_SIZE 15
set_parameter MULTIPLIER_NO_CHAIN 0
set_operation_latency signed_comp_u 1
set_parameter DUAL_PORT_BINDING 0
set_resource_constraint unsigned_divide_32 6
set_operation_latency unsigned_modulus_64 0
set_operation_latency altfp_multiply_8 5
set_operation_latency altfp_multiply_32 4
set_operation_latency signed_add_8 0
set_operation_latency altfp_add_16 4
set_operation_latency altfp_truncate_32 0
set_resource_constraint unsigned_divide_64 4
set_resource_constraint signed_divide_8 2
set_operation_latency altfp_subtract_16 7
set_resource_constraint signed_modulus_64 2
set_operation_latency altfp_extend_32 6
set_resource_constraint unsigned_add_8 7
set_operation_latency signed_add_16 5
set_operation_latency reg 6
set_resource_constraint altfp_add_16 1
set_parameter PS_BIT_DIFF_THRESHOLD 11
set_operation_latency altfp_add_8 0
set_resource_constraint altfp_divide_8 6
set_operation_latency altfp_sitofp 8
set_resource_constraint unsigned_add_64 3
set_resource_constraint signed_add_64 6
set_resource_constraint signed_modulus_32 3
set_operation_latency signed_divide_32 0
set_parameter MODULO_SCHEDULER SDC_BACKTRACKING
set_operation_latency unsigned_divide_64 8
set_resource_constraint unsigned_add_16 5
set_parameter DONT_CHAIN_GET_ELEM_PTR 1
set_resource_constraint signed_divide_16 8
set_parameter EXPLICIT_LPM_MULTS 0
set_operation_latency unsigned_modulus_8 0
set_parameter MB_MAX_BACK_PASSES 20587
set_operation_latency signed_modulus_16 1
set_parameter SDC_MULTIPUMP 0
set_resource_constraint signed_multiply_16 1
set_operation_latency altfp_multiply_16 2
set_operation_latency unsigned_multiply_16 3
set_operation_latency altfp_extend_8 0
set_operation_latency unsigned_divide_32 2
set_operation_latency altfp_divide_32 0
set_parameter PATTERN_SHARE_SHIFT 0
set_resource_constraint unsigned_multiply_8 1
set_resource_constraint unsigned_divide_16 7
set_operation_latency unsigned_add_16 6
set_parameter PATTERN_SHARE_SUB 0
set_parameter CLOCK_PERIOD 28
set_resource_constraint signed_modulus_8 2
set_resource_constraint altfp_subtract_8 5
set_resource_constraint unsigned_multiply_32 5
set_operation_latency altfp_subtract_32 6
set_parameter NO_LOOP_PIPELINING 1
set_operation_latency unsigned_divide_8 1
set_resource_constraint altfp_multiply_16 8
set_operation_latency altfp_divide_64 2
set_resource_constraint altfp_divide_32 2
set_parameter INCREMENTAL_SDC 0
set_operation_latency signed_divide_8 2
set_operation_latency altfp_truncate_64 8
set_resource_constraint altfp_multiply_8 3
set_resource_constraint unsigned_multiply_16 4
set_operation_latency signed_modulus_64 8
set_operation_latency unsigned_modulus_32 0
set_operation_latency unsigned_multiply_64 1
set_operation_latency unsigned_modulus_16 0
set_resource_constraint altfp_divide_16 8
set_resource_constraint unsigned_multiply_64 5
set_operation_latency signed_add_32 7
set_operation_latency unsigned_add_8 0
set_operation_latency altfp_extend_16 1
set_parameter DISABLE_REG_SHARING 0
set_operation_latency signed_add_64 5
set_resource_constraint altfp_subtract_32 1
set_resource_constraint unsigned_modulus_8 1
set_combine_basicblock 0
set_parameter ENABLE_PATTERN_SHARING 1
set_resource_constraint unsigned_divide_8 3
set_parameter PIPELINE_RESOURCE_SHARING 1
set_resource_constraint signed_divide_64 2
set_parameter MULTIPUMPING 1
set_resource_constraint signed_add_32 2
