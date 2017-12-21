INPUT_DATA_DIR = data
INPUT_FILE = 2017_responses.csv
RANK_DATA_DIR = output
RANK_INPUT_FILE = 2017_responses_deduped.csv
OUTPUT_DATA_DIR = output
INTERMEDIATE_DATA_DIR = tmp


.PHONY: all clean

all:
	@echo "Use 'make clean_dedupe' and after reviewing the clustering results 'make rank'"

# clean and dedupe rules
clean_dedupe: $(OUTPUT_DATA_DIR)/2017_responses_deduped.csv

$(OUTPUT_DATA_DIR)/2017_responses_deduped.csv: $(OUTPUT_DATA_DIR)/2017_responses_normalized.csv
	./scripts/dedupe.sh $< > $@

$(OUTPUT_DATA_DIR)/2017_responses_normalized.csv: $(INPUT_DATA_DIR)/$(INPUT_FILE) $(OUTPUT_DATA_DIR)
	cat $< | ./scripts/clean_ballot_stuffing.py | ./scripts/transform_form_responses.py > $@

# Rank rules
rank: $(OUTPUT_DATA_DIR)/2017_responses_top100.csv

$(OUTPUT_DATA_DIR)/2017_responses_top100.csv: $(INTERMEDIATE_DATA_DIR)/2017_responses_ranked.csv
	cat $< | head -n 101 > $@

$(INTERMEDIATE_DATA_DIR)/2017_responses_ranked.csv: $(OUTPUT_DATA_DIR)/2017_responses_deduped_standard.csv $(INTERMEDIATE_DATA_DIR)/2017_responses_aggclusterperiod.csv
	./scripts/merge_cluster_ranking_album_artist.py $^ | ./scripts/rankall.py > $@

$(INTERMEDIATE_DATA_DIR)/2017_responses_aggclusterperiod.csv: $(INTERMEDIATE_DATA_DIR)/2017_responses_pivotclusterbyday.csv
	cat $< | ./scripts/aggregate_cluster_period.py > $@

$(INTERMEDIATE_DATA_DIR)/2017_responses_pivotclusterbyday.csv: $(OUTPUT_DATA_DIR)/2017_responses_deduped_standard.csv $(INTERMEDIATE_DATA_DIR)
	cat $< | ./scripts/rank_cluster_day.py | ./scripts/pivot_cluster_day.py > $@

$(OUTPUT_DATA_DIR)/2017_responses_deduped_standard.csv: $(RANK_DATA_DIR)/$(RANK_INPUT_FILE) $(OUTPUT_DATA_DIR)
	cat $< | ./scripts/standarize_cluster_responses.py  > $@


# Aux rules
$(INTERMEDIATE_DATA_DIR):
	mkdir -p $(INTERMEDIATE_DATA_DIR)

$(OUTPUT_DATA_DIR):
	mkdir -p $(OUTPUT_DATA_DIR)

clean:
	rm -rf $(OUTPUT_DATA_DIR)

# Daily report of ranking of top100 album/artist per day
# Used by music for verification purposes
$(OUTPUT_DATA_DIR)/2017_responses_dailyreport.csv: $(OUTPUT_DATA_DIR)/2017_responses_top100.csv $(INTERMEDIATE_DATA_DIR)/2017_responses_pivotclusterbyday.csv
	./scripts/dailyreport.py $^ > $@
