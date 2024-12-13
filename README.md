# Pymarc utils

[![Active Development](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

A set of functions to handle data using [Python `pymarc` library](https://pypi.org/project/marc/) :

* `marc_utils_4.py` using version 4.2.2 of the library
* `marc_utils_5.py` using version 5.2.0

## Incompatible changes from `marc_utils_4.py` to `marc_utils_5.py`

* `__sort_subfields()` parameter `curr_subf` was renammed to `subf_list`
* `force_indicators` :
  * Parameter `indicators` (list of strings, defaulted to `[" ", " "]`) was changed to become two parameter `ind1` & `ind2`, both `str` defaulted to `None`
  * Now, if their value is set to `None` (default behaviour), keeps their current value (before, default behaviour was to write to a blank and this function could not be used to keep the current field indicators)
* `edit_specific_repeatable_subfield_content_with_regexp()` returns a list of `pymarc.field.Subfield` instead of a list of string following old subfield managing system (code 1, value 1, code 2, value 2, etc.)
* Added `edit_repeatable_subf_content_with_regexp_for_tag()` which is the same as `edit_specific_repeatable_subfield_content_with_regexp()` except it takes as argument a record and a tag and edit all fields with that tag, like all functions except the two using regular expressions
* `replace_specific_repeatable_subfield_content_not_matching_regexp()` returns a list of `pymarc.field.Subfield` instead of a list of string following old subfield managing system (code 1, value 1, code 2, value 2, etc.)
* Added `replace_repeatable_subf_content_not_matching_regexp_for_tag()` which is the same as `replace_specific_repeatable_subfield_content_not_matching_regexp()` except it takes as argument a record and a tag and edit all fields with that tag, like all functions except the two using regular expressions
* Added `field_as_string()` and `record_as_string()` which returns the field / record as a string in WinIBW style
* Added all functions to retrieve dates from the record (`get_years_in_specific_subfield()`, `get_year_from_UNM_100()`, `get_years_less_accurate()` & `get_years()`)
* Added `merge_all_subfields_with_code()` to merge all subfields witht the same code for each field with given tag

_See [`pymarc` releases in the GitLab repository](https://gitlab.com/pymarc/pymarc/-/releases) for important changes in the library._

## Functions

### Getting data from fields

#### Function `get_years_in_specific_subfield()`

Returns a `list` of `ints` containing the first 4 consecutive numbers in the specified field-subfield couple.

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag
* `code` (`str`) : the subfields code tag

#### Function `get_year_from_UNM_100()`

Returns a `list` of `ints` containing the position 9-12 or 0-3 of the `100$a` if they are 4 consecutive numbers.

Takes as argument :

* `record` (`pymarc.record.Record`)
* _[Optionnal]_ `creation` (`bool`, defaulted to `False`) : return the creation date (pos. 0-3) instead of the publication one (pos. 9-12)

#### Function `get_years_less_accurate()`

Returns a `list` of `ints` containing the first 4 consecutive numbers in the specified field (all subfields are analyzed).
_Note : dates inferior to 1700 or superioir to 2100 are deleted before returning the `list`._

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag

#### Function `get_years()`

Returns a `list` of `ints` containing either :

* The first 4 consecutive numbers in the specified field-subfield (calls `get_years_in_specific_subfield()`)
* The first 4 consecutive numbers in the specified field (calls `get_years_less_accurate()`).

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tags` (`list` of `tuple` of 2 `str`) : a list of field + subfield or field + `None`

Example :

``` Python
marc_utils.get_years(record, [
            ("214", "d"),
            ("330", None),
            ("615", "a"),
            ("200", None),
            ])
# Will call get_years_in_specific_subfield() for 214$d
# Then get_years_less_accurate() for 330
# Then get_years_in_specific_subfield() for 615$a
# Then get_years_less_accurate() for 200
```

### Sorting fields or subfields

#### `sort` argument logic

Every functions that uses sort on subfields follow this logic :

* If a subfield code is not in the `sort` argument, its position will stay the same relative to the other subfields not moving
* If a subfield is in the `sort` argument, it will be moved to that order
* To sort at the end, use `*` as a code to separate codes used to sort at the beginning from codes used to sort at the end

For example :

* `["a", "b"]` will put at the beginning all subfields using code `a`, followed by all subfields using code `b`, followed by all other subfields, keeping their original order
* `["*", "y", "z"]` will keep every subfield in their original order except those with codes `y` & `z`, followed by all subfields with code `y`, followed at the end by all subfields with code `z`
* `["a", "*", "z"]` will put at the beginning all subfields using code `a`, followed by all other subfields except those with codes `z`, followed at the end by all subfields with code `z`

#### Function `sort_fields_by_tag()`

Sorts the record fields by their tag.

Takes as argument : `record` (`pymarc.record.Record`)

#### Function `sort_subfields_for_tag()`

Sorts subfields for all fields with given tag.

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to sort
* `sort` (`list` of `str`) : list of subfields codes to sort. See [_`sort` argument logic_](#sort-argument-logic) to see how to configure it for this indicator.

### Forcing data

#### Function `force_indicators()`

Forces the indicators on every field with given tag.
If an indicator is set to `None`, the field will keep it's current value.

__The function does not check if given values are legal values.__

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to edit
* `ind1` (`str`, default to `None`) : first indicator value
* `ind2` (`str`, default to `None`) : second indicator value

### Adding data

#### Function `add_missing_subfield_to_field()`

Adds a new subfield with given code & value to every field with given tag if they do not already have a subfield with that code.

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to edit
* `code` (`str`) : the subfield code
* `val` (`str`) : the subfield value to add
* _[Optionnal]_ `pos` (`int`, defaulted to `999`) : the position of the new subfield (if added). _First position is `0`_

#### Function `edit_repeatable_subf_content_with_regexp_for_tag()`

Applies a substitution using regular expression to all subfields with given codes for all fields with given tag.
No flag are used and no flag can be set.

_Alternate version `edit_specific_repeatable_subfield_content_with_regexp()` is not described here to keep all documented functions using the same logic in arguments to pass._

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to edit
* `codes` (`list` of `str`) : list of subfield codes to edit
* `pattern` (`str`) : regular expression matching pattern
* `repl` (`str`) : regular expression substitution expression

#### Function `replace_repeatable_subf_content_not_matching_regexp_for_tag()`

Replaces all subfields value with given codes for all fields with given tag if they do not match given regular expression.
No flag are used and no flag can be set.

_Alternate version `replace_specific_repeatable_subfield_content_not_matching_regexp()` is not described here to keep all documented functions using the same logic in arguments to pass._

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to edit
* `codes` (`list` of `str`) : list of subfield codes to edit
* `pattern` (`str`) : regular expression matching pattern
* `repl` (`str`) : the replacement text to use

#### Function `fix_7XX()`

Change tags in `7XX` fields to make sure that only 1 `7X0` is in the record and there's at least one `7X0` if there are `7X1` or `7X2`

Takes as argument :

* `record` (`pymarc.record.Record`)
* _[Optionnal]_ `prioritize_71X` (`bool`, default to `False`) : prioritize `710` over `700`

### Merge fields

#### Function `merge_all_fields_by_tag()`

Merges __all__ fields with given tag, sorting the subfields if wanted.
Edits the record __and returns the new field__ (`pymarc.field.Field`).
Indicators used are those from the first field occurrence.

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to merge
* _[Optionnal]_ `sort` (`list` of `str`, default to no sort) : list of subfields codes to sort. See [_`sort` argument logic_](#sort-argument-logic) to see how to configure it.

#### Function `merge_all_subfields_with_code()`

Merges all subfields with given code in every field with given tag.
The position of the first subfield will be kept.

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to edit
* `code` (`str`) : the subfield code to merge
* `separator` (`str`) : the separtor to use between subfields

### Split fields

#### Function `split_tags_if_multiple_specific_subfield()`

Splits all fields with given tag into multiple fields if the field has multiple subfields with given code.
Every other subfield is copied into all created fields.

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to split
* `code` (`str`) : the subfield code to check

#### Function `split_merged_tags()`

Splits all fields with given tag into multiple fields if there are multiple subfields with the same code.
In case some fields sufields have less occurrence than other subfields, copies the first subfield occurence for this code.

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to split

### Delete data

#### Function `delete_empty_subfields()`

Deletes every empty subfields in whole the record.

Takes as argument : `record` (`pymarc.record.Record`)

#### Function `delete_empty_fields()`

Deletes every empty fields in whole the record.

Takes as argument : `record` (`pymarc.record.Record`)

#### Function `delete_field_if_all_subfields_match_regexp()`

For all fields with given tag, deletes the entire field if __all__ subfields with given code match the given regular expression.

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to delete
* `code` (`str`) : the subfield code to check
* `pattern` (`str`) : regular expression matching pattern
* _[Optionnal]_  `keep_if_no_subf` (`bool`, default to `True`) : if no subfield has given code, should the field be __kept__

#### Function `delete_multiple_subfield_for_tag()`

For all fields with given tag, only keeps the first subfield with given code.

Takes as argument :

* `record` (`pymarc.record.Record`)
* `tag` (`str`) : the fields tag to edit
* `code` (`str`) : the subfield code to keep only once

### Debugging

#### Function `field_as_string()`

Returns the field as a string in WinIBW (blank indicators are returned as `#`)

Takes as argument :

* `field` (`pymarc.field.Field`)

#### Function `record_as_string()`

Returns the record as a string in WinIBW (blank indicators are returned as `#`)

Takes as argument :

* `record` (`pymarc.record.Record`)