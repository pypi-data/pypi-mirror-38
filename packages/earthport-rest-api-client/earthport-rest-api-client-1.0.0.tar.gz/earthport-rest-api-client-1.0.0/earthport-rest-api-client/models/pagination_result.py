# -*- coding: utf-8 -*-


class PaginationResult(object):

    """Implementation of the 'PaginationResult' model.

    This returns a paged set of results rather than the full result set.

    Attributes:
        offset (int): 0-based starting offset of the page with respect to the
            entire resultset.
        page_size (int): Number of items per page to return. If empty the
            maximum allowable (25) number of records will be returned.
        total_number_of_records (int): Total number of records in full result
            set.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "offset":'offset',
        "total_number_of_records":'totalNumberOfRecords',
        "page_size":'pageSize'
    }

    def __init__(self,
                 offset=None,
                 total_number_of_records=None,
                 page_size=None):
        """Constructor for the PaginationResult class"""

        # Initialize members of the class
        self.offset = offset
        self.page_size = page_size
        self.total_number_of_records = total_number_of_records


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        offset = dictionary.get('offset')
        total_number_of_records = dictionary.get('totalNumberOfRecords')
        page_size = dictionary.get('pageSize')

        # Return an object of this model
        return cls(offset,
                   total_number_of_records,
                   page_size)


