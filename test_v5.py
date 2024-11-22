# -*- coding: utf-8 -*- 

# external imports
import pymarc

# Internal import
import marc_utils_5 as marc_utils

MARC_READER = pymarc.MARCReader(open("test_records.mrc", "rb"), to_unicode=True, force_utf8=True) # DON'T FORGET ME
MARC_WRITER = open("test_records_modified.mrc", "wb") # DON'T FORGET ME

# Loop through records
for index, record in enumerate(MARC_READER):
    print(f"--- Starting Record {index}")

    # If record is invalid
    if record is None:
        print(f"Current chunk: {MARC_READER.current_chunk} was ignored because the following exception raised: {MARC_READER.current_exception}")
        continue

    record_nb = record["001"].data

    # Record 000001 : test sorting fields
    marc_utils.sort_fields_by_tag(record)

    # Record 000002 : test sorting subfields
    marc_utils.sort_subfields_for_tag(record, "610", ["9", "a", "*", "8", "z"])
    marc_utils.sort_subfields_for_tag(record, "615", ["0", "f"])
    marc_utils.sort_subfields_for_tag(record, "620", ["*", "5", "k"])

    # Record 000003 : test forcing indicators
    if record_nb == "000003":
        marc_utils.force_indicators(record, "200")
        marc_utils.force_indicators(record, "330", ind1="3", ind2=" ")
        marc_utils.force_indicators(record, "701", ind1="9")
        marc_utils.force_indicators(record, "702", ind2="8")

    # Recod 000004 : test adding missing subfields
    if record_nb == "000004":
        marc_utils.add_missing_subfield_to_field(record, "701", "z", "fre", 5)

    # Record 000005 : test edit specific subfields with regexp (old & new func)
    if record_nb == "000005":
        marc_utils.edit_specific_repeatable_subfield_content_with_regexp(record["101"], ["a", "c"], r"^\s*([a-z]{3})\s*$", r"\1")
        marc_utils.edit_specific_repeatable_subfield_content_with_regexp(record["330"], ["a"], r"^\s+$", "")
        marc_utils.edit_repeatable_subf_content_with_regexp_for_tag(record, "102", ["a", "c"], r"^\s*([A-Z]{2})\s*$", r"\1")
        marc_utils.edit_repeatable_subf_content_with_regexp_for_tag(record, "200", ["e"], r"^\s+$", "")

    # Record 000006 : test replacing specific subfields not maching regexp (old & new func)
    if record_nb == "000006":
        marc_utils.replace_specific_repeatable_subfield_content_not_matching_regexp(record["101"], ["a", "c"], r"^[a-z]{3}$", "und")
        marc_utils.replace_specific_repeatable_subfield_content_not_matching_regexp(record["330"], ["a"], r"^Résumé \:", "Résumé invalide")
        marc_utils.replace_repeatable_subf_content_not_matching_regexp_for_tag(record, "102", ["a", "c"], r"^[A-Z]{2}$", r"??")
        marc_utils.replace_repeatable_subf_content_not_matching_regexp_for_tag(record, "200", ["e"], r"^in :", "ARA ARA ARA")

    # Record 000007 : test merging fields
    marc_utils.merge_all_fields_by_tag(record, "099")
    marc_utils.merge_all_fields_by_tag(record, "181", ["6", "*", "2"])

    # Record 000008 : test splitting a field if a specific subfield is repeated
    marc_utils.split_tags_if_multiple_specific_subfield(record, "463", "t")

    # Record 000009 : test splitting field that have multiple times subfields
    marc_utils.split_merged_tags(record, "995")
    marc_utils.split_merged_tags(record, "777")

    # Record 000010 : test deleting empty subfields & empty fields
    if record_nb == "000010":
        marc_utils.delete_empty_subfields(record)
        marc_utils.delete_empty_fields(record)

    # Record 000011 : test deleting fields if a subfield matches a regexp
    marc_utils.delete_field_if_all_subfields_match_regexp(record, "410", "t", r"^\s+$", keep_if_no_subf=False)
    marc_utils.delete_field_if_all_subfields_match_regexp(record, "412", "t", r"^\s+$", keep_if_no_subf=True)

    # Record 000012 : test deleting multiple subfields in a field
    marc_utils.delete_multiple_subfield_for_tag(record, "725", "4")

    # Print the record in the terminak
    print(marc_utils.record_as_string(record))

    # Write record
    MARC_WRITER.write(record.as_marc())

MARC_READER.close()
MARC_WRITER.close()