################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../BinomialHeap.cpp \
../Edge.cpp \
../FindUnionSet.cpp \
../TarjanAlgorithm.cpp \
../TreeNode.cpp \
../main.cpp 

OBJS += \
./BinomialHeap.o \
./Edge.o \
./FindUnionSet.o \
./TarjanAlgorithm.o \
./TreeNode.o \
./main.o 

CPP_DEPS += \
./BinomialHeap.d \
./Edge.d \
./FindUnionSet.d \
./TarjanAlgorithm.d \
./TreeNode.d \
./main.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: Cygwin C++ Compiler'
	g++ -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


