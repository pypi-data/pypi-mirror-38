# read rev JSON files
import json
import sys
import logging
import pandas
import time
import os


log = logging.getLogger(__file__)
handler = logging.StreamHandler()
log.addHandler(handler)
log.setLevel(logging.WARNING)


def json_reader(input_file):
    """
    Read JSON from rev
    Arguments:
        input_file (str, required) : Path to JSON file
    Returns:
        dictionary parsed from JSON
    """
    with open(input_file, "r") as jsonin:
        output_dict =  json.load(jsonin)
    log.debug("json_reader read file '{}' with length {}".format(input_file, len(output_dict)))
    return output_dict

def rev_json_parser(input_dict, additional_offset = 0):
    """
    Convert the JSON created `input_dict` towards FAVE format
    Defined here: https://github.com/JoFrhwld/FAVE/wiki/Using-FAVE-align
    Args:
        input_dict (dict, required) : input_dict as created from Rev annotation transcript
        additional_offset (float, optional) : number to add to / subtract from each timestamp; defaults to 0
    Returns:
        list of dicts with keys required to make DataFrame for FAVE
    """
    count, fails = 0, 0
    output_list = []
    speaker_dict = {dicti["id"] : dicti["name"] for dicti in input_dict["speakers"]}
    log.debug("Speakers: {}".format(speaker_dict))
    monologues = input_dict["monologues"]
    for monologue in monologues:
        spans = monologue["spans"]
        annotated_spans = [i for i in spans if i.get("ts") and i.get("endTs")]
        fails += len(spans) - len(annotated_spans)
        if annotated_spans:
            speaker_id = monologue.get("speaker")
            speaker_name = speaker_dict.get(speaker_id)
            onset, offset = annotated_spans[0]["ts"], annotated_spans[-1]["endTs"]
            transcription = " ".join([i.get("value") for i in annotated_spans])
            fave_dict = {           
                        "speaker_id": speaker_id,
                        "speaker_name": speaker_name,
                        "onset": onset + additional_offset,
                        "offset": offset + additional_offset,
                        "transcription": transcription
                    }
            output_list.append(fave_dict)
    log.debug("{} spans output by rev_json_parser".format(len(output_list)))
    log.debug("{} spans did not have complete timestamp information".format(fails))
    return output_list

def fave_csv_writer(input_list, output_file):
    """
    Takes a list of dicts to write to CSV
    Arguments:
        input_list (list, required) : a list of dicts, to be fed into DataFrame.from_records
        output_file (str, required) : path to write the CSV file to
    Returns:
        Nothing
    """
    ordered_cols = ["speaker_id", "speaker_name", "onset", "offset", "transcription"]
    df = pandas.DataFrame.from_records(input_list)
    df.to_csv(output_file, index = False, columns = ordered_cols, sep = "\t", header = False)
    log.debug("Written fave_csv to '{}'".format(output_file))

if __name__ == "__main__":
    """
    User needs to input (drag & drop) a folder containing json files with rev transcripts. 
    """
    if len(sys.argv) < 2:
        raise IOError("Not enough inputs: 'folder_name' needed")
    if len(sys.argv) > 3:
        raise IOError("Too many inputs: only 'folder_name', 'additional_offset' needed. Inputs given: {}".format(",".join(sys.argv)))
    if len(sys.argv) == 3:
        additionaloffset = float(sys.argv[2])
    else: 
        additionaloffset = 0
    inputfolder = sys.argv[1]
    for fili in [os.path.join(inputfolder, i) for i in os.listdir(inputfolder) if i.lower().endswith(".json")]:
        print ("Working on input file '{}'".format(fili))
        timestamp = time.strftime("%Y%m%d-%H%M")
        outputfile = "_".join([os.path.split(fili)[1].lower().rstrip(".json"), timestamp, "faved.csv"])
        outputpath = os.path.join(os.path.split(fili)[0], outputfile)
        json_dict = json_reader(fili)
        parsed_list = rev_json_parser(json_dict, additional_offset = additionaloffset)
        fave_csv_writer(input_list = parsed_list, output_file = outputpath)
        print ("CSV file written to '{}'".format(outputpath))
