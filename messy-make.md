INPUT_DATA_DIR = data
INPUT_FILE = allsongs_responses.csv
RANK_DATA_DIR = output
RANK_INPUT_FILE = allsongs_responses_deduped.csv
OUTPUT_DATA_DIR = output
INTERMEDIATE_DATA_DIR = tmp

# EXAMPLE GOOGLE SPREADSHEET URL PUBLISHED AS A CSV Extract of 2017 data
CSV_URL='https://docs.google.com/spreadsheets/d/e/2PACX-1vSMW2pbk3YWfNWU4C0wHVdMr90oHvyMHrRp_SJlUei6P1bnQDUWKOfBkR2zi3QFefk2GEfv5TTE-vJw/pub?gid=1988637773&single=true&output=csv'

## clean_ballot_stuffing.py configuration
# 4 hours = 4 * 60 * 60 seconds
DUPLICATE_TIME_THRESHOLD=14400
# 1 hour = 60 * 60
RANDOM_ORDER_TIME_THRESHOLD=3600

## transform_form_responses.py configuration
MAX_SUBMIT=10
# Poll opened on March 21, 2018
POLL_START_DATE='3/21/2018'
# Poll closed April 2, 2018
POLL_END_DATE='4/2/2018'

## pivot_cluster_day.py configuration
# Value to assign to a cluster ID that does not appear on a given day
NOTFOUND_VALUE=200
# Value to assign when there are no votes on a given day
NOVOTES_VALUE=0

# ranked output configuration
RANKED_OUTPUT_NUM=100
RANKED_OUTPUT_NUM+=1

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
	--max_submit $(MAX_SUBMIT) \
	--poll_start_date $(POLL_START_DATE) \
	--poll_end_date $(POLL_END_DATE) > $@

$(INPUT_DATA_DIR)/$(INPUT_FILE): $(INPUT_DATA_DIR)
	curl -o $@ '$(CSV_URL)'


# Rank rules
rank: $(OUTPUT_DATA_DIR)/allsongs_responses_top100.csv

$(OUTPUT_DATA_DIR)/allsongs_responses_top100.csv: $(INTERMEDIATE_DATA_DIR)/allsongs_responses_ranked.csv
	cat $< | head -n $(RANKED_OUTPUT_NUM) > $@


$(INTERMEDIATE_DATA_DIR)/allsongs_responses_ranked.csv: $(OUTPUT_DATA_DIR)/allsongs_responses_deduped_standard.csv $(INTERMEDIATE_DATA_DIR)/allsongs_responses_aggclusterperiod.csv
	./scripts/merge_cluster_ranking_album_artist.py $^ | ./scripts/rankall.py > $@

	# PRINTS:
	# ./scripts/merge_cluster_ranking_album_artist.py output/allsongs_responses_deduped_standard.csv tmp/allsongs_responses_aggclusterperiod.csv | ./scripts/rankall.py > tmp/allsongs_responses_ranked.csv
	# ./scripts/merge_cluster_ranking_album_artist.py output/allsongs_responses_deduped_standard.csv tmp/aggclusterperiod.csv | ./scripts/rankall.py > tmp/ranked.csv

# Modified to sum and output total points
$(INTERMEDIATE_DATA_DIR)/allsongs_responses_aggclusterperiod.csv: $(INTERMEDIATE_DATA_DIR)/allsongs_responses_pivotclusterbyday.csv
	cat $< | ./scripts/aggregate_cluster_period.py > $@

	# PRINTS:
	# cat tmp/allsongs_responses_pivotclusterbyday.csv | ./scripts/aggregate_cluster_period.py > tmp/aggclusterperiod.csv
	# cat tmp/sum_per_day.csv | ./scripts/aggregate_cluster_period.py > tmp/aggclusterperiod.csv

# Modified to sum points per day instead of calculate a rank per day, pivot has a TODO
$(INTERMEDIATE_DATA_DIR)/allsongs_responses_pivotclusterbyday.csv: $(OUTPUT_DATA_DIR)/allsongs_responses_deduped_standard.csv $(INTERMEDIATE_DATA_DIR)
	cat $< | ./scripts/rank_cluster_day.py | \
	./scripts/pivot_cluster_day.py \
	--notfound_value $(NOTFOUND_VALUE) --novotes_value $(NOVOTES_VALUE) > $@

	# PRINTS:
	# cat output/allsongs_responses_deduped_standard.csv | ./scripts/rank_cluster_day.py | ./scripts/pivot_cluster_day.py > tmp/sum_per_day.csv

$(OUTPUT_DATA_DIR)/allsongs_responses_deduped_standard.csv: $(RANK_DATA_DIR)/$(RANK_INPUT_FILE) $(OUTPUT_DATA_DIR)
	cat $< | ./scripts/standarize_cluster_responses.py  > $@

# Aux rules
$(INTERMEDIATE_DATA_DIR):
	mkdir -p $(INTERMEDIATE_DATA_DIR)

$(OUTPUT_DATA_DIR):
	mkdir -p $(OUTPUT_DATA_DIR)

$(INPUT_DATA_DIR):
	mkdir -p $(INPUT_DATA_DIR)

clean:
	rm -rf $(OUTPUT_DATA_DIR)
	rm -rf $(INTERMEDIATE_DATA_DIR)
	rm $(INPUT_DATA_DIR)/$(INPUT_FILE)

# Daily report of ranking of top100 album/artist per day
# Used by music for verification purposes
$(OUTPUT_DATA_DIR)/allsongs_responses_dailyreport.csv: $(OUTPUT_DATA_DIR)/allsongs_responses_top100.csv $(INTERMEDIATE_DATA_DIR)/allsongs_responses_pivotclusterbyday.csv
	./scripts/dailyreport.py $^ > $@
