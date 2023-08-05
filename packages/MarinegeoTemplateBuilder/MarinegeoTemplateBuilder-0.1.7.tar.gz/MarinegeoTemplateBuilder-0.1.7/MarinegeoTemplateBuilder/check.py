# dry run to create template to check inputs
from MarinegeoTemplateBuilder.classes import Field, Vocab
import logging
import re
from MarinegeoTemplateBuilder.validators import isfloat


def check_vocab(vocabTerms, fieldsList):
    """
    checks all vocab objects in a list to see if they are valid
    :param vocabTerms: list of Vocab() objects
    :param fieldsList: list of Field() objects
    :return:
    """

    for vocab in vocabTerms:

        # vocab destination
        checkerNoneVocab(vocab, "fieldName")
        checkerSymbolsVocab(vocab, "fieldName")
        checkerVocabDestinationExist(vocab, fieldsList) # check that the field actually exists

        # code
        checkerNoneVocab(vocab, "code")
        checkerSymbolsVocab(vocab, "code")

        # definitions
        checkerNoneVocab(vocab, "definition")
        checkerSymbolsVocab(vocab, "definition")

    pass


def check_fields(fieldsList):
    """
    Checks all field objects in a list to see if they are valid
    :param fieldsList: List of Field() object
    :return: nothing - warnings and errors are logged
    """
    for field in fieldsList:

        # check that sheet is defined and doesn't contain bad values
        checkerNone(field, "sheet")
        checkerSymbols(field, "sheet")

        # check that fieldName is defined and doesn't contain bad values
        checkerNone(field, "fieldName")
        checkerSymbols(field, "fieldName")

        # check that field definition is defined
        checkerNone(field, "fieldDefinition")

        # check that fileType is defined and valid
        checkerNone(field, "fieldType")
        checkerAllowedValues(field, "fieldType", ['string', 'date', 'list', 'integer', 'decimal', 'time', 'fkey'])

        # check format string for time date fields?

        # check that the lookup value exists?
        if field.fieldType == 'fkey':
            checkerNone(field, "lookup")
            checkerFkey(field, fieldsList)

        # unit - PASS

        # check that min and max values are numbers
        if field.fieldType in ["integer", "decimal"]:
            checkerNumber(field, 'minValue')
            checkerNumber(field, 'maxValue')

        # check that the given column warnLevel are in the allowed list
        checkerAllowedValues(field, "warnLevel", ['warning', 'stop', 'information'])

    pass


def checkerNone(fieldObj, attribute):
    """
    logs a warning if the field attribute value is none
    :param fieldObj: Field() object to test
    :param attribute: String of the attribute to check
    :return:
    """
    value = getattr(fieldObj, attribute)  # get attribute value
    if value is None:
        logging.warning("{} {} - {} is None.".format(fieldObj.sheet, fieldObj.fieldName, attribute))
    pass


def checkerAllowedValues(fieldObj, attribute, allowedValues):
    """
    logs a warning if the field attribute value is not in the list of allowed values
    :param fieldObj: Field() object to test
    :param attribute: String of the attribute to check
    :param allowedValues: list of allowed values for attribute
    :return:
    """
    value = getattr(fieldObj, attribute)  # get attribute value
    if value not in allowedValues:
        logging.warning(
            "{} {} - {} not valid. Must be in {}.".format(fieldObj.sheet, fieldObj.fieldName, attribute, allowedValues))
    pass


def checkerSymbols(fieldObj, attribute, illegalSymbols='[@_!#$%^&*()<>?/\|}{~:]'):
    """
    logs an error if the attribute value contains an illegal symbol
    :param fieldObj: Field() object to test
    :param attribute: String of the attribute to check
    :param illegalSymbols: String containing all the illegal symbols to check
    :return:
    """
    value = getattr(fieldObj, attribute)  # get attribute value

    # https://www.geeksforgeeks.org/python-program-check-string-contains-special-character/
    regex = re.compile(illegalSymbols)

    if regex.search(str(value)) != None:
        logging.error("{} {} - {} is not valid. {} contains illegal symbols.".format(fieldObj.sheet, fieldObj.fieldName, attribute, value))
    pass


def checkerNumber(fieldObj, attribute):
    """
    logs an error if the attribute value is not a number
    :param fieldObj: Field() object to test
    :param attribute: String of the attribute to check
    :return:
    """
    value = getattr(fieldObj, attribute)  # get attribute value

    if not isfloat(value):
        logging.error("{} {} - {} is not valid. Must be a number.".format(fieldObj.sheet, fieldObj.fieldName, attribute, value))

    pass


def checkerFkey(fieldObj, objList):
    """
    logs an error if the foreign key destination does not exist
    :param fieldObj: Field() object that is a foreign key to test
    :param objList: List of all the Field objects in the workbook
    :return:
    """
    value = getattr(fieldObj, "lookup")  # get attribute value

    # pull out the lookup destination sheet and fieldName
    dest_sheet, dest_field = value.split("$")

    # list comp over objList to find matches
    match = [x for x in objList if (x.sheet == dest_sheet and x.fieldName == dest_field)]

    if len(match) == 0:
        logging.error("{} {} - {} is not valid. {} does not exist.".format(fieldObj.sheet, fieldObj.fieldName, "Foreign Key", value))
    pass


def checkerNoneVocab(vocabObj, attribute):
    """
    logs a warning if the field attribute value is none
    :param vocabObj: vocab() object to test
    :param attribute: String of the attribute to check
    :return:
    """
    value = getattr(vocabObj, attribute)  # get attribute value
    if value is None:
        logging.warning("Vocabulary {} {} is None.".format(vocabObj.fieldName, attribute))
    pass


def checkerSymbolsVocab(vocabObj, attribute, illegalSymbols='[@_!#$%^&*()<>?/\|}{~:]'):
    """
    logs an error if the attribute value contains an illegal symbol
    :param vocabObj: vocab() object to test
    :param attribute: String of the attribute to check
    :param illegalSymbols: String containing all the illegal symbols to check
    :return:
    """
    value = getattr(vocabObj, attribute)  # get attribute value

    # https://www.geeksforgeeks.org/python-program-check-string-contains-special-character/
    regex = re.compile(illegalSymbols)

    if regex.search(str(value)) != None:
        logging.error("Vocabulary {} - {} is not valid. {} contains illegal symbols.".format(vocabObj.fieldName, attribute, value))
    pass


def checkerVocabDestinationExist(vocabObj, fieldList):
    value = getattr(vocabObj, "fieldName")  # get attribute value

    # list comp over fieldList to find matches
    match = [x for x in fieldList if x.fieldName == value]

    if len(match) == 0:
        logging.error(
            "Vocabulary destination missing for fieldName {}.".format(value))
    pass