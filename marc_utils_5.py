# -*- coding: utf-8 -*- 

import pymarc
from typing import List
import re

# ------------------------------ Sort ------------------------------

def sort_fields_by_tag(record:pymarc.record.Record):
    """Sort the record fields by their tag"""
    record.fields = sorted(record.fields, key=lambda field: field.tag)

def __sort_subfields(curr_subf:List[pymarc.field.Subfield], sort:List[str]) -> List[str]:
    """Sort a list of subfields and returns the new list :
    * If a subfield code is not in sort, its position will stay the same
    * If a subfield is in sort, it will be moved to that order
    * To sort at the end, use "*" as a code to separate values to use to sort at the beginning
    from values to use to sort at the end

    Takes as argument :
        - curr_subf : subfields as given by pymarc.field.Field.subfields [code1, content1, code2, content2, etc.]
        - sort : a list of subfield codes (str)"""

    # Stores every existing subfield
    new_subf = []
    # get positive & negative sort
    positive_sort = []
    negative_sort = []
    if not "*" in sort:
        positive_sort = sort
    else:
        positive_sort = sort[:sort.index("*")]
        negative_sort = sort[sort.index("*")+1:len(sort)]
    
    # Positive sort
    for code in positive_sort:
        for subf in curr_subf:
            if subf.code == code:
                new_subf.append(subf)

    # Default sort
    for subf in curr_subf:
        if subf.code not in positive_sort + negative_sort:
            new_subf.append(subf)

    # Negative sort
    for code in negative_sort:
        for subf in curr_subf:
            if subf.code == code:
                new_subf.append(subf)
    
    return new_subf

def sort_subfields_for_tag(record:pymarc.record.Record, tag:str, sort:list[str]):
    """Sort subfields for all field with this tag :
    * If a subfield code is not in sort, its position will stay the same
    * If a subfield is in sort, it will be moved to that order
    * To sort at the end, use "*" as a code to separate values to use to sort at the beginning
    from values to use to sort at the end

    Takes as argument :
        - record : the pymarc record
        - tag : the field tag to sort (str)
        - sort : a list of subfield codes (str)"""
    
    for field in record.get_fields(tag):
        field.subfields = __sort_subfields(field.subfields, sort)

# ------------------------------ Force ------------------------------

def force_indicators(record:pymarc.record.Record, tag:str, indicators:List[str]=[" ", " "]):
    """Forces the indicators on every field with this tag in the record
    Defaults to no indicator
    
    /!\\ Does not check if indicators are legal values

    Takes as argument :
        - record : a pymarc record
        - tag : the tag to check (str)
        - indicators : the indicators (list of str)"""
    for field in record.get_fields(tag):
        field.indicators = indicators

# ------------------------------ Add ------------------------------

def add_missing_subfield_to_field(record:pymarc.record.Record, tag:str, code:str, val:str, pos:int=999):
    """Adds a subfield with this code with val to every field witht this tag only if the field
    does not already have a subfield with this code
    
    Takes as argument :
        - record : a pymarc record
        - tag : a field tag (str)
        - code : the subfield code (str)
        - val : the val to add
        - [OPTIONNAL] pos : the position if the subfield is added (default to 999)"""
    
    for field in record.get_fields(tag):
        if not code in field.subfields_as_dict():
            field.add_subfield(code, val, pos)

# ------------------------------ Edit ------------------------------

def edit_specific_repeatable_subfield_content_with_regexp(field:pymarc.field.Field, codes:List[str], pattern:str, repl:str) -> List[str]:
    """Apply a regexp substitution to all subfields of a code (no flag).
    Edits the field and also return the subfield list as [code, content, code2, content2, etc.]
    
    Takes as argument :
        - field : pymarc Field to edit
        - codes : list of codes to edit (str)
        - pattern : regexp pattern
        - repl : regexp sub pattern"""
    
    curr_subf:list = field.subfields
    new_subf = []
    for index in range(0, len(curr_subf), 2):
        # If not the right code, keep the subfield
        if curr_subf[index] not in codes:
            new_subf += curr_subf[index:index+2]
        # use the regex replace
        else:
            new_subf.append(curr_subf[index])
            new_subf.append(re.sub(pattern, repl, curr_subf[index+1]))
    # Updates the field
    field.subfields = new_subf
    return new_subf

def replace_specific_repeatable_subfield_content_not_matching_regexp(field:pymarc.field.Field, codes:List[str], pattern:str, repl:str) -> List[str]:
    """Replace all subfields of a code by a value if they do not match a regexp (no flag).
    Edits the field and also return the subfield list as [code, content, code2, content2, etc.]
    
    Takes as argument :
        - field : pymarc Field to edit
        - codes : list of codes to edit (str)
        - pattern : regexp pattern
        - repl : repalcement text"""
    
    curr_subf:list = field.subfields
    new_subf = []
    for index in range(0, len(curr_subf), 2):
        # If not the right code, keep the subfield
        if curr_subf[index] not in codes:
            new_subf += curr_subf[index:index+2]
        # use the regex replace
        else:
            new_subf.append(curr_subf[index])
            if not re.match(pattern, curr_subf[index+1]):
                new_subf.append(repl)
            else:
                new_subf.append(curr_subf[index+1])

    # Updates the field
    field.subfields = new_subf
    return new_subf

# ------------------------------ Merge ------------------------------

def merge_all_fields_by_tag(record:pymarc.record.Record, tag:str, sort:List[str]=[]) -> pymarc.field.Field|None:
    """Merge ALL fields with the tag as one, sorting them if wanted
    Edits the record and also returns the new field
    Indicators used are from the first field
    
    Takes as argument :
        - record : the pymarc record
        - tag : the field tag to merge (str)
        - sort : a list of subfield codes (str) (see sort_subfields for explanation)"""
    
    # Return if no match
    if record.get_fields(tag) == []:
        return None
    # Create the new field
    new_field = pymarc.field.Field(tag, record.get_fields(tag)[0].indicators)
    # Stores every existing subfield
    curr_subf = []
    for field in record.get_fields(tag):
        curr_subf += field.subfields

    # Sort the subfields    
    new_field.subfields = __sort_subfields(curr_subf, sort)

    # Replace current fields by the new one
    record.remove_fields(tag)
    record.add_ordered_field(new_field)
    return new_field

# ------------------------------ Split ------------------------------

def split_tags_if_multiple_specific_subfield(record:pymarc.record.Record, tag:str, code:str):
    """Splits a tag into multiple if there are multiple subfields with this code.
    Evry ther subfield if pasted with this one
    
    Takes as argument :
        - record : a pymarc record
        - tag : the tag to check (str)
        - code : the code to check (str)"""
    
    for field in record.get_fields(tag):
        # Leave if there is no subfield with this code
        if not code in field.subfields_as_dict():
            continue
        # Leave if there is only one subfield with this code
        if len(field.subfields_as_dict()[code]) < 2:
            continue
        # Get this subfield values
        vals = field.subfields_as_dict()[code]
        # Get all other subfield values
        other_subf = []
        for index in range(0, len(field.subfields), 2):
            if field.subfields[index] != code:
                other_subf += field.subfields[index:index+2]
        # Append new field for each subfield
        for val in vals:
            new_field = pymarc.field.Field(tag, field.indicators)
            new_field.subfields = other_subf + [code, val]
            record.add_ordered_field(new_field)

        # Delete the original field
        record.remove_field(field)

def split_merged_tags(record:pymarc.record.Record, tag:str):
    """Splits a tag into multiple if there are multiple subfields with the same code.
    In case some tags do not have all subfields, copies the first occurence of this subfield
    
    Takes as argument :
        - record : a pymarc record
        - tag : the tag to check (str)"""
    
    for field in record.get_fields(tag):
        all_subf = field.subfields_as_dict()
        # Skip this fieldif all subfields are not repeated
        skip = True
        highest_repeat = 1
        for code in all_subf:
            if len(all_subf[code]) > 1:
                skip = False
            if len(all_subf[code]) > highest_repeat:
                highest_repeat = len(all_subf[code])
        if skip:
            continue

        # Creates a list of dict
        list_of_new_fields:List[dict] = []
        for index in range(0, highest_repeat):
            new_field = {}
            for code in all_subf:
                # Index is not superior to maximum subfields for this code
                if index < len(all_subf[code]):
                    new_field[code] = all_subf[code][index]
                # Index is out of range, defaults to the first subfield
                else:
                    new_field[code] = all_subf[code][0]
            list_of_new_fields.append(new_field)

        # Adds every new field to the record
        for new_field_as_dict in list_of_new_fields:
            new_field = pymarc.field.Field(tag=tag, indicators=field.indicators)
            for code in new_field_as_dict:
                new_field.add_subfield(code, new_field_as_dict[code])
            record.add_ordered_field(new_field)
        
        # Delete the original field
        record.remove_field(field)

# ------------------------------ Delete ------------------------------
    
def delete_empty_subfields(record:pymarc.record.Record):
    "Deletes every empty subfields"
    for field in record:
        # Skip control fields
        if field.is_control_field():
            continue
        # If something is empty
        if "" in field.subfields:
            curr_subf = field.subfields
            new_subf = []
            for index in range(0, len(curr_subf), 2):
                if curr_subf[index+1] != "":
                    new_subf += curr_subf[index:index+2]
            field.subfields = new_subf

def delete_empty_fields(record:pymarc.record.Record):
    "Deletes every empty fields"
    for field in record:
        # Control fields
        if field.is_control_field():
            if field.data == "":
                record.remove_field(field)
        # Data fields
        else:
            if field.subfields == []:
                record.remove_field(field)


def delete_field_if_all_subfields_match_regexp(record:pymarc.record.Record, tag:str, code:str, pattern:str, keep_if_no_subf:bool=True):
    """Delete all fields for this tag if ALL subfields with this code match the regexp.
    
    Takes as argument :
        - record : a pymarc record
        - tag : the tag to check (str)
        - code : the code to check (str)
        - pattern : the regexp pattern to check
        - [OPTIONNAL, True] keep_if_no_subf : if set to false, deletes the field if
    no subfield had the code"""

    for field in record.get_fields(tag):
        # If the field is not here, keep or del (yeah nesting "if" was not necessary but easier to read)
        if not code in field.subfields_as_dict():
            if keep_if_no_subf:
                continue
            else:
                record.remove_field(field)
                continue
        
        # The field has subfields for this code
        delete = True
        for content in field.subfields_as_dict()[code]:
            # At least one of the subfied does not match, keep the field
            if not re.match(pattern, content):
                delete = False
        
        if delete:
            record.remove_field(field)


def delete_multiple_subfield_for_tag(record:pymarc.record.Record, tag:str, code:str):
    """Only keeps the first subfield with this code of all fields with this tag
    
    Takes as argument :
        - record : a pymarc record
        - tag : the tag to check (str)
        - code : the code to check (str)"""
    
    for field in record.get_fields(tag):
        # Leave if there is no subfield with this code
        if not code in field.subfields_as_dict():
            continue
        first = True
        curr_subf = field.subfields
        new_subf = []
        for index in range(0, len(curr_subf), 2):
            if curr_subf[index] != code:
                new_subf += curr_subf[index:index+2]
            elif curr_subf[index] == code and first:
                new_subf += curr_subf[index:index+2]
                first = False
        field.subfields = new_subf