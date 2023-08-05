# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_identity_list_items

class BeneficiaryIdentityField(object):

    """Implementation of the 'BeneficiaryIdentityField' model.

    Each BeneficiaryIdentityField would normally be displayed in the UI from
    left to right based on the tabOrder attribute. The
    BeneficiaryIdentityField element contains the following attributes:
    tabOrder: indicates the ordering of this field in the UIparameterName: the
    name of the corresponding Earthport parameter to use when calling
    addBeneficiaryBankAcountdisplaySize: a suggested field size to
    displaymaxSize: suggested client side syntactic validation
    ruledescription: suggested roll-over or help text description to assist
    usersseparator: the separator to display following (to the right hand
    side) this field, usually '-' or '/'input: whether this field should be
    represented as a text field or a list of optionssubTitle: if present
    contains a sub-label to be displayed with the fieldlocale: the
    localisation setting of this particular recordelementName: the name of the
    element in the addBeneficiaryBankAccount request document for the
    corresponding fieldmandatory: indicates whether the field is
    mandatoryvalueRegexp: the regexp for the value of this field

    Attributes:
        description (string): TODO: type description here.
        display_size (int): TODO: type description here.
        element_name (string): TODO: type description here.
        input (BeneficiaryIdentityFieldInputEnum): Supported input types for a
            beneficiary identity UI.
        locale (string): TODO: type description here.
        mandatory (string): TODO: type description here.
        max_size (int): TODO: type description here.
        parameter_name (string): TODO: type description here.
        separator (string): TODO: type description here.
        sub_title (string): TODO: type description here.
        tab_order (int): TODO: type description here.
        value_regexp (string): TODO: type description here.
        list_items (BeneficiaryIdentityListItems): The
            beneficiaryIdentityField contains optional listItem sub-elements.
            The listItem sub-elements would normally be present where the
            inputType attribute is 'list'.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "description":'description',
        "display_size":'displaySize',
        "element_name":'elementName',
        "input":'input',
        "locale":'locale',
        "mandatory":'mandatory',
        "max_size":'maxSize',
        "sub_title":'subTitle',
        "tab_order":'tabOrder',
        "parameter_name":'parameterName',
        "separator":'separator',
        "value_regexp":'valueRegexp',
        "list_items":'listItems'
    }

    def __init__(self,
                 description=None,
                 display_size=None,
                 element_name=None,
                 input=None,
                 locale=None,
                 mandatory=None,
                 max_size=None,
                 sub_title=None,
                 tab_order=None,
                 parameter_name=None,
                 separator=None,
                 value_regexp=None,
                 list_items=None):
        """Constructor for the BeneficiaryIdentityField class"""

        # Initialize members of the class
        self.description = description
        self.display_size = display_size
        self.element_name = element_name
        self.input = input
        self.locale = locale
        self.mandatory = mandatory
        self.max_size = max_size
        self.parameter_name = parameter_name
        self.separator = separator
        self.sub_title = sub_title
        self.tab_order = tab_order
        self.value_regexp = value_regexp
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
        element_name = dictionary.get('elementName')
        input = dictionary.get('input')
        locale = dictionary.get('locale')
        mandatory = dictionary.get('mandatory')
        max_size = dictionary.get('maxSize')
        sub_title = dictionary.get('subTitle')
        tab_order = dictionary.get('tabOrder')
        parameter_name = dictionary.get('parameterName')
        separator = dictionary.get('separator')
        value_regexp = dictionary.get('valueRegexp')
        list_items = earthport-rest-api-client.models.beneficiary_identity_list_items.BeneficiaryIdentityListItems.from_dictionary(dictionary.get('listItems')) if dictionary.get('listItems') else None

        # Return an object of this model
        return cls(description,
                   display_size,
                   element_name,
                   input,
                   locale,
                   mandatory,
                   max_size,
                   sub_title,
                   tab_order,
                   parameter_name,
                   separator,
                   value_regexp,
                   list_items)


