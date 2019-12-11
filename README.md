# jail scrapers

## summary

Every hour at 15min past the hour, `scrapers.py` scrapes the online jail dockets for ten separate county jails and programmatically enters the raw data into an Airtable base. `scrapers.py` imports functions from the `standardization.py` module that are designed to standardize the LEA and race across jails.

When an intake sheet is detected for the first time, not only is the data entered into the Airtable base, but also `web_to_pdf.py` creates a pdf of the intake sheet, and `pdf_to_dc.py` uploads that pdf to documentcloud.org. Every four hours, `polish_data.py` performs several functions to automate a lot of data cleaning. Once per day, `snapshot.py` runs to record the total admissions and the total jail population per jail for the day.

`scrapers.py` also keeps track of how long people are listed on the jail dockets to calculate approximate lengths of incarceration. A more precise figure for length of incarceration is available for five of the ten jails, for which exact datetimes of release (`DOR`) are provided. Occasionally, the initial booking data is updated, and although `scrapers.py` will update the Airtable base accordingly, a new pdf is not generated for every version of the intake sheet. For example, if someone is booked for a DUI, and the next morning, the charges are updated to include a reckless driving charge, the Airtable base will reflect the updated charges, but the pdf will be a timestamped snapshot of the initial intake sheet.

## jails scraped

| jail                                  | abbreviation | started scraping | discontinued scraping |
|---------------------------------------|-------------|------------------|-----------------------|
| Madison County Detention Center       | `mcdc`    | Sep. 6, 2018     | present               |
| Pearl River County Detention Facility | `prcdf`   | Sep. 6, 2018     | present               |
| Lee County Detention Center           | `lcdc`    | Dec. 1, 2018     | present               |
| Jones County Detention Center         | `jcdc`    | Dec. 14, 2018    | Nov. 1, 2019*         |
| Hinds County Detention Center         | `hcdc`    | Dec. 28, 2018    | present               |
| Kemper County Detention Center        | `kcdc`      | Apr. 6, 2019     | present               |
| Tunica County Detention Center        | `tcdc`      | Apr. 6, 2019     | present               |
| Adams County Detention Center         | `acdc`      | May 25, 2019     | present               |
| Clay County Detention Center          | `ccdc`      | May 24, 2019     | present               |
| Jasper County Jail                    | `jcj`       | Jun. 3, 2019     | present               |
| Jackson County Adult Detention Center | `jcadc`     | Dec. 2, 2019     | present               |

\* Since Nov. 1, 2019, the Jones County Sheriff's Office website has been down.

As of Nov. 27, the Airtable base included data for 6,555 `mcdc` admissions, 1,661 `prcdf` admissions, 5,119 `lcdc` admissions, 2,260 `jcdc` admissions, 3,616 `hcdc` admissions, 1,128 `kcdc` admissions, 672 `tcdc` admissions, 563 `ccdc` admissions, 772 `acdc` admissions, and 345 `jcj` admissions.

## access to the data

At this time, only a fraction of the data is provided at [bfeldman89.com](https://bfeldman89.com/projects/jails). Once I get all the data cleaned and the incarcerated arrestees anonymized to a degree I'm comfortable with, I'll post a lot more of the data (e.g., charge(s), bond, arresting agency). **If you are a journalist, activist, or civil rights attorney interested in the data, let me know via [email](mailto:bfeldman89@pm.me) or [DM](https://twitter.com/messages/compose?recipient_id=2163941252).** It's easy for me to share links to the airtable, but if you are interested in downloading the data, please provide your github username in the email, and I will invite you to a private repository with the csv files. If you don't already have a github account, you can create a free account at https://github.com/join.

## what about the other ~70 county jails in the state

Not all sheriffs make the jail docket publicly available via the county website. Of the dockets that are online, a lot of them are designed in a way that hinders scraping. That said, there are absolutely more jail dockets in Mississippi that can be scraped, and I'm happy to help if someone takes the lead. It isn't yet complete, but a table with more info about each county's docket is available [here](https://airtable.com/shrQaYBSCpTvNpqhn).

The remainder of this README documents and defines the fields in the Airtable base.

### fields

field | field type | description
---|---|---
`UID`| formula<sup>[1](#UID)</sup> | unique ID
`uid_for_humans`| formula<sup>[2](#uid_for_humans)</sup> | unique id composed of first initial, last name and date of incarceration (e.g., "S. SMITH 2019-11-16")
`jail` | single select | `mcdc`, `prcdf`, `lcdc`, `jcdc`, `hcdc`, `kcdc`, `tcdc`, `acdc`, `ccdc`, or `jcj`
`bk` | single line text | Most jails' intake sheets have an explicit booking number field, but the `bk` for `lcdc` is extracted from the unique intake url parameter, `iid`. For example, the `bk` for an intake sheet available at `https://tcsi-roster.azurewebsites.net/InmateInfo.aspx?i=26&code=Lee&type=roster&iid=283176` would be `283176`.
`intake_number` | single line text | There is a longer booking number for each intake at `mcdc` & `prcdf`, which allows for independent bookings of the same individual to be documented clearly. `lcdc` intake sheets have a "Booking #" that indicates how many times the individual has been booked into the jail before, and an `intake_number` is constructed by combining `bk` with that number.
`intake_case_number` | single line text | This only exists for intakes on the `mcdc` & `prcdf` dockets. It can be helpful for requesting incident reports via the MS Pub. Records Act.
`dc_id` | single line text | the unique documentcloud id. The `dc_id` is used to formulate the `PDF` and `dc_canonical_url` fields.
`link` | url | the most recently provided url to the intake sheet on the county docket's website. The link for most intakes are constant, but be cautious with using the links for `mcdc` and `prcdf`. The link should usually point to the accurate intake sheet bc the scraper not only updates incarceration status each hour, but also updates the`link` and `img_src` fields if they've changed.
`html` | long text | the html of the most recent version of intake sheet
`recent_text` | long text | the plain text of the most recent version of intake sheet
`PDF`| formula<sup>[3](#PDF)</sup> | the url for a pdf of the initial version of the intake sheet
`dc_canonical_url` | formula<sup>[4](#dc_canonical_url)</sup> | the url for the canonical documentcloud url for the initial version of the intake sheet
`dc_title` | single line text | the title of the pdf uploaded to documentcloud
`dc_pages`| number | the number of pages of the documentcloud pdf
`dc_access` | single select | public, private, pending, or error
`dc_full_text` | long text | the full text from the pdf of the initial version of the intake sheet
`initial_scrape` | datetime | the datetime of the initial scrape
`DOA` | datetime | the date of arrest (only provided for `jcadc`)
`DOI` | datetime | date of intake
`DOO` | datetime | date of offense (only provided for `mcdc` & `prcdf`)
`DOR` | datetime | date of release (only provided for `jcdc`, `kcdc`, `tcdc`, `ccdc`, and `jcj`)
`SDOR` | datetime | scheduled date of release (only provided for `lcdc`)
`last_verified` | datetime | the datetime of the most recent instance that the scraper detected the intake sheet on the online docket. This field is used to calculate `status`, and -- for intakes that lack an explicit `DOR` -- it is also used to calculate `days_incarcerated` and `hours_incarcerated`.
`status_verbose` | formula<sup>[5](#status)</sup> |  ✔️✔️✔️✔️ (was identified on the docket w/in the last 12 hours), ✔️✔️✔️ (24 hours), ✔️✔️ (7 days), ✔️ (30 days), or ❌ (31+ days)
`days_incarcerated`| formula<sup>[6](#days_incarcerated)</sup> | the calculated number of days the individual has been incarcerated. If the intake sheet provides a date of release (`DOR`), this is the difference between the `DOR` and date of intake (`DOI`). Otherwise, it is the difference between the datetime the intake was last identified on the county docket and the `DOI`.
`hours_incarcerated`| formula<sup>[7](#hours_incarcerated)</sup> | the calculated number of hours the individual has been incarcerated. If the intake sheet provides a date of release (`DOR`), this is the time difference between the `DOR` and date of intake (`DOI`). Otherwise, it is the difference between the datetime the intake was last identified on the county docket and the `DOI`.
`SDOR` | datetime | occasionally provided by `lcdc`, seemingly indicating the detention is not pretrial
`first_name` | single line text | first name extracted from the full name via [nameparser](https://pypi.org/project/nameparser/)
`middle_name` | single line text | middle name extracted from the full name via [nameparser](https://pypi.org/project/nameparser/)
`suffix` | single line text | suffix extracted from the full name via [nameparser](https://pypi.org/project/nameparser/)
`DOB` | datetime | date of birth (only provided by `mcdc`, `prcdf`, `lcdc`, and `hcdc`)
`intake_age`| number | every jail except `hcdc` provides the incarcerated person's age. This field represents the incarcerated person's current age (rather than age at the time of booking)
`age_at_time_of_arrest`| formula<sup>[8](#age_at_time_of_arrest)</sup> | the age at the time of arrest (only available for intakes that include `DOB`)
`AGE` | formula<sup>[9](#AGE)</sup> | the age provided by the most recent version of the intake sheet (the current age of the incarcerated individual)
`sex` | single select | M (male) or F (female)
`race` | single select | W (white), AI (indigenous), AS (Asian), B (Black), H (Hispanic), O (other), and U (unknown)
`intake_hair` | single line text |
`intake_eye` | single line text |
`intake_compl` | single line text |
`intake_height` | single line text |
`intake_weight` | single line text |
`glasses` | single select | only provided by `lcdc`
`intake_address_line_1` | single line text | only provided by `hcdc`
`intake_address_line_2` | single line text | only provided by `hcdc`
`intake_pin` | single line text | only provided by `hcdc`
`intake_cell` | single line text | only provided by `hcdc`
`intake_section` | single line text | only provided by `hcdc`
`intake_location` | single line text | only provided by `hcdc`
`intake_pod` | single line text | only provided by `hcdc`
`charge_1` | single line text | The first charge listed isn't necessarily meaningful, but `mcdc` & `prcdf` include the code section for the top charge, which is then parsed into `charge_1_statute` and `charge_1_title`
`charge_1_title` | single line text | the title of the top charge
`charge_1_statute` | single select | the code section for the top charge for `mcdc` & `prcdf` intakes
`charges` | long text | all charges listed on the most recent version of intake sheet
`charge(s)` | multiple select | unfortunately, these are not yet standardized. In the full dataset, there are over 2,000 unique charges, but that includes stylistic differences of substantively identical charges. Also, this field does not include multiple counts of the same charge. For instance, someone charged with three counts of 'Conspiracy' would only have 'Conspiracy' listed once in this field.
`charge_classifications` | long text | the classification (e.g., misdemeanor or felony) for each charge listed. This datapoint is only provided by some jails, and until the charges have been standardized, it is only provided if provided by the jail docket itself.
`total_charges` | count | the count of items in the `charge(s)` field
`LEA` | single line text | a standardized version of the arresting agency (e.g., the raw data 'HIGHWAY PATROL', 'MISSISSIPPI HIGHWAY PATROL', 'MHP MS HIGHWAY PATROL(138)', and 'MISS. HWY PATROL' have been standardized as 'MHP'). This has narrowed the number of unique LEAs down to [154](https://airtable.com/shrCgqWuMFH54ePVx).
`courts` | single line text | the court exercising jurisdiction (only provided by `mcdc` & `prcdf`). By standardizing data for this field (accounting for stylistic differences between `mcdc` & `prcdf`), the number of unique courts is narrowed to [12](https://airtable.com/shrIHbiAyOTDArn8l).
`intake_bond_written` | currency | only provided by `mcdc` & `prcdf`
`intake_bond_cash` | currency | only provided by `mcdc`, `prcdf`, `lcdc`, `jcdc`, `tcdc`, `acdc`, and `ccdc`
`bond_ammounts` | long text | itemized bond amounts, only provided by `mcdc`, `prcdf`, and `lcdc`
`intake_fine_ammount` | currency | only provided by `lcdc`
`fine_ammounts` | long text | itemized fine amounts, only provided by `lcdc`
`img_src` | url | mugshot url (In May 2019, `lcdc` [stopped posting mugshots](https://www.wcbi.com/lee-county-ends-practice-posting-mugshots) bc of the negative consequences for defendants)
`pixelated_url`| formula<sup>[10](#pixelated_url)</sup> | url to be uploaded for `PIXELATED_IMG`
`PIXELATED_IMG` | attachment | a translucent, pixelated version of the "mugshot"
`issue(s)` | multiple select |a field for flagging an issue presented by the record.
`blurb` | formula<sup>[11](#blurb)</sup> | summary for humans
`total_admissions_filter` | formula<sup>[12](#total_admissions_filter)</sup> | specifies whether the date of intake predates the date the scraper began scraping the respective jail. In other words, it allows for filtering out the intakes from dates for which we do not have complete admission data.

___

### Airtable formulas

#### UID

```Airtable
IF(jail='ccdc', bk,
IF(jail='jcadc', SUBSTITUTE(LOWER(bk), 'c0', 'c_0'),
jail & '_' &
IF(AND(LEN(bk) = 12, LEN(intake_number) = 18), SUBSTITUTE(SUBSTITUTE(intake_number, ' - ', '_'), 'BK', ''),
IF(AND(LEN(bk) = 12, intake_number = ''), SUBSTITUTE(bk, 'BK', '') & '_xxx',
IF(LEN(bk) = 10, bk,
IF(LEN(bk) = 7, '000' & bk,
IF(LEN(bk) = 6, '0000' & bk,
IF(LEN(bk) = 5, '00000' & bk,
IF(LEN(bk) = 4, '000000' & bk,
IF(LEN(bk) = 3, '0000000' & bk,
IF(LEN(bk) = 2, '00000000' & bk, '')))))))))))
```

#### uid_for_humans

```Airtable
UPPER(LEFT({first_name}, 1)) & '. ' & UPPER({last_name}) & ' ' & DATETIME_FORMAT(DOI, 'YYYY-MM-DD')
```

#### PDF

```Airtable
IF(NOT(dc_id=''), "https://assets.documentcloud.org/documents/" & SUBSTITUTE(dc_id, '-', '/', 1) & ".pdf")
```

#### dc_canonical_url

```Airtable
IF(dc_id = "", "", "https://www.documentcloud.org/documents/" & dc_id & ".html")
```

#### status

```Airtable
IF(DATETIME_DIFF(NOW(), {last_verified}, 'hours') < 12,
   '1. verified less than 12 hours ago',
   IF(DATETIME_DIFF(NOW(), {last_verified}, 'hours') <= 24,
      '2. last verified 12-24 hours ago',
      IF(DATETIME_DIFF(NOW(), {last_verified}, 'days') <= 7,
         '3. last verified 1-7 days ago',
         IF(DATETIME_DIFF(NOW(), {last_verified}, 'days') <= 30,
            '4. last verified 8-30 days ago',
            '5. last verified more than 30 days ago'))))
```

#### days_incarcerated

```Airtable
IF(hours_incarcerated = '-23.0',
   VALUE('0.0'),
   IF(hours_incarcerated != '',
   hours_incarcerated / 24)
   )
```

#### hours_incarcerated

```Airtable
IF(NOT(DOR = ''),
   DATETIME_DIFF(DOR,
                 DOI,
                 'hours'),
   DATETIME_DIFF(SET_TIMEZONE(last_verified, 'America/Chicago'),
                 DOI,
                 'hours')
    )
```

#### age_at_time_of_arrest

```Airtable
IF(DOB != '',
   DATETIME_DIFF(DOI, DOB, 'years')
   )
```

#### AGE

```Airtable
IF(jail = 'hcdc',
   DATETIME_DIFF(NOW(), DATETIME_PARSE(DOB), 'years'),
   intake_age)
```

#### pixelated_url

```Airtable
"https://res.cloudinary.com/bfeldman89/image/upload/e_pixelate_faces:" &
IF(jail = "mcdc", "20/o_45/",
IF(jail = "prcdf", "15/o_60/",
IF(jail = "lcdc", "13/o_80/",
IF(jail = "ccdc", "5/",
IF(jail = "acdc", "10/",
IF(jail = "jcj", "10/o_75/",
IF(jail = "jcadc", "11/o_45/",
"16/o_90/"))))))) & UID & ".jpg"
```

#### blurb

```Airtable
SUBSTITUTE(
    SUBSTITUTE(
        SUBSTITUTE(
            CONCATENATE(
                "On ",
                DATETIME_FORMAT(DOI, 'MMM. D, YYYY'),
                ", a ",
                AGE,
                "yo ",
                SWITCH(race, "W", "white ", "B", "Black ", "AS", "Asian ","H", "Latinx ","AI", "Native American"),
                SWITCH(sex, 'M', 'man', 'F', 'woman'),
                " was jailed at ",
                UPPER(jail),
                ". ",
                IF(
                    status != '✔️✔️✔️✔️',
                    CONCATENATE(
                        "The docket indicated ",
                        SWITCH(sex, 'M', 'he', 'F', 'she'),
                        " was incarcerated for ",
                        ROUND({days_incarcerated}, 1),
                        " days."
                    ),
                    CONCATENATE(
                        "As of ",
                        DATETIME_FORMAT(SET_TIMEZONE(last_verified, 'America/Chicago'), 'MMM. D, YYYY'),
                        ", ",
                        SWITCH(sex, 'M', 'he', 'F', 'she'),
                        " is still in jail.")
                    )
                ), " 1 days", " 1 day"),
        'May. ', 'May '),
    "a 18", "an 18")
```

#### total_admissions_filter

```Airtable
IF(AND(jail='hcdc', DATETIME_DIFF(DOI, DATETIME_PARSE('2018-12-28'), 'days') >= 0), 'booked during jail scraper project',
IF(AND(jail='kcdc', DATETIME_DIFF(DOI, DATETIME_PARSE('2019-04-06'), 'days') >= 0), 'booked during jail scraper project',
IF(AND(jail='tcdc', DATETIME_DIFF(DOI, DATETIME_PARSE('2019-04-06'), 'days') >= 0), 'booked during jail scraper project',
IF(AND(jail='jcdc', DATETIME_DIFF(DOI, DATETIME_PARSE('2018-12-14'), 'days') >= 0), 'booked during jail scraper project',
IF(AND(jail='mcdc', DATETIME_DIFF(DOI, DATETIME_PARSE('2018-09-06'), 'days') >= 0), 'booked during jail scraper project',
IF(AND(jail='prcdf', DATETIME_DIFF(DOI, DATETIME_PARSE('2018-09-06'), 'days') >= 0), 'booked during jail scraper project',
IF(AND(jail='lcdc', DATETIME_DIFF(DOI, DATETIME_PARSE('2018-12-01'), 'days') >= 0), 'booked during jail scraper project',
IF(AND(jail='acdc', DATETIME_DIFF(DOI, DATETIME_PARSE('2019-05-25'), 'days') >= 0), 'booked during jail scraper project',
IF(AND(jail='ccdc', DATETIME_DIFF(DOI, DATETIME_PARSE('2019-05-24'), 'days') >= 0), 'booked during jail scraper project',
IF(AND(jail='jcj', DATETIME_DIFF(DOI, DATETIME_PARSE('2019-06-02'), 'days') >= 0), 'booked during jail scraper project',
'booked prior to project'))))))))))
```
