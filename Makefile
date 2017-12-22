INPUT_DATA_DIR = data
INPUT_FILE = allsongs_responses.csv
RANK_DATA_DIR = output
RANK_INPUT_FILE = allsongs_responses_deduped.csv
OUTPUT_DATA_DIR = output
INTERMEDIATE_DATA_DIR = tmp

# EXAMPLE GOOGLE SPREADSHEET URL PUBLISHED AS A CSV Extract of 2017 data
CSV_URL=https://docs.google.com/spreadsheets/d/e/2PACX-1vTdnDO2daqBhCWFPPPwzqwHzZIyNDKS_N9af5QEx7HwgAT-bApIjireeZ_F6KAD30BSe49kWc4Dp7UE/pub?gid=43875107&single=true&output=csv

## clean_ballot_stuffing.py configuration
# 4 hours = 4 * 60 * 60 seconds
DUPLICATE_TIME_THRESHOLD=14400
# 1 hour = 60 * 60
RANDOM_ORDER_TIME_THRESHOLD=3600

## transform_form_responses.py configuration
# Decreased by one for each subsequent album/artist pair
MAX_POINTS=15
# 4th December
POLL_START_DAY=4
# 11th December
POLL_END_DAY=11

## pivot_cluster_day.py configuration
# Value to assign to a cluster ID that does not appear on a given day
NOTFOUND_VALUE=200



.PHONY: all clean

all:
	@echo "Use 'make dedupe' and after reviewing the clustering results 'make rank'"

# clean and dedupe rules
dedupe: $(OUTPUT_DATA_DIR)/allsongs_responses_deduped.csv

$(OUTPUT_DATA_DIR)/allsongs_responses_deduped.csv: $(OUTPUT_DATA_DIR)/allsongs_responses_normalized.csv
	./scripts/dedupe.sh $< > $@

$(OUTPUT_DATA_DIR)/allsongs_responses_normalized.csv: $(INPUT_DATA_DIR)/$(INPUT_FILE) $(OUTPUT_DATA_DIR)
	cat $< | \
	./scripts/clean_ballot_stuffing.py \
	--duplicate_threshold $(DUPLICATE_TIME_THRESHOLD) \
	--random_order_threshold $(RANDOM_ORDER_TIME_THRESHOLD) | \
	./scripts/transform_form_responses.py \
	--max_points $(MAX_POINTS) \
	--poll_start_day $(POLL_START_DAY) \
	--poll_end_day $(POLL_END_DAY) > $@

$(INPUT_DATA_DIR)/$(INPUT_FILE):
	curl -o $@ '$(CSV_URL)'

# Rank rules
rank: $(OUTPUT_DATA_DIR)/allsongs_responses_top100.csv

$(OUTPUT_DATA_DIR)/allsongs_responses_top100.csv: $(INTERMEDIATE_DATA_DIR)/allsongs_responses_ranked.csv
	cat $< | head -n 101 > $@

$(INTERMEDIATE_DATA_DIR)/allsongs_responses_ranked.csv: $(OUTPUT_DATA_DIR)/allsongs_responses_deduped_standard.csv $(INTERMEDIATE_DATA_DIR)/allsongs_responses_aggclusterperiod.csv
	./scripts/merge_cluster_ranking_album_artist.py $^ | ./scripts/rankall.py > $@

$(INTERMEDIATE_DATA_DIR)/allsongs_responses_aggclusterperiod.csv: $(INTERMEDIATE_DATA_DIR)/allsongs_responses_pivotclusterbyday.csv
	cat $< | ./scripts/aggregate_cluster_period.py > $@

$(INTERMEDIATE_DATA_DIR)/allsongs_responses_pivotclusterbyday.csv: $(OUTPUT_DATA_DIR)/allsongs_responses_deduped_standard.csv $(INTERMEDIATE_DATA_DIR)
	cat $< | ./scripts/rank_cluster_day.py | \
	./scripts/pivot_cluster_day.py \
	--notfound_value $(NOTFOUND_VALUE) > $@

$(OUTPUT_DATA_DIR)/allsongs_responses_deduped_standard.csv: $(RANK_DATA_DIR)/$(RANK_INPUT_FILE) $(OUTPUT_DATA_DIR)
	cat $< | ./scripts/standarize_cluster_responses.py  > $@


# Aux rules
$(INTERMEDIATE_DATA_DIR):
	mkdir -p $(INTERMEDIATE_DATA_DIR)

$(OUTPUT_DATA_DIR):
	mkdir -p $(OUTPUT_DATA_DIR)

clean:
	rm -rf $(OUTPUT_DATA_DIR)
	rm -rf $(INTERMEDIATE_DATA_DIR)
	rm $(INPUT_DATA_DIR)/$(INPUT_FILE)

# Daily report of ranking of top100 album/artist per day
# Used by music for verification purposes
$(OUTPUT_DATA_DIR)/allsongs_responses_dailyreport.csv: $(OUTPUT_DATA_DIR)/allsongs_responses_top100.csv $(INTERMEDIATE_DATA_DIR)/allsongs_responses_pivotclusterbyday.csv
	./scripts/dailyreport.py $^ > $@
