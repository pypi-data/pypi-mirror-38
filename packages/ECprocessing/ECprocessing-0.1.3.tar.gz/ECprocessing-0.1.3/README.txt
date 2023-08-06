===========
ECprocessing
===========

ECprocessing will provide a variety of useful functions involved in 
preprocessing. Currently there are only functions for text preprocessing.
 
Typical usage often looks like this::



    from ecprocessing import text_preprocessing as txp


    string_to_process = "This string<br> will be pr3processed to cha__nge '£lots of messy párts."
    processed_string = txp.normalize_text(string_to_process)




