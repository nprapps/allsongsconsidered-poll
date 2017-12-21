INPUT_DATA_DIR = output
INPUT_FILE = 2017_responses_deduped_refine.csv
OUTPUT_DATA_DIR = output
INTERMEDIATE_DATA_DIR = tmp


.PHONY: all clean report

all: $(OUTPUT_DATA_DIR)/2017_responses_top100.csv

$(OUTPUT_DATA_DIR)/2017_responses_top100.csv: $(INTERMEDIATE_DATA_DIR)/2017_responses_ranked.csv
	cat $< | head -n 101 > $@

$(INTERMEDIATE_DATA_DIR)/2017_responses_ranked.csv: $(INTERMEDIATE_DATA_DIR)/2017_responses_clustermergedalbumartist.csv
	cat $< | ./scripts/rankall.py > $@

$(INTERMEDIATE_DATA_DIR)/2017_responses_clustermergedalbumartist.csv: $(OUTPUT_DATA_DIR)/2017_responses_deduped_standard.csv $(INTERMEDIATE_DATA_DIR)/2017_responses_aggclusterperiod.csv
	./scripts/merge_cluster_ranking_album_artist.py $^ > $@

$(INTERMEDIATE_DATA_DIR)/2017_responses_aggclusterperiod.csv: $(INTERMEDIATE_DATA_DIR)/2017_responses_pivotclusterbyday.csv
	cat $< | ./scripts/aggregate_cluster_period.py > $@

$(INTERMEDIATE_DATA_DIR)/2017_responses_pivotclusterbyday.csv: $(INTERMEDIATE_DATA_DIR)/2017_responses_rankbydayandcluster.csv
	cat $< | ./scripts/pivot_cluster_day.py > $@

$(INTERMEDIATE_DATA_DIR)/2017_responses_rankbydayandcluster.csv: $(OUTPUT_DATA_DIR)/2017_responses_deduped_standard.csv $(INTERMEDIATE_DATA_DIR)
	cat $< | ./scripts/rank_cluster_day.py > $@

$(OUTPUT_DATA_DIR)/2017_responses_deduped_standard.csv: $(INPUT_DATA_DIR)/$(INPUT_FILE) $(OUTPUT_DATA_DIR)
	cat $< | ./scripts/standarize_cluster_responses.py > $@

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

