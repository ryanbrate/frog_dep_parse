"""
The output from the KB_sampling/sample.py script is as follows:

# list of tuples
[
    # e.g., typing tuples of (ocr_name, ocr as a dict)
    [
        ocr_name,
        {
            "text": {
                "title": # str
                "p": # list[str] or str or None?
            }
        }
    ],
    ...
]

convert to each (ocr_name, ocr as a dict) tuple into ...
[
    label,
    # list of strings
],

"""

def convert(t)->tuple:
    """ Return (ocr_name::str, list_of_strings::list[str]) from an ocr sample
        produced by KB_sampling.

        Args:
            t: (ocr_name::str, ocr::dict)
    """

    ocr_name, ocr = t

    # get the list_of_strings
    if type(ocr["text"]["p"]) == str:
        list_of_strings = [ocr["text"]["p"]]
    elif type(ocr["text"]["p"]) == list: 
        list_of_strings = ocr["text"]["p"]
    else:
        list_of_strings = []

    return (ocr_name, list_of_strings)


       




    

