
# archived functions

## jcdc

This is an archived function that was used to scrape the jones county docket.

```python
def jcdc_scraper(log_id, print_table=False):
    start_time, new_intakes, total_intakes = time.time(), 0, 0
    url = 'https://www.jonesso.com/roster.php'
    docket_pages = set()
    docket_pages.add(url)
    r = requests.get(url)
    if r.status_code != 200:
        print('jcdc website is still down')
        return False
    soup = BeautifulSoup(r.text, 'html.parser')
    for x in soup.find_all('a', class_='page_num'):
        page = urllib.parse.urljoin(url, x.get('href'))
        docket_pages.add(page)
    intakes = []
    for page in docket_pages:
        try:
            r = requests.get(page)
        except requests.ConnectionError as err:
            damn_it(err)
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        for x in soup.find_all('a'):
            link = x.get('href')
            if link is not None:
                if link.startswith('roster_view.php?booking_num'):
                    intakes.append(link)
    total_intakes = len(intakes)
    for x in intakes:
        this_dict = {'jail': 'jcdc', 'linking': ['recuLxs8EEAfHcYfd']}
        this_dict['link'] = f"https://www.jonesso.com/{x}"
        try:
            r = requests.get(this_dict['link'])
        except requests.ConnectionError as err:
            damn_it(err)
            continue
        this_dict['bk'] = x[-5:]
        this_dict['last_verified'] = (
            datetime.utcnow()
            .replace(tzinfo=timezone.utc)
            .strftime('%Y-%m-%d %H:%M')
        )
        soup = BeautifulSoup(r.text, 'html.parser').find(id='cms-content')
        data = []
        for string in soup.stripped_strings:
            data.append(str(string))
        this_dict['recent_text'] = '\n'.join(data[0: len(data) - 1])
        if 'Arresting Agency:' in data:
            raw_lea = data[1 + data.index('Arresting Agency:')]
        else:
            raw_lea = ''
        m = airtab.match('bk', this_dict['bk'], view='jcdc', fields='recent_text')
        if not m:
            this_dict['html'] = soup.prettify()
            get_name(data[data.index('Booking #:') - 1], this_dict)
            if 'Age:' in data:
                this_dict['intake_age'] = int(data[1 + data.index('Age:')])
            this_dict['sex'] = data[1 + data.index('Gender:')]
            if data[1 + data.index('Race:')] == 'I':
                this_dict['race'] = 'AI'
            else:
                this_dict['race'] = data[1 + data.index('Race:')]
            if raw_lea:
                this_dict['LEA'] = standardize.jcdc_lea(raw_lea)
            this_dict['DOI'] = datetime.strptime(
                data[1 + data.index('Booking Date:')], '%m-%d-%Y - %I:%M %p').strftime('%m/%d/%Y %I:%M%p')
            c = data[1 + data.index('Charges:')]
            if c.startswith('Note:'):
                this_dict['charge_1'] = ''
            else:
                this_dict['charge_1'] = c
            if 'Bond:' in data:
                this_dict['intake_bond_cash'] = data[1 + data.index('Bond:')]
            this_dict['img_src'] = f"https://www.jonesso.com/templates/jonesso.com/images/inmates/{this_dict['bk']}.jpg"
            image_url = {'url': this_dict['img_src']}
            attachments_array = []
            attachments_array.append(image_url)
            this_dict['PHOTO'] = attachments_array
            if this_dict['img_src'] == 'https://www.jonesso.com/common/images/pna.gif':
                this_dict['PIXELATED_IMG'] = attachments_array
            airtab.insert(this_dict, typecast=True)
            new_intakes += 1
        else:
            update_record(this_dict, soup, m, standardize.jcdc_lea, raw_lea)
    wrap_it_up('jcdc', start_time, new_intakes, total_intakes, log_id, print_table)
```

This is an archived function that was used translate the arresting LEA data from jcdc's syntax to a standardized syntax.

```python
def jcdc_lea(raw_lea):
    if raw_lea == "JONES COUNTY SHERIFF'S OFFICE":
        return 'JonesCntySD'
    if raw_lea in {'LAUREL POLICE DEPARTMENT', 'LA police'}:
        return 'LaurelPD'
    if raw_lea == 'ELLISVILLE POLICE DEPARTMENT':
        return 'EllisvillePD'
    if raw_lea in {'MDOC(200)', 'MISS. DEPT OF CORRECTIONS', 'DEPT OF CORR (MDOC)'}:
        return 'MDOC'
    if raw_lea in {
            'HIGHWAY PATROL',
            'MISSISSIPPI HIGHWAY PATROL',
            'MHP MS HIGHWAY PATROL(138)',
            'MISS. HWY PATROL',
    }:
        return 'MHP'
    if raw_lea == 'JONES COUNTY DRUG COURT':
        return 'JonesCntyDrugCt'
    if raw_lea == 'SANDERSVILLE POLICE DEPARTMENT':
        return 'SandersvillePD'
    if raw_lea in {'DEPT OF TRANS (MDOT)', 'MISS DEPT OF TRANSPORTATION'}:
        return 'MDOT'
    if raw_lea == 'LAMAR COUNTY':
        return 'LamarCntySD'
    if raw_lea == 'JONES COUNTY SCHOOLS':
        return 'JonesCntySchools'
    if raw_lea == 'JEFFERSON DAVIS SHERIFFS DEPT':
        return 'JeffDavisCntySD'
    if raw_lea in {'JCJC', 'JONES JR. COLLEGE'}:
        return 'JonesCntyJC'
    if raw_lea == 'FORREST COUNTY':
        return 'ForrestCntySD'
    if raw_lea == 'Bonding Company':
        return 'BondingCo'
    if raw_lea == 'LAUDERDALE COUNTY':
        return 'LauderdaleCntySD'
    if raw_lea.startswith('US MARSHAL') or raw_lea.startswith('USMARSHAL'):
        return 'USMarshals'
    if raw_lea == 'JUSTICE CT.':
        return 'JonesCntyJusticeCt'
    if raw_lea == 'MARION COUNTY':
        return 'MarionCntySD'
    if raw_lea in {'JASPER COUNTY', "JASPER COUNTY SHERIFF'S DEPT"}:
        return 'JasperCntySD'
    if raw_lea == 'HARRISON COUNTY':
        return 'HarrisonCntySD'
    if raw_lea == 'SOSO POLICE DEPARTMENT':
        return 'SosoPD'
    return raw_lea
```
