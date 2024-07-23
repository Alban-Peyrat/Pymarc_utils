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


    # Write record
    MARC_WRITER.write(record.as_marc())

MARC_READER.close()
MARC_WRITER.close()