Compare the recommendations for various tactical voting sites for the UK 2024 General Election, to help check that they are aligned.

# Purpose

In this election, there are a number of tactical voting sites that make recommendations for the best candidate to vote for
to get the Tories out of power. These are not affiliated with any one party. They use several different approaches to make
their recommendations, such as polls, the results of the last election, and where parties are putting in effort.

Theoretically, their recommendations should all be aligned, but that's not always true.

This code aims to scrape the various different sites to assemble a unified spreadsheet of recommendations, highlighting
the inconsistencies, so the administrators of each site can check to see why they disagree and hopefully back a
single non-Tory candidate.

# Current differences between tactical voting sites

* Brighton Pavilion (E14001130): Stop the Tories has Green or Labour at https://stopthetories.vote/parl/brighton-pavilion, tactical.vote has Green at https://tactical.vote/brighton-pavilion/, tacticalvote.co.uk has Any at https://tacticalvote.co.uk/#BrightonPavilion
* Bristol Central (E14001131): Stop the Tories has Labour or Green at https://stopthetories.vote/parl/bristol-central, tactical.vote has Green at https://tactical.vote/bristol-central/, tacticalvote.co.uk has Any at https://tacticalvote.co.uk/#BristolCentral
* Hamilton and Clyde Valley (S14000092): Stop the Tories has Labour or SNP at https://stopthetories.vote/parl/hamilton-and-clyde-valley, tactical.vote has SNP at https://tactical.vote/hamilton-and-clyde-valley/, tacticalvote.co.uk has Any at https://tacticalvote.co.uk/#HamiltonClydeValley
* Livingston (S14000095): Stop the Tories has Labour or SNP at https://stopthetories.vote/parl/livingston, tactical.vote has SNP at https://tactical.vote/livingston/, tacticalvote.co.uk has Any at https://tacticalvote.co.uk/#Livingston
* Lothian East (S14000096): Stop the Tories has TBC at https://stopthetories.vote/parl/lothian-east, tactical.vote has SNP at https://tactical.vote/lothian-east/, tacticalvote.co.uk has Labour or SNP at https://tacticalvote.co.uk/#LothianEast
* Waveney Valley (E14001569): Stop the Tories has Green at https://stopthetories.vote/parl/waveney-valley, tactical.vote has Labour at https://tactical.vote/waveney-valley/, tacticalvote.co.uk has Green at https://tacticalvote.co.uk/#WaveneyValley

This excludes the many constituencies that are currently marked as TBC.

It also excludes constituencies where one or more sites have "Any", considering it a safe non-Tory seat, but others have a specific recommendation. 

# Sites covered

- tacticalvote.co.uk
- tactical.vote
- stopthetories.vote (note - currently scraping, but there are CSVs at https://stopthetories.vote/data - the filename changes regularly)
- getvoting.org (not yet - no recommendations yet, and not as clearly anti-Tory as the others)

# Data files
## constituencies.csv

Data format: 

    ONS ID of constituency,Name of constituency,Sample postcode

Data sources:
- ONS IDs and constituency names from https://www.doogal.co.uk/Constituency24CSV/
- Post codes from the various post code files beneath that - e.g. https://www.doogal.co.uk/Constituency24CSV/W07000081,
  processed to take the first active post code

# License

Data on constituencies is ultimately from the Office of National Statistics and covered 
by the Open Government License, and downloaded via Chris Bell at www.doogal.co.uk.

Code is copyright (C) 2024 Inigo Surguy

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.