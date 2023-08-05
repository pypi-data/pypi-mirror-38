# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_bank_account_list_items

class BeneficiaryBankAccountField(object):

    """Implementation of the 'BeneficiaryBankAccountField' model.

    Each beneficiaryBankAccountField would normally be displayed in the UI
    from left to right based on the tabOrder attribute. The
    beneficiaryBankAccountField element contains the following attributes:-
    tabOrder - indicates the ordering of this field in the UIparameterName -
    the name of the corresponding Earthport parameter to use when calling
    addBeneficiaryBankAcountdisplaySize - a suggested field size to
    displaymaxSize - suggested client side syntactic validation
    ruledescription - suggested roll-over or help text description to assist
    usersseparator - the separator to display following (to the right hand
    side) this field, usually '-' or '/' input - whether this field should be
    represented as a text field or a list of optionssubTitle- if present
    contains a sub-label to be displayed with the fieldlocale - the
    localisation setting of this particular recordvalue - the current value of
    this field, populated by the getBeneficiaryBankAccount service.

    Attributes:
        description (string): TODO: type description here.
        display_size (int): TODO: type description here.
        input (BeneficiaryBankAccountFieldInputEnum): Supported input types
            for a bank registration UI.
        locale (string): TODO: type description here.
        max_size (int): TODO: type description here.
        parameter_name (string): TODO: type description here.
        separator (string): TODO: type description here.
        sub_title (string): TODO: type description here.
        tab_order (int): TODO: type description here.
        value (string): TODO: type description here.
        list_items (BeneficiaryBankAccountListItems): The
            beneficiaryBankAccountField contains optional listItem
            sub-elements. The listItem sub-elements would normally be present
            where the inputType attribute is 'list'.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "description":'description',
        "display_size":'displaySize',
        "input":'input',
        "locale":'locale',
        "max_size":'maxSize',
        "parameter_name":'parameterName',
        "separator":'separator',
        "sub_title":'subTitle',
        "tab_order":'tabOrder',
        "value":'value',
        "list_items":'listItems'
    }

    def __init__(self,
                 description=None,
                 display_size=None,
                 input=None,
                 locale=None,
                 max_size=None,
                 parameter_name=None,
                 separator=None,
                 sub_title=None,
                 tab_order=None,
                 value=None,
                 list_items=None):
        """Constructor for the BeneficiaryBankAccountField class"""

        # Initialize members of the class
        self.description = description
        self.display_size = display_size
        self.input = input
        self.locale = locale
        self.max_size = max_size
        self.parameter_name = parameter_name
        self.separator = separator
        self.sub_title = sub_title
        self.tab_order = tab_order
        self.value = value
        self.list_items = list_items


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
        description = dictionary.get('description')
        display_size = dictionary.get('displaySize')
        input = dictionary.get('input')
        locale = dictionary.get('locale')
        max_size = dictionary.get('maxSize')
        parameter_name = dictionary.get('parameterName')
        separator = dictionary.get('separator')
        sub_title = dictionary.get('subTitle')
        tab_order = dictionary.get('tabOrder')
        value = dictionary.get('value')
        list_items = earthport-rest-api-client.models.beneficiary_bank_account_list_items.BeneficiaryBankAccountListItems.from_dictionary(dictionary.get('listItems')) if dictionary.get('listItems') else None

        # Return an object of this model
        return cls(description,
                   display_size,
                   input,
                   locale,
                   max_size,
                   parameter_name,
                   separator,
                   sub_title,
                   tab_order,
                   value,
                   list_items)


