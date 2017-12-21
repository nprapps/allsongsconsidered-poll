INPUT_DATA_DIR = data
INPUT_FILE = 2017_responses.csv
OUTPUT_DATA_DIR = output


.PHONY: all clean

all: $(OUTPUT_DATA_DIR)/2017_responses_deduped.csv

$(OUTPUT_DATA_DIR)/2017_responses_deduped.csv: $(OUTPUT_DATA_DIR)/2017_responses_normalized.csv
	./scripts/dedupe.sh $< > $@

$(OUTPUT_DATA_DIR)/2017_responses_normalized.csv: $(OUTPUT_DATA_DIR)/2017_responses_clean.csv
	cat $< | ./scripts/transform_form_responses.py > $@

$(OUTPUT_DATA_DIR)/2017_responses_clean.csv: $(INPUT_DATA_DIR)/$(INPUT_FILE) $(OUTPUT_DATA_DIR)
	cat $< | ./scripts/clean_ballot_stuffing.py > $@

$(OUTPUT_DATA_DIR):
	mkdir -p $(OUTPUT_DATA_DIR)

clean:
	rm -rf $(OUTPUT_DATA_DIR)
