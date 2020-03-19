# !/usr/bin/env python3
"""These functions take the raw race or raw lea and standardizes them"""


def mcdc_lea(raw_lea):
    if raw_lea in {'MADISON SO', 'MCSO'}:
        return 'MadisonCntySD'
    if raw_lea.startswith('US MARSHAL') or raw_lea.startswith('USMARSHAL'):
        return 'USMarshals'
    if raw_lea == 'RIDGELAND PD':
        return 'RidgelandPD'
    if raw_lea == 'CANTON PD':
        return 'CantonPD'
    if raw_lea == 'MADISON PD':
        return 'MadisonPD'
    if raw_lea == 'VICKSBURG PD':
        return 'VicksburgPD'
    if raw_lea in {
            'HIGHWAY PATROL',
            'MISSISSIPPI HIGHWAY PATROL',
            'MHP MS HIGHWAY PATROL(138)',
            'MISS. HWY PATROL',
    }:
        return 'MHP'
    if raw_lea in {'MDOC(200)', 'MISS. DEPT OF CORRECTIONS', 'DEPT OF CORR (MDOC)'}:
        return 'MDOC'
    if raw_lea == 'FLORA PD':
        return 'FloraPD'
    if raw_lea == 'OTHER AGENCY/OVERNIGHT':
        return 'OtherLEA/Overnight'
    if raw_lea == 'WARREN SO':
        return 'WarrenCntySD'
    if raw_lea in {'MIKE BROWN', 'BRAD HARBOUR', 'JOHNNY SIMS', 'WILL WEISENBERGER'}:
        return 'MadisonCntyConstable'
    if raw_lea == 'US CUSTOMS':
        return 'CBP'
    if raw_lea == 'PARK RANGER':
        return 'ParkRangers'
    if raw_lea == 'PRV':
        return 'PearlRiverValley'
    if raw_lea == 'YAZOO SO':
        return 'YazooCntySD'
    if raw_lea == 'PEARL RIVER COUNTY':
        return 'PearlRiverCntySD'
    if raw_lea == 'NESHOBA SO':
        return 'NeshobaCntySD'
    if raw_lea == 'RICHLAND PD':
        return 'RichlandPD'
    if raw_lea == 'CHOCTAW SO':
        return 'ChoctawCntySD'
    if raw_lea == 'WASHINGTON SO':
        return 'WashingtonCntySO'
    if raw_lea in {'HCSO', 'HINDS SO'}:
        return 'HindsCntySD'
    if raw_lea == 'POPLARVILLE PD':
        return 'PoplarvillePD'
    if raw_lea == 'US POSTAL INSPECTOR':
        return 'USPostalInspector'
    if raw_lea == 'ROLLING FORK':
        return 'RollingForkPD'
    if raw_lea == 'PEARL PD':
        return 'PearlPD'
    if raw_lea == 'MS BUREAU OF NARCOTICS':
        return 'MBN'
    if raw_lea == 'PANOLA SO':
        return 'PanolaCntySD'
    if raw_lea == 'HOLMES COMMUNITY COLLEGE':
        return 'HolmesCC'
    if raw_lea == 'RANKIN SO':
        return 'RankinCntySD'
    return raw_lea


def prcdf_lea(raw_lea):
    if raw_lea == 'PEARL RIVER COUNTY':
        return 'PearlRiverCntySD'
    if raw_lea in {'MDOC(200)', 'MISS. DEPT OF CORRECTIONS', 'DEPT OF CORR (MDOC)'}:
        return 'MDOC'
    if raw_lea == 'POPLARVILLE PD':
        return 'PoplarvillePD'
    if raw_lea == 'PICAYUNE PD':
        return 'PicayunePD'
    if raw_lea in {
            'HIGHWAY PATROL',
            'MISSISSIPPI HIGHWAY PATROL',
            'MHP MS HIGHWAY PATROL(138)',
            'MISS. HWY PATROL',
    }:
        return 'MHP'
    if raw_lea == 'DRUG COURT':
        return 'DrugCt'
    if raw_lea == 'PRC CAMPUS POLICE':
        return 'PearlRiverCntyCampusPD'
    if raw_lea == 'MS BUREAU OF NARCOTICS':
        return 'MBN'
    if raw_lea == 'EXT TRAN OF AMER':
        return 'ExtTran'
    if raw_lea == 'LAMAR COUNTY':
        return 'LamarCntySD'
    if raw_lea in {'DEPT OF TRANS (MDOT)', 'MISS DEPT OF TRANSPORTATION'}:
        return 'MDOT'
    if raw_lea == 'PRCCC':
        return 'PearlRiverCntyCC'
    if raw_lea == 'HARRISON COUNTY':
        return 'HarrisonCntySD'
    return raw_lea


def tcdc_lea(raw_lea):
    if raw_lea == 'TCSO':
        return 'TunicaCntySD'
    if raw_lea == 'CITY':
        return 'TunicaPD'
    if raw_lea in {'MDOC(200)', 'MISS. DEPT OF CORRECTIONS', 'DEPT OF CORR (MDOC)'}:
        return 'MDOC'
    return raw_lea


def lcdc_lea(raw_lea):
    if raw_lea == 'TUPELO POLICE DEPARTMENT(107)':
        return 'TupeloPD'
    if raw_lea == "LEE COUNTY SHERIFF'S DEPARTMENT(100)":
        return 'LeeCntySD'
    if raw_lea in {
            'MDOC(200)',
            'MISS. DEPT OF CORRECTIONS',
            'DEPT OF CORR (MDOC)',
    }:
        return 'MDOC'
    if raw_lea in {
            'HIGHWAY PATROL',
            'MISSISSIPPI HIGHWAY PATROL',
            'MHP MS HIGHWAY PATROL(138)',
            'MISS. HWY PATROL',
    }:
        return 'MHP'
    if raw_lea == 'VERONA POLICE DEPARTMENT(108)':
        return 'VeronaPD'
    if raw_lea == 'SHANNON POLICE DEPARTMENT(106)':
        return 'ShannonPD'
    if raw_lea == 'BALDWYN POLICE DEPARTMENT(101)':
        return 'BaldwynPD'
    if raw_lea == 'SALTILLO POLICE DEPARTMENT(105)':
        return 'SaltilloPD'
    if raw_lea == 'GUNTOWN POLICE DEPARTMENT(102)':
        return 'GuntownPD'
    if raw_lea == 'NATCHEZ TRACE/US MARSHALL(400)':
        return 'NatchezTrace/USMarshals'
    if raw_lea == 'PLANTERSVILLE POLICE DEPARTMENT(104)':
        return 'PlantersvillePD'
    if raw_lea == 'Prisoner Trasport Service':
        return 'PrisonerTransportService'
    if raw_lea in {
            'TRIGG COUNTY KY',
            'TUSCALOOSA CO AL',
            'ALL OTHER STATES (SPECIFY)(700)',
    }:
        return 'OtherStateLEA'
    if raw_lea == 'NETTLETON POLICE DEPARTMENT(103)':
        return 'NettletonPD'
    if raw_lea.startswith('US MARSHAL') or raw_lea.startswith('USMARSHAL'):
        return 'USMarshals'
    if raw_lea == 'INMATE SERVICES CORPORATION':
        return 'InmateServicesCorp'
    if raw_lea == 'ALL OTHER MS AGENCYS (SPECIFY)(600)':
        return 'OtherLEA'
    if raw_lea == 'MANTACHIE':
        return 'MantachiePD'
    if raw_lea == 'NEW ALBANY':
        return 'NewAlbanyPD'
    if raw_lea == "ITAWAMBA COUNTY SHERIFF'S DEPT.(112)":
        return 'ItawambaCntySD'
    if raw_lea == 'SHERMAN POLICE DEPARTMENT(139)':
        return 'ShermanPD'
    if raw_lea == 'SECURITY TRANSPORT SERVICES, INC':
        return '"Security Transport Services, Inc."'
    return raw_lea


def hcdc_lea(raw_lea):
    if raw_lea == 'JPD':
        return 'JacksonPD'
    if raw_lea in {'HCSO', 'HINDS SO', 'HSCO'}:
        return 'HindsCntySD'
    if raw_lea in {'MDOC(200)', 'MISS. DEPT OF CORRECTIONS', 'DEPT OF CORR (MDOC)', 'MISSISSIPPI DEPT OF CORRECTIONS'}:
        return 'MDOC'
    if raw_lea == 'CPD':
        return 'ClintonPD'
    if raw_lea in {'BYPD', 'BRYA', 'BYRA'}:
        return 'ByramPD'
    if raw_lea == 'UMC':
        return 'UMMC'
    if raw_lea in {
            'HIGHWAY PATROL', 'MISSISSIPPI HIGHWAY PATROL', 'MHP MS HIGHWAY PATROL(138)', 'MISS. HWY PATROL', 'MHP -G'}:
        return 'MHP'
    if raw_lea == 'MS BUREAU OF NARCOTICS':
        return 'MBN'
    if raw_lea == 'RPD':
        return 'RaymondPD'
    if raw_lea == 'EPD':
        return 'EdwardsPD'
    if raw_lea in {'MADISON SO', 'MCSO'}:
        return 'MadisonCntySD'
    if raw_lea == 'JPS':
        return 'JacksonSchools'
    if raw_lea in {'TERR', 'TPD'}:
        return 'TerryPD'
    if raw_lea == 'UPD':
        return 'UticaPD'
    if raw_lea == 'HCCC':
        return 'HindsCntyCC'
    return raw_lea


def ccdc_lea(raw_lea):
    if raw_lea == 'CLAY COUNTY SHERIFFS OFFICE':
        return 'ClayCntySD'
    if raw_lea == 'WEST POINT POLICE DEPARTMENT':
        return 'WestPointPD'
    if raw_lea in {'MDOC(200)', 'MISS. DEPT OF CORRECTIONS', 'DEPT OF CORR (MDOC)'}:
        return 'MDOC'
    return raw_lea


def jcj_lea(raw_lea):
    if raw_lea in {'JASPER COUNTY', "JASPER COUNTY SHERIFF'S DEPT"}:
        return 'JasperCntySD'
    if raw_lea == 'BAY SPRINGS POLICE DEPT.':
        return 'BaySpringsPD'
    if raw_lea in {'HIGHWAY PATROL', 'MISSISSIPPI HIGHWAY PATROL', 'MHP MS HIGHWAY PATROL(138)', 'MISS. HWY PATROL'}:
        return 'MHP'
    if raw_lea == "ATTORNEY GENERAL'S OFFICE":
        return 'AGO'
    if raw_lea == 'LAUREL POLICE DEPT':
        return 'LaurelPD'
    if raw_lea == 'HEIDELBURG POLICE DEPT':
        return 'HeidelburgPD'
    if raw_lea == 'MISSISSIPPI DEPT OF CORRECTIONS':
        return 'MDOC'
    return raw_lea


def jcadc_lea(raw_lea):
    if raw_lea == 'MSATTGEN':
        return 'AG'


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


def mcdc_race(raw_race):
    if raw_race == 'BLACK':
        return 'B'
    if raw_race == 'WHITE':
        return 'W'
    if raw_race == 'HISPANIC':
        return 'H'
    if raw_race == 'ASIAN IS':
        return 'AS'
    if raw_race == 'AMERICAN':
        return 'NA'
    if raw_race == 'OTHER':
        return 'O'
    return raw_race


def prcdf_race(raw_race):
    if raw_race == 'BLACK':
        return 'B'
    if raw_race == 'BLACK':
        return 'B'
    if raw_race == 'WHITE':
        return 'W'
    if raw_race == 'HISPANIC':
        return 'H'
    if raw_race == 'ASIAN':
        return 'AS'
    if raw_race == 'INDIAN':
        return 'NA'
    if raw_race == 'OTHER':
        return 'O'
    if raw_race == 'UNKNOWN':
        return 'U'
    return raw_race


def kcdc_race(raw_race):
    if raw_race == 'African American':
        return 'B'
    if raw_race == 'Caucasian':
        return 'W'
    if raw_race == 'Hispanic':
        return 'H'
    if raw_race == 'Native American':
        return 'NA'
    if raw_race == 'Other':
        return 'O'
    return raw_race


def lcdc_race(raw_race):
    if raw_race == 'Caucasian':
        return 'W'
    if raw_race == 'African American':
        return 'B'
    if raw_race == 'Hispanic':
        return 'H'
    if raw_race == 'Asian':
        return 'AS'
    if raw_race == 'Native American':
        return 'NA'
    if raw_race == 'Other':
        return 'O'
    return raw_race


def ccdc_race(raw_race):
    if raw_race == 'BLACK':
        return 'B'
    if raw_race == 'WHITE':
        return 'W'
    if raw_race == 'Native Haw':
        return 'NHPI'
    if raw_race == 'INDIAN (NA':     # CCSO0000038538
        return 'NA'
    if raw_race == 'UNKNOWN':     # CCSO0000038253
        return 'U'
    return raw_race
