
Darr is a Python science library for storing and sharing numeric data arrays
in a way that is open, simple, and self-explanatory. It also enables fast 
memory-mapped read/write access to such disk-based data, the ability to append 
data, and the flexible use of metadata. It is primarily designed for 
scientific use cases. Save and use your numeric arrays and metadata with one 
line of code while long-term and tool-independent accessibility and easy 
shareability is ensured.

To avoid dependency on specific tools, Darr is based on a combination of
flat binary and human-readable text files. It automatically saves a clear
text description of how the data is stored, together with code for reading
the specific data in a variety of current scientific data tools such as
Python, R, Julia, Matlab and Mathematica (see 
[example array](https://github.com/gbeckers/Darr/tree/master/examplearray.da)).

Darr is currently pre-1.0, still undergoing significant development.

Features
--------

-   **Transparent data format** based on **flat binary** and **text** files.
-   Supports **very large data arrays** through **memory-mapped** file access.
-   Data read/write access through **NumPy indexing**
-   Data is easily **appendable**.
-   **Human-readable explanation of how the binary data is stored** is saved 
    in a README text file.
-   README also contains **examples of how to read the array** in popular 
    analysis environments such as Python (without Darr), R, Julia, 
    Octave/Matlab, GDL/IDL, and Mathematica.
-   **Many numeric types** are supported: (u)int8-(u)int64, float16-float64, 
    complex64, complex128.
-   Easy use of **metadata**, stored in a separate JSON text file.
-   **Minimal dependencies**, only NumPy.
-   **Integrates easily** with the Dask or NumExpr libraries for 
    **numeric computation on very large Darr arrays**.

See the [documentation](http://darr.readthedocs.io/) for more information.



