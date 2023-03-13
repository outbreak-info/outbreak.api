# API Documentation

## 1. Sequence counts

Description
```
Returns number of sequences per day by location
```

Endpoint: https://api.outbreak.info/genomics/sequence-count

Parameters

* `location_id` (Optional). If not specified, the global total counts are returned.
* `cumulative` (Optional). If `true` returns the cumulative number of sequences till date.
* `subadmin` (Optional). If `true` and `cumulative`=`true`,  returns the cumulative number of sequences for the immedaite lower admin level.

Examples,
Number of sequences per day globally.
https://api.outbreak.info/genomics/sequence-count

Cumulative number of sequences for every US state.
https://api.outbreak.info/genomics/sequence-count?location_id=USA&cumulative=true&subadmin=true

Daily number of sequences for California
https://api.outbreak.info/genomics/sequence-count?location_id=USA_US-CA

## 2. Global daily prevalence of a PANGO lineage [DEPRECATED]
**Deprecated: changed `location_id` to be an optional field in #3**

```
Returns the global daily prevalence of a PANGO lineage
```

Endpoint: https://api.outbreak.info/genomics/global-prevalence

Parameters

* `pangolin_lineage` (Required).
* `mutations` (Optional). Comma separated list of mutations.
* `cumulative` (Optional). If `true` returns the cumulative global prevalence since the first day of detection.

Examples,
Global daily prevalence of B.1.1.7 lineage
https://api.outbreak.info/genomics/global-prevalence?pangolin_lineage=b.1.1.7

Global daily prevalence of B.1.1.7 lineage with S:E484K mutation
https://api.outbreak.info/genomics/global-prevalence?pangolin_lineage=b.1.1.7&mutations=S:E484K

Cumulative global prevalence of B.1.1.7
https://api.outbreak.info/genomics/global-prevalence?pangolin_lineage=b.1.1.7&cumulative=true

## 3. Daily prevalence of a PANGO lineage by location

```
Returns the daily prevalence of a PANGO lineage by location
```

Endpoint: https://api.outbreak.info/genomics/prevalence-by-location

Parameters

* `pangolin_lineage` (Required). List of lineages separated by `,`
* `location_id` (Optional).
* `mutations` (Optional). List of mutations separated by `AND`
* `cumulative` (Optional). If `true` returns the cumulative global prevalence since the first day of detection.

Examples,

Global daily prevalence of B.1.1.7 lineage in the United States
https://api.outbreak.info/genomics/prevalence-by-location?pangolin_lineage=b.1.1.7&location_id=USA

Global daily prevalence of B.1.1.7 lineage with S:E484K mutation in the United States
https://api.outbreak.info/genomics/prevalence-by-location?pangolin_lineage=b.1.1.7&mutations=S:E484K&location_id=USA

Cumulative prevalence of B.1.1.7 in the United States
https://api.outbreak.info/genomics/prevalence-by-location?pangolin_lineage=b.1.1.7&cumulative=true&location_id=USA


## 4. Cumulative prevalence of a PANGO lineage by the immediate admin level of a location

Endpoint: https://api.outbreak.info/genomics/lineage-by-sub-admin-most-recent

Parameters:

* `pangolin_lineage` (Required). List of lineages separated by `,`
* `mutations` (Optional). List of mutations separated by `AND`.
* `location_id`  (Optional). If not specified, returns cumulative prevalence at the country level globally.
* `ndays` (Optional). Specify number of days from current date to calculative cumuative counts. If not specified, there is no limit on the window.
* `detected` (Optional). If `true` returns ony if at least


## 5. Most recent collection date by location

Endpoint: https://api.outbreak.info/genomics/most-recent-collection-date-by-location

Parameters:

* `pangolin_lineage` (Required).
* `mutations` (Optional). Comma separated list of mutations.
* `location_id`  (Optional). If not specified, return most recent date globally.

Examples,

Most recent collection date of B.1.1.7 PANGO lineage globally.
https://api.outbreak.info/genomics/most-recent-collection-date-by-location?pangolin_lineage=b.1.1.7

Most recent collection date of B.1.1.7 PANGO lineage with S:E484K globally.
https://api.outbreak.info/genomics/most-recent-collection-date-by-location?pangolin_lineage=b.1.1.7&mutations=S:E484K

Most recent collection date of B.1.1.7 PANGO lineage in California
https://api.outbreak.info/genomics/most-recent-collection-date-by-location?pangolin_lineage=b.1.1.7&location_id=USA_US-CA

## 6. Most recent submission date by location

Endpoint: https://api.outbreak.info/genomics/most-recent-submission-date-by-location

Parameters:

* `pangolin_lineage` (Required).
* `mutations` (Optional). Comma separated list of mutations.
* `location_id`  (Optional). If not specified, return most recent date globally.

Examples,

Most recent submission date of B.1.1.7 PANGO lineage globally.
https://api.outbreak.info/genomics/most-recent-submission-date-by-location?pangolin_lineage=b.1.1.7

Most recent submission date of B.1.1.7 PANGO lineage with S:E484K globally.
https://api.outbreak.info/genomics/most-recent-submission-date-by-location?pangolin_lineage=b.1.1.7&mutations=S:E484K

Most recent submission date of B.1.1.7 PANGO lineage in California
https://api.outbreak.info/genomics/most-recent-submission-date-by-location?pangolin_lineage=b.1.1.7&location_id=USA_US-CA

## 7. Get details of a mutation

Endpoint: https://api.outbreak.info/genomics/mutation-details

Parameters:
* `mutations` (Required). Comma separated list of mutations.

Examples,

Get details of S:E484K and S:N501Y
https://api.outbreak.info/genomics/mutation-details?mutations=S:E484K,S:N501Y

## 8. Get prevalence of a mutation across lineages per location

Endpoint: https://api.outbreak.info/genomics/mutations-by-lineage

Parameters

* `mutations` (Optional). List of mutations separated by `AND`.
* `location_id`  (Optional). If not specified, return most recent date globally.
* `pangolin_lineage` (Optional). If not specfied, returns all Pango lineages containing that mutation.
* `frequency` (Optional) Minimimum frequency threshold for the prevalence of a mutation in a lineage.

Examples,

Get prevalence of S:E484K across all lineages in the U.S.
https://api.outbreak.info/genomics/mutations-by-lineage?mutations=S:E484K&location_id=USA

## 9. Get prevalence of mutations in a lineage above a frequency threshold

Endpoint: https://api.outbreak.info/genomics/lineage-mutations

Parameters

* `pangolin_lineage` (Required). List of lineages separated by `OR`. List of mutations can be added as, `Lineage 1 OR Lineage 2 OR Lineage 3 AND Mutation 1 AND Mutation 2`. Mutiple queries can be separated by `,`.
* `frequency` (Optional, default: 0.8). A number between 0 and 1 specifying the threshold above which to return mutations.

Examples,

Get all mutations in A.27 lineage.
https://api.outbreak.info/genomics/lineage-mutations?pangolin_lineage=A.27

## 10. Return the daily lag between collection and submission dates by location

Endpoint: https://api.outbreak.info/genomics/collection-submission

Parameters:

* `location_id` (Optional). If not specified, return lag globally.

## 11. Match lineage name using wildcards.

Endpoint: https://api.outbreak.info/genomics/lineage

Parameters:

* `name` (Required). Supports wildcards.

Examples,

Get all lineages that start with b.1
https://api.outbreak.info/genomics/lineage?name=b.1.*

## 12. Match location name using wildcards.

Endpoint: https://api.outbreak.info/genomics/location

Parameters:

* `name` (Required). Supports wildcards.

Examples,

Get all locations that start with united
https://api.outbreak.info/genomics/location?name=united*

## 13. Get location details using ID.

Parameters:
* `id` (Required).

Examples,

Get location details using id: `USA_US-CA`
https://dev.outbreak.info/genomics/location-lookup?id=USA_US-CA

## 14. Match mutations using wildcards.

Endpoint: https://api.outbreak.info/genomics/mutations

Parameters:
* `name` (Required)

Examples,

Get all mutations that start with S:E484
https://api.outbreak.info/genomics/mutations?name=S:E484*

## 15. Get prevalence of all lineages over time for a location

Endpoint: https://api.outbreak.info/genomics/prevalence-by-location-all-lineages

Parameters:
* `location_id` (Required)
* `other_threshold` (Default: `0.05`) Minimum prevalence threshold below which lineages must be accumulated under "Other".
* `nday_threshold` (Default: `10`) Minimum number of days in which the prevalence of a lineage must be below `other_threshold` to be accumulated under "Other".
* `ndays` (Default: `180`) The number of days before the current date to be used as a window to accumulate linegaes under "Other".
* `other_exclude` Comma separated lineages that are NOT to be included under "Other" even if the conditions specified by the three thresholds above are met.
* `cumulative` (Default: `false`) If `true` return the cumulative prevalence.

Examples,

Give me the prevalence of all lineages in the U.S., classify lineages that are below 0.03 prevalence for atleast 5 days over the last 60 days as "Other", and exclude p.1 from "Other" even if conditions for "Other" are satisfied.
https://api.outbreak.info/genomics/prevalence-by-location-all-lineages?location_id=USA&other_threshold=0.03&nday_threshold=5&ndays=60&other_exclude=p.1

## 16. Get prevalence of each amino acid by codon number
Endpoint: https://api.outbreak.info/genomics/prevalence-by-position

Parameters:
* `name`: (required) Name of a gene:codon number, such as `S:484`
* `location_id` (optional)
* `pangolin_lineage` (optional)

Example: https://api.outbreak.info/genomics/prevalence-by-position?name=S:484&pangolin_lineage=B.1.526&location_id=USA_US-NY
