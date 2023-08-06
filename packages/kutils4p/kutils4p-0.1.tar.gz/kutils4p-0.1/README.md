# kutils4p

Simple everyday utils and data structs written in vanilla python3.

# Includes

## File Utils
* generate_files_of_type
* is_non_zero_file
## KDecorator

* Generic decorator class which calls "before" method before decorated function and "after" method on output decorated output. Flow can be interrupted by raising a KException to prevent "after" call.

## Data Structs
* RingBuffer
    * python list wrapper which, when iterated, loops back to index 0 of contents
* SpiralBuffer
    * python list wrapper which, when iterated, proceeds forwards and then backwards through contents

# Install

pip3 install kutils4p --user 
