# summary

About once every hour, a python script scrapes the online jail dockets for nine separate county jails in Mississippi.
When a booking is detected for the first time, a pdf is created and uploaded to documentcloud.org, and the raw data is programatically entered into the Airtable base.
The script also keeps track of how long people are listed on the jail dockets to calculate approximate lengths of incarceration.
A more precise figure for length of incarceration is available for five of the ten jails, for which exact datetimes of release (`DOR`) are provided.
Occassionally, the initial booking data is updated, and the scraper will update the Airtable accordingly, but a new pdf is not generated for every version of the intake sheet.

## jails scraped

jail | abreviation | start date | end date
---|---|---|---
Madison County Detention Center | `mcdc` | Sep. 6, 2018 | present
Pearl River County Detention Facility | `prcdf` | Sep. 6, 2018 | present
Lee County Detention Center | `lcdc` | Dec. 1, 2018 | present
Jones County Detention Center | `jcdc` | Dec. 14, 2018 | Nov. 1, 2019
Hinds County Detention Center | `hcdc` | Dec. 28, 2018 | present
Kemper County Detention Center | `kcdc` | Apr. 6, 2019 | present
Tunica County Detention Center | `tcdc` | Apr. 6, 2019 | present
Adams County Detention Center | `acdc` | May 25, 2019 | present
Clay County Detention Center | `ccdc` | May 24, 2019 | present
Jasper County Jail | `jcj` | Jun. 3, 2019 | present

As of Nov. 27, the Airtable base includes data for 6,554 mcdc admissions, 1,659 prcdf admissions, 5,107 lcdc admissions, 2,260 jcdc admissions, 3,616 hcdc admissions, 1,128 kcdc admissions, 617 tcdc admissions, 562 ccdc admissions, 770 acdc admissions, and 345 jcj admissions.

As of Nov., 2019: Only a fraction of the data is provided via the links at [bfeldman89.com/projects/jails](https://bfeldman89.com/projects/jails). Once I get all the data cleaned and the incarcerated arrestees anonymized to a degree I'm comfortable with, I'll post a lot more of the data (e.g., charge(s), bond, arresting agency). If you are a journalist, activist, or civil rights attorney interested in the data, email me.

## field descriptions

field | description | formula
---|---|---
`UID` | unique ID |
`bk` | Most jails' intake sheets have an explicit booking number field, but the numbers for LCDC, JCDC and HCDC are not booking numbers per se. Unlike,  MCDC & PRCDF, however, LCDC, JCDC and HCDC do not shuffle intakes among a fixed number of url addresses. Rather, each inmate, has a unique url. The numbers are the unique parameter from the intake urls. |
`intake_number` | There is a longer booking number for each intake at MCDC & PRCDF, which allows for independant bookings of the same individual to be documented clearly.  LCDC intake sheets have a 'Booking #' field, and an `intake_number` is constructed by combining `bk` with that number. |
`intake_case_number` | only exists for mcdc & prcdf |
`first name` | first name |
`last name` | last name |
`middle name` | middle name |
`suffix` | suffix |
`charge_1` | The first charge listed isn't necessarily meaningful, but mcdc & prcdf include the MS code section for the top charge, which is then parsed into `charge_1_statute` and `charge_1_title` |
`charge_1_statute` | the code section for the top charge for mcdc & prcdf intakes |
`charge_1_title` | the title of the top charge |
`charges` | all charges listed on the most recent version of intake sheet |
`charge(s)` | unfortunately, these are not yet standardized. In the full dataset, there are over a thousand unique charges, but that includes stylistic differences of substatively identical charges. Also, this field does not include multiple counts of the same charge. For instance, someone charged with three counts of 'Conspiracy' would only have 'Conspiracy' listed once in this field. |
`total charges` | the count of items in the `charge(s)` field |
`LEA` | a standardized version of the arresting agency (e.g., the raw data 'HIGHWAY PATROL', 'MISSISSIPPI HIGHWAY PATROL', 'MHP MS HIGHWAY PATROL(138)', and 'MISS. HWY PATROL' have been standardized as 'MHP') |
`COURT` | the court exercising jurisdiction (only provided by mcdc & prcdf) |
`link` | the most recently provided url to the intake sheet on the county docket's website. The link for most intakes are constant, but be cautious with using the links for mcdc and prcdf. The link should usually point to the accurate intake sheet bc the scraper not only updates incarceration status each hour, but also updates the`link` and `img_src` fields if they've changed. |
`html` | the html of the most recent version of intake sheet |
`recent_text` | the plain text of the most recent version of intake sheet |
`PDF` | the url for a pdf of the initial version of the intake sheet | ```IF(NOT(dc_id=''), "https://assets.documentcloud.org/documents/" & SUBSTITUTE(dc_id, '-', '/', 1) & ".pdf")```
`dc_full_text` | the full text from the pdf of the initial version of the intake sheet |
`pixelated url` | url to be uploaded for `PIXELATED_IMG` | ```IF(jail = "jcdc", "https://res.cloudinary.com/bfeldman89/image/upload/e_pixelate_faces:8/" & UID & ".jpg",
IF(jail = "mcdc", "https://res.cloudinary.com/bfeldman89/image/upload/e_pixelate_faces:20/o_45/" & UID & ".jpg",
IF(jail = "prcdf", "https://res.cloudinary.com/bfeldman89/image/upload/e_pixelate_faces:15/o_60/" & UID & ".jpg",
IF(jail = "lcdc", "https://res.cloudinary.com/bfeldman89/image/upload/e_pixelate_faces:13/o_80/" & UID & ".jpg",
IF(jail = "ccdc", "https://res.cloudinary.com/bfeldman89/image/upload/e_pixelate_faces:5/" & UID & ".jpg",
IF(jail = "acdc", "https://res.cloudinary.com/bfeldman89/image/upload/e_pixelate_faces:10/" & UID & ".jpg", IF(jail = "jcj", "https://res.cloudinary.com/bfeldman89/image/upload/e_pixelate_faces:10/o_75/" & UID & ".jpg",
"https://res.cloudinary.com/bfeldman89/image/upload/e_pixelate_faces:16/o_90/" & UID & ".jpg")))))))```
`PIXELATED_IMG` | a translucent, pixelated version of the "mugshot" |
`AGE` | the age provided by the most recent version of the intake sheet (the current age of the incarcerated individual) | ```IF(jail = 'hcdc', DATETIME_DIFF(NOW(), DATETIME_PARSE(DOB), 'years'), intake_age)```
`DOB` | date of birth (only provided by mcdc, prcdf, lcdc, and hcdc) |
`age at time of arrest` | the age at the time of arrest (only available for intakes that include `DOB`) | ```IF(DOB != '', DATETIME_DIFF(DOI, DOB, 'years'))```
`DOI` | date of intake |
`DOO` | date of offense (only provided by mcdc & prcdf) |
`DOR` | date of release (only provided by jcdc, kcdc, tcdc, ccdc, and jcj) |
`initial_scrape` | the datetime of the initial scrape |
`last_verified` | the datetime of the most recent instance that the scraper detected tbe intake sheet on the online docket. every hour, the script runs, and if the individual is still listed on the docket, this field is updated, which allows for `DAYS_INCARCERATED` to be calculated and `currently_incarcerated` to be maintained. |
`hours_incarcerated` | the calculated number of hours the individual has been incarcerated. If the intake sheet provides a date of release (`DOR`), this is the time difference between the `DOR` and date of intake (`DOI`). Otherwise, it is the difference between the datetime the intake was last identified on the county docket and the `DOI`. | ```IF(NOT(DOR = ''), DATETIME_DIFF(DOR, DOI, 'hours'), DATETIME_DIFF(SET_TIMEZONE(last_verified, 'America/Chicago'), DOI, 'hours'))```
`days_incarcerated` | the calculated number of days the individual has been incarcerated. If the intake sheet provides a date of release (`DOR`), this is the difference between the `DOR` and date of intake (`DOI`). Otherwise, it is the difference between the datetime the intake was last identified on the county docket and the `DOI`. | ```IF(hours_incarcerated = '-23.0', VALUE('0.0'), IF(hours_incarcerated != '', hours_incarcerated / 24))```
`scheduled_release_date` | occassionally provided by lcdc, suggesting the detention is not pretrial |
`sex` | standardized sex categories (M (male) or F (female)) |
`race` | standardized race categories (W (white), AI (indigenous), AS (Asian), B (Black), H (Hispanic), O (other), and U (unknown)) |
`intake_hair` | |
`intake_eye` | |
`intake_compl` | |
`intake_height` | |
`intake_weight` | |
`glasses` | only provided by lcdc |
`intake_bond_written` | |
`intake_bond_cash` | |
`intake_fine_ammount` | |
`bond_ammounts` | |
`fine_ammounts` | |
`intake_address_line_1` | only provided by hcdc |
`intake_address_line_2` | only provided by hcdc |
`intake_pin` | only provided by hcdc |
`intake_cell` | only provided by hcdc |
`intake_section` | only provided by hcdc |
`intake_location` | only provided by hcdc |
`intake_pod` | only provided by hcdc |
`status` | | ```IF(DATETIME_DIFF(NOW(), {last_verified}, 'hours') <= 12, '✔️✔️✔️✔️', IF(DATETIME_DIFF(NOW(), {last_verified}, 'hours') <= 24, '✔️✔️✔️', IF(DATETIME_DIFF(NOW(), {last_verified}, 'days') <= 7, '✔️✔️',
IF(DATETIME_DIFF(NOW(), {last_verified}, 'days') <= 30, '✔️',
'❌'))))```
`blurb` | |
