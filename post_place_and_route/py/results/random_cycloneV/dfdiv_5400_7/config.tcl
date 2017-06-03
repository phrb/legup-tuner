source ../../legup.tcl
source ../config.tcl
set_parameter LOCAL_RAMS 1
set_parameter GROUP_RAMS 1
set_parameter GROUP_RAMS_SIMPLE_OFFSET 1
set_parameter CASE_FSM 1
set_operation_latency altfp_add_32 3
set_operation_latency altfp_divide_16 6
set_resource_constraint unsigned_add_32 5
set_operation_latency mem_dual_port 5
set_resource_constraint altfp_add_8 3
set_operation_latency altfp_truncate_16 5
set_resource_constraint unsigned_modulus_64 6
set_parameter NO_ROMS 0
set_operation_latency signed_modulus_8 3
set_parameter PIPELINE_ALL 1
set_parameter SDC_NO_CHAINING 0
set_resource_constraint signed_multiply_8 3
set_resource_constraint altfp_add_32 2
set_parameter PS_MIN_WIDTH 7
set_operation_latency altfp_subtract_8 8
set_resource_constraint unsigned_modulus_16 4
set_operation_latency signed_multiply_8 7
set_resource_constraint mem_dual_port 8
set_resource_constraint altfp_divide_64 5
set_operation_latency altfp_extend_64 6
set_operation_latency unsigned_multiply_32 1
set_resource_constraint shared_mem_dual_port 5
set_operation_latency local_mem_dual_port 3
set_operation_latency altfp_subtract_64 6
set_resource_constraint signed_divide_32 5
set_resource_constraint signed_multiply_32 6
set_resource_constraint altfp_multiply_64 1
set_operation_latency unsigned_divide_16 7
set_operation_latency signed_multiply_16 4
set_operation_latency signed_divide_16 5
set_operation_latency signed_modulus_32 0
set_operation_latency altfp_divide_8 2
set_operation_latency signed_multiply_32 6
set_operation_latency signed_multiply_64 4
set_parameter PATTERN_SHARE_BITOPS 1
set_operation_latency altfp_add_64 5
set_operation_latency altfp_fptosi 4
set_resource_constraint signed_add_8 2
set_parameter SDC_PRIORITY 0
set_parameter PS_MIN_SIZE 9
set_resource_constraint altfp_multiply_32 8
set_resource_constraint altfp_add_64 5
set_operation_latency altfp_multiply_64 2
set_operation_latency unsigned_add_64 2
set_operation_latency unsigned_multiply_8 0
set_resource_constraint signed_modulus_16 6
set_operation_latency unsigned_add_32 1
set_operation_latency altfp_truncate_8 0
set_resource_constraint signed_multiply_64 2
set_resource_constraint unsigned_modulus_32 8
set_operation_latency signed_divide_64 3
set_resource_constraint altfp_subtract_16 1
set_parameter MB_MINIMIZE_HW 0
set_parameter PATTERN_SHARE_ADD 1
set_operation_latency signed_comp_o 1
set_resource_constraint altfp_subtract_64 2
set_resource_constraint signed_add_16 7
set_parameter PS_MAX_SIZE 3
set_parameter MULTIPLIER_NO_CHAIN 1
set_operation_latency signed_comp_u 5
set_parameter DUAL_PORT_BINDING 0
set_resource_constraint unsigned_divide_32 3
set_operation_latency unsigned_modulus_64 6
set_operation_latency altfp_multiply_8 8
set_operation_latency altfp_multiply_32 7
set_operation_latency signed_add_8 8
set_operation_latency altfp_add_16 8
set_operation_latency altfp_truncate_32 7
set_resource_constraint unsigned_divide_64 2
set_resource_constraint signed_divide_8 6
set_operation_latency altfp_subtract_16 1
set_resource_constraint signed_modulus_64 6
set_operation_latency altfp_extend_32 6
set_resource_constraint unsigned_add_8 5
set_operation_latency signed_add_16 7
set_operation_latency reg 5
set_resource_constraint altfp_add_16 1
set_parameter PS_BIT_DIFF_THRESHOLD 6
set_operation_latency altfp_add_8 6
set_resource_constraint altfp_divide_8 1
set_operation_latency altfp_sitofp 8
set_resource_constraint unsigned_add_64 4
set_resource_constraint signed_add_64 1
set_resource_constraint signed_modulus_32 7
set_operation_latency signed_divide_32 2
set_parameter MODULO_SCHEDULER SDC_BACKTRACKING
set_operation_latency unsigned_divide_64 5
set_resource_constraint unsigned_add_16 2
set_parameter DONT_CHAIN_GET_ELEM_PTR 0
set_resource_constraint signed_divide_16 1
set_parameter EXPLICIT_LPM_MULTS 1
set_operation_latency unsigned_modulus_8 7
set_parameter MB_MAX_BACK_PASSES 6056
set_operation_latency signed_modulus_16 8
set_parameter SDC_MULTIPUMP 1
set_resource_constraint signed_multiply_16 6
set_operation_latency altfp_multiply_16 6
set_operation_latency unsigned_multiply_16 6
set_operation_latency altfp_extend_8 4
set_operation_latency unsigned_divide_32 1
set_operation_latency altfp_divide_32 6
set_parameter PATTERN_SHARE_SHIFT 1
set_resource_constraint unsigned_multiply_8 2
set_resource_constraint unsigned_divide_16 6
set_operation_latency unsigned_add_16 4
set_parameter PATTERN_SHARE_SUB 1
set_parameter CLOCK_PERIOD 29
set_resource_constraint signed_modulus_8 4
set_resource_constraint altfp_subtract_8 7
set_resource_constraint unsigned_multiply_32 1
set_operation_latency altfp_subtract_32 5
set_parameter NO_LOOP_PIPELINING 1
set_operation_latency unsigned_divide_8 1
set_resource_constraint altfp_multiply_16 6
set_operation_latency altfp_divide_64 5
set_resource_constraint altfp_divide_32 8
set_parameter INCREMENTAL_SDC 1
set_operation_latency signed_divide_8 0
set_operation_latency altfp_truncate_64 7
set_resource_constraint altfp_multiply_8 8
set_resource_constraint unsigned_multiply_16 4
set_operation_latency signed_modulus_64 0
set_operation_latency unsigned_modulus_32 5
set_operation_latency unsigned_multiply_64 2
set_operation_latency unsigned_modulus_16 0
set_resource_constraint altfp_divide_16 2
set_resource_constraint unsigned_multiply_64 6
set_operation_latency signed_add_32 1
set_operation_latency unsigned_add_8 8
set_operation_latency altfp_extend_16 0
set_parameter DISABLE_REG_SHARING 1
set_operation_latency signed_add_64 4
set_resource_constraint altfp_subtract_32 1
set_resource_constraint unsigned_modulus_8 4
set_combine_basicblock 2
set_parameter ENABLE_PATTERN_SHARING 1
set_resource_constraint unsigned_divide_8 1
set_parameter PIPELINE_RESOURCE_SHARING 1
set_resource_constraint signed_divide_64 6
set_parameter MULTIPUMPING 0
set_resource_constraint signed_add_32 6
