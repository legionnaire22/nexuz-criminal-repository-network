"""
generate_firs.py
Creates all synthetic FIR text files for 3 cases.
Run: python generate_firs.py
Output: nexus/data/raw/firs/
"""
import os

BASE = r"c:\Users\sudee\Desktop\SIH New\nexus\data\raw\firs"
os.makedirs(BASE, exist_ok=True)

firs = {}

# ─────────────────────────────────────────────────────────────────────────────
# CASE 1 – OPERATION SANDSTORM (Narcotics ring)
# Entities: P001=Arjun Mehta, P002=Deepak Rao, P003=Sunita Verma,
#           P004=Rajan Pillai, P005=Kabir Sheikh
# ORG001=Phoenix Exports, ORG002=Sunrise Traders
# Phones: PH001=+91-98400-11111, PH002=+91-98400-12345 (burner),
#         PH003=+91-98400-22222, PH004=+91-98400-33333
# Noise:  Ramesh Iyer (witness), Priya Sharma (bystander)
# ─────────────────────────────────────────────────────────────────────────────

firs["fir_sandstorm_1.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0041/2025/0312
Date of Filing : 13/03/2025
Time of Filing : 19:45
Police Station : Dharavi Police Station
District       : Mumbai (Central)
State          : Maharashtra
Section of BNS : Sections 22, 27, 29 – Narcotic Drugs and
                 Psychotropic Substances Act, 1985 (NDPS)

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name           : Inspector K.G. Nair
Badge No.      : MH-CIB-4401
Police Station : Dharavi, Mumbai
Phone          : +91-98400-90001
Designation    : Sub-Inspector, Crime Investigation Branch

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name        : A. Mehta
  Father's Name : Suresh Mehta
  Address     : Room 14-B, Kumbharwada Chawl, Dharavi, Mumbai – 400017
  Phone       : +91-98400-11111
  Occupation  : Described as commission agent for Phoenix Exports

Accused No. 2
  Name        : Deepak R.
  Father's Name : Govind Rao
  Address     : 22, Nehru Nagar, Sion, Mumbai – 400022
  Phone       : +91-98400-22222
  Vehicle     : MH-04-AB-1234 (Maruti Suzuki Eeco, white)
  Occupation  : Transport contractor

Accused No. 3
  Name        : Kabeer Sheikh
  Father's Name : Mohammed Sheikh
  Address     : Bldg No. 7, Transit Camp, Dharavi, Mumbai – 400017
  Phone       : +91-98400-55555
  Occupation  : Daily wage labourer (stated)

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
On 13/03/2025 at approximately 18:30 hours, acting on credible intelligence
received through a secret informer, Sub-Inspector K.G. Nair along with a team
of constables from Dharavi Police Station conducted a surprise check near
Pottery Road Junction, Dharavi, Mumbai.

During the check, a white Maruti Suzuki Eeco van bearing registration
MH-04-AB-1234 was intercepted. The vehicle was driven by one Deepak R.,
a known associate of a narcotics distribution network operating in the
Dharavi and Sion areas.

On search of the vehicle, constables recovered 4.2 kg of suspected
brown-sugar (diacetylmorphine) concealed inside hollow vegetable crates
branded with the logo of "Phoenix Exports". The contraband was vacuum-sealed
in black polythene and showed evidence of recent packaging.

A. Mehta, who was present at the scene and identified himself as the
consignment coordinator for Phoenix Exports (+91-98400-11111), was apprehended
at the same spot. On personal search, a second mobile phone bearing SIM with
number +91-98400-12345 was recovered from his possession.

A third person, Kabeer Sheikh, was apprehended 150 metres from the site while
attempting to flee. He is believed to be the street-level distributor.

Witness Ramesh Iyer, a resident of Plot 8, Dharavi, was present at the scene
and has agreed to provide a statement. Priya Sharma, who resides in the
adjacent lane, was questioned briefly but stated she had no connection to the
accused persons.

The following items were seized:
  – 4.2 kg suspected heroin (sample sent for chemical analysis)
  – 1 x Nokia mobile phone (IMEI ending 3311) from A. Mehta
  – 1 x Samsung mobile phone (IMEI ending 7892) (burner, SIM +91-98400-12345)
  – Cash of Rs. 38,500/- from Deepak R.
  – Vehicle MH-04-AB-1234 (impounded)
  – 12 x Phoenix Exports branded crates

Subsequent phone records indicated that A. Mehta (+91-98400-11111) had received
multiple calls from an unidentified number (+91-98400-33333) in the 48 hours
preceding the seizure. Investigation is ongoing.

═══════════════════════════════════════════════════════════════════
4. WITNESSES
═══════════════════════════════════════════════════════════════════
1. Ramesh Iyer, Plot 8, Pottery Road, Dharavi, Mumbai – 400017
   Phone: +91-98400-77777

2. Constable Santosh Patil, Badge MH-1204, Dharavi PS

═══════════════════════════════════════════════════════════════════
5. PROPERTY SEIZED (detailed list in Panchnama attached)
═══════════════════════════════════════════════════════════════════
  Ref. Panchnama No.: DHAR-PNM-2025-0312

Signature of Complainant : Insp. K.G. Nair  (K.G. Nair)
Signature of IO          : SI Mohan Deshmukh
Date/Time Recorded       : 13/03/2025 / 19:45 hrs
"""

firs["fir_sandstorm_2.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0041/2025/0318
Date of Filing : 15/03/2025
Time of Filing : 23:10
Police Station : Amboli Police Station (Andheri West)
District       : Mumbai (Suburban)
State          : Maharashtra
Section of BNS : Sections 22, 27 – NDPS Act 1985;
                 Section 120-B IPC (Criminal Conspiracy)

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name           : ACP Vasant Kulkarni
Badge No.      : MH-ACP-0071
Phone          : +91-98400-90002
Designation    : Asst. Commissioner of Police, Zone IV, Mumbai

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name        : Arjun Mehata          [NOTE: Alias — canon: Arjun Mehta]
  Address     : Room 14-B, Kumbharwada Chawl, Dharavi (same as FIR 0312)
  Phone       : +91-98400-11111
  Status      : In judicial custody (arrested 13/03/2025 per FIR 0312)

Accused No. 2
  Name        : S. Verma
  Father's Name : Hariom Verma
  Address     : Flat 4C, Veena Nagar, Andheri West, Mumbai – 400053
  Phone       : +91-98400-33333
  Occupation  : Accounts executive, Sunrise Trading Co.

Accused No. 3
  Name        : Rajan Pillai
  Father's Name : Krishnan Pillai
  Address     : 301, Shanti Apt., D.N. Road, Andheri West, Mumbai – 400053
  Phone       : +91-98400-44444
  Occupation  : Delivery agent

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
Following the seizure of narcotics on 13/03/2025 (FIR No. MH-0041/2025/0312),
further investigation revealed a second consignment was scheduled for delivery
at a godown near Andheri (W) on 15/03/2025.

Acting on this intelligence, a special team conducted a raid at Godown No. 7,
Krishi Market Complex, J.P. Road, Andheri West at 22:15 hours on 15/03/2025.

One S. Verma, accounts executive of Sunrise Trading Co., was found on the
premises maintaining a cash ledger. She was in telephonic contact with
+91-98400-11111 (Arjun Mehata, in custody) as recently as 14/03/2025 at
17:40 hours, confirmed by call detail records.

Rajan Pillai was present at the godown and claimed he was merely a delivery
agent. However, records show he received Rs. 15,000 in cash from Sunrise
Trading Co. on 10/03/2025 — three days before the first seizure.

Seized at the godown:
  – 2.8 kg suspected heroin (sample sent for analysis, Ref. FSLD-2025-0803)
  – Cash ledger with entries showing disbursements to "D.R." and "K.S."
    corresponding to aliases used by Deepak R. and Kabeer Sheikh
  – 1 x iPhone (recovered from S. Verma) with messages referencing "delivery"
  – Bank deposit slips for Sunrise Trading Co. account SBI-XXXX-2002

Investigation indicates the network operated through two shell entities —
Phoenix Exports and Sunrise Trading Co. — to launder proceeds.

═══════════════════════════════════════════════════════════════════
4. WITNESSES
═══════════════════════════════════════════════════════════════════
1. HC Dinesh Pawar, Badge MH-3301, Amboli PS
2. Godown guard Suresh Patkar (statement recorded separately)

Signature of Complainant : ACP V. Kulkarni
Signature of IO          : PI Rajesh Bhosale, Amboli PS
Date/Time Recorded       : 15/03/2025 / 23:10 hrs
"""

firs["fir_sandstorm_3.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0041/2025/0325
Date of Filing : 18/03/2025
Time of Filing : 11:20
Police Station : Dharavi Police Station
District       : Mumbai (Central)
State          : Maharashtra
Section of BNS : Section 3 – Prevention of Money Laundering Act (PMLA);
                 Section 420 IPC (Cheating)

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : Branch Manager, HDFC Bank, Sion Branch
Address   : HDFC Bank, Plot 22, Sion Circle, Mumbai – 400022
Phone     : +91-22-2401-1100

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name         : Arjun M.           [NOTE: Alias — canon: Arjun Mehta]
  Account      : HDFC-XXXX-1001
  Address      : Room 14-B, Kumbharwada Chawl, Dharavi, Mumbai
  Phone        : +91-98400-11111

Accused No. 2 (Entity)
  Name         : Phoenix Exp. Pvt Ltd
  Account      : HDFC-XXXX-1002
  Registered Address : 11, Indira Industrial Estate, Kurla, Mumbai – 400070
  Director (stated): Arjun M.

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
The complainant, Branch Manager of HDFC Bank Sion, reports suspicious
transaction patterns in accounts linked to one Arjun M. and the corporate
entity Phoenix Exp. Pvt Ltd.

Between 01/01/2025 and 13/03/2025, account HDFC-XXXX-1001 (held by Arjun M.)
received 10 cash deposits ranging from Rs. 9,80,000 to Rs. 9,95,000 each.
These transactions occurred on non-consecutive days and consistently fell
just below the Rs. 10,00,000 regulatory reporting threshold under the
Prevention of Money Laundering Act.

Each deposit was followed within 24 hours by a transfer to the corporate
account HDFC-XXXX-1002, maintained in the name of Phoenix Exp. Pvt Ltd.
The funds were subsequently transferred to account SBI-XXXX-2001 held by
one D. Rao (believed to be alias Deepak R.).

The bank did not receive satisfactory documentation for the stated business
purpose (export commission payments). The account was flagged by the bank's
automated transaction monitoring system.

Note: Account HDFC-XXXX-1001 is linked to mobile number +91-98400-11111,
which appears in FIR No. MH-0041/2025/0312 as the primary contact of
the arrested accused A. Mehta.

═══════════════════════════════════════════════════════════════════
4. DOCUMENTS ATTACHED
═══════════════════════════════════════════════════════════════════
  – Bank statement HDFC-XXXX-1001 (01/01/2025 – 15/03/2025)
  – Bank statement HDFC-XXXX-1002 (01/01/2025 – 15/03/2025)
  – STR filed with FIU-IND (Ref: STR-MH-2025-04421)

Signature of Complainant : Branch Manager, HDFC Sion
Signature of IO          : SI Mohan Deshmukh, Dharavi PS
Date/Time Recorded       : 18/03/2025 / 11:20 hrs
"""

firs["fir_sandstorm_4.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0041/2025/0341
Date of Filing : 22/03/2025
Time of Filing : 15:00
Police Station : Dharavi Police Station
District       : Mumbai (Central)
State          : Maharashtra
Section of BNS : Section 22, 29 – NDPS Act; Section 34 IPC (Common intention)

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : Insp. K.G. Nair
Badge No. : MH-CIB-4401
Phone     : +91-98400-90001

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name    : Sunitha Verma          [NOTE: Alias — canon: Sunita Verma]
  Address : Flat 4C, Veena Nagar, Andheri West, Mumbai
  Phone   : +91-98400-33333

Accused No. 2
  Name    : K. Sheikh
  Address : Bldg No. 7, Transit Camp, Dharavi, Mumbai
  Phone   : +91-98400-55555

Accused No. 3 (absconding)
  Name    : D. Rao
  Vehicle : MH-04-AB-1234 (same vehicle FIR 0312; currently impounded)
  Phone   : +91-98400-22222
  Status  : Absconding as of 22/03/2025

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
Following arrest and remand of A. Mehta and Kabeer Sheikh, and recovery of
the ledger from S. Verma (FIR 0318), further CDR analysis conducted by the
CIB confirmed the following calling pattern in the 48 hours before the first
seizure on 13/03/2025:

- +91-98400-11111 (A. Mehta) placed or received 14 calls on 12–13/03/2025
  across a period of 31 hours, compared to a daily average of 1–2 calls
  in the preceding 30-day baseline.

- The majority of these calls were to +91-98400-22222 (D. Rao) and
  +91-98400-33333 (Sunitha Verma).

- K. Sheikh's phone (+91-98400-55555) shows 6 calls to +91-98400-11111
  on 12/03/2025, all from Tower BOM-447 (Dharavi area), confirming
  physical presence near the seizure site.

On 22/03/2025, Sunitha Verma was arrested at her residence. K. Sheikh,
who was already in custody, has been additionally charged under this FIR.
D. Rao remains at large. A lookout notice has been issued.

Investigating officers believe Sunrise Trading Co. (Sunrise Trading Co.)
served as the distribution-side financial conduit, while Phoenix Exp. Pvt Ltd
handled the procurement-side. Both entities share a registered address
at Kurla Industrial Estate.

═══════════════════════════════════════════════════════════════════
4. WITNESSES
═══════════════════════════════════════════════════════════════════
1. Ramesh Iyer (original witness, FIR 0312)
2. HC Dinesh Pawar (FIR 0318)
3. Forensic Analyst Report FSLD-2025-0803 (attached)

Signature of Complainant : Insp. K.G. Nair
Signature of IO          : PI Rajesh Bhosale
Date/Time Recorded       : 22/03/2025 / 15:00 hrs
"""

# ─────────────────────────────────────────────────────────────────────────────
# CASE 2 – OPERATION PHANTOM (Extortion / Hawala)
# Entities: Q001=Vikram Sinha, Q002=Meera Nambiar, Q003=Farhan Qureshi,
#           Q004=Lakshmi Devi (victim), Q006=Anand Krishnan (HIDDEN BRIDGE),
#           Q007=Rohit Jain (Cluster B), Q008=Neha Gupta (Cluster B)
# ORG003=Delta Finance Ltd, ORG004=Sigma Holdings
# ─────────────────────────────────────────────────────────────────────────────

firs["fir_phantom_1.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0062/2025/0198
Date of Filing : 05/04/2025
Time of Filing : 14:30
Police Station : Andheri East Police Station
District       : Mumbai (Suburban)
State          : Maharashtra
Section of BNS : Section 383, 384, 386 IPC (Extortion); Section 506 IPC (Criminal Intimidation)

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : Lakshmi Devi
Age       : 52
Address   : 7B, Geetanjali Co-op Society, Marol, Andheri East, Mumbai – 400059
Phone     : +91-97300-44444
Occupation: Retired school teacher

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1 (identified from voice; identity unconfirmed)
  Name (stated) : V. Sinha
  Phone used    : +91-97300-11111
  Description   : Male, approximately 35–40 years, fluent Hindi speaker

Accused No. 2
  Name    : Farhan Quereshi       [NOTE: Alias — canon: Farhan Qureshi]
  Address : 204, Yasmin Building, Kurla West, Mumbai – 400070
  Phone   : +91-97300-33333
  Role    : Cash collector / courier

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
The complainant Lakshmi Devi states that from approximately 01/03/2025,
she began receiving threatening calls from the number +91-97300-11111.
The caller, who identified himself only as V. Sinha, demanded a payment of
Rs. 5,00,000, threatening physical harm to her son if payment was not made.

The complainant paid a first installment of exactly Rs. 5,00,000 in cash on
12/03/2025, which was collected from her residence by one Farhan Quereshi,
who arrived in an autorickshaw and provided no receipt or identification.

On 28/03/2025, a second demand of Rs. 5,00,000 was made via the same
number. The complainant has not paid the second installment and has instead
filed this complaint.

Witness: Suresh Babu, neighbour, was present during the collection on
12/03/2025 and can identify Farhan Quereshi by appearance.

Call records for +91-97300-11111 are requested to be subpoenaed.

═══════════════════════════════════════════════════════════════════
4. WITNESSES
═══════════════════════════════════════════════════════════════════
1. Suresh Babu, C/o Complainant's address, Phone: +91-97300-55555

Signature of Complainant : Lakshmi Devi
Signature of IO          : SI Pradeep Ghate, Andheri East PS
Date/Time Recorded       : 05/04/2025 / 14:30 hrs
"""

firs["fir_phantom_2.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0062/2025/0211
Date of Filing : 10/04/2025
Time of Filing : 16:00
Police Station : Andheri East Police Station
District       : Mumbai (Suburban)
State          : Maharashtra
Section of BNS : FEMA Sections 3, 4; Section 25 PMLA; Section 120-B IPC

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : Inspector Sushil Tawde
Badge No. : MH-EOW-0022
Unit      : Economic Offences Wing, Mumbai
Phone     : +91-98400-90003

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name    : Vikram S.             [NOTE: Alias — canon: Vikram Sinha]
  Address : 501 Prestige Tower, Link Road, Malad West, Mumbai – 400064
  Phone   : +91-97300-11111
  Account : AXIS-XXXX-4001

Accused No. 2
  Name    : M. Nambiar
  Address : 12, Devidas Lane, Borivali West, Mumbai – 400092
  Phone   : +91-97300-22222
  Account : AXIS-XXXX-4002
  Role    : Hawala operator; listed as director of Delta Finance Ltd

Accused No. 3 (Entity)
  Name    : Delta Finance Ltd (also referred as Delta Finance)
  Account : YES-XXXX-5001
  Address : Office 3C, Trade Centre, BKC, Mumbai – 400051

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
Intelligence inputs obtained by the Economic Offences Wing indicate that
a hawala network operating under the front of Delta Finance Ltd has been
routing extortion proceeds out of Mumbai through informal value transfer
channels.

Analysis of account AXIS-XXXX-4002 (held by M. Nambiar) shows receipt of
6 transfers of exactly Rs. 5,00,000 and Rs. 10,00,000 between 15/01/2025
and 05/04/2025, all originating from accounts linked to entities in which
Vikram S. is a common signatory.

These round-number transfers — all exactly Rs. 5,00,000 or Rs. 10,00,000
— are inconsistent with legitimate business activity and are consistent
with hawala settlement patterns observed in prior investigations.

Each incoming transfer was followed within 48 hours by an outward RTGS
to account YES-XXXX-5001 (Delta Finance Ltd), subsequently disbursed
in multiple smaller amounts.

The network's Cluster A (Vikram S. and M. Nambiar) has no apparent
connection to a second network (Cluster B) under separate investigation.
Cross-reference with EOW file number EOW-2025-B-041 is recommended.

═══════════════════════════════════════════════════════════════════
4. DOCUMENTS ATTACHED
═══════════════════════════════════════════════════════════════════
  – Account statements AXIS-XXXX-4001, AXIS-XXXX-4002, YES-XXXX-5001
  – STR filed with FIU-IND (Ref: STR-MH-2025-06112)
  – Subscriber details for +91-97300-11111 and +91-97300-22222

Signature of Complainant : Insp. S. Tawde, EOW
Signature of IO          : PI Sandeep Rane, Andheri East PS
Date/Time Recorded       : 10/04/2025 / 16:00 hrs
"""

firs["fir_phantom_3.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0062/2025/0229
Date of Filing : 17/04/2025
Time of Filing : 09:45
Police Station : Kurla Police Station
District       : Mumbai (Suburban)
State          : Maharashtra
Section of BNS : Section 384, 411 IPC; NDPS Act Section 29

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : SI Ganesh Mahadik
Badge No. : MH-1892
Phone     : +91-98400-90004

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name    : F. Qureshi             [NOTE: Alias — canon: Farhan Qureshi]
  Address : 204, Yasmin Building, Kurla West, Mumbai – 400070
  Phone   : +91-97300-33333
  Status  : Arrested 17/04/2025

Accused No. 2 (not yet apprehended)
  Name    : Aanand Krishnan        [NOTE: Alias — canon: Anand Krishnan, HIDDEN BRIDGE]
  Address : Office known to be in BKC area (exact address under investigation)
  Phone   : +91-97300-66666
  Account : HDFC-XXXX-4003

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
On 17/04/2025, acting on surveillance conducted over 3 days, a team from
Kurla PS apprehended F. Qureshi at his residence, 204, Yasmin Building,
Kurla West.

On search, the following were recovered:
  – Rs. 2,40,000 in cash (alleged to be extortion proceeds collected on
    behalf of V. Sinha)
  – A chit containing mobile number +91-97300-66666 and the name
    "Aanand K." with a notation "BKC office – balance settle"
  – A register showing 7 cash collection entries, each corresponding to
    dates of known extortion demands against Lakshmi Devi (FIR 0198)

The reference to Aanand K. (+91-97300-66666) and account HDFC-XXXX-4003
is currently under investigation. Initial checks indicate this entity
may act as a financial intermediary between Cluster A and a separate
operation. Further details are being pursued.

F. Qureshi stated under caution that he was instructed by V. Sinha
(+91-97300-11111) to hand over collected cash to "Aanand" at a BKC cafe
on at least three occasions. This has not yet been independently verified.

═══════════════════════════════════════════════════════════════════
4. WITNESSES
═══════════════════════════════════════════════════════════════════
1. SI Ganesh Mahadik (arresting officer)
2. Constable Dilip Naik, Badge MH-2204

Signature of Complainant : SI G. Mahadik
Signature of IO          : PI Sandeep Rane, Andheri East PS
Date/Time Recorded       : 17/04/2025 / 09:45 hrs
"""

firs["fir_phantom_4.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0062/2025/0244
Date of Filing : 24/04/2025
Time of Filing : 18:30
Police Station : BKC Police Post (Bandra Kurla Complex)
District       : Mumbai (Suburban)
State          : Maharashtra
Section of BNS : Section 3, 4 PMLA; Section 120-B IPC; FEMA

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : Inspector Sushil Tawde
Badge No. : MH-EOW-0022
Unit      : Economic Offences Wing

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name    : A. Krishnan            [NOTE: Alias — canon: Anand Krishnan]
  Address : Suite 12B, Platina Tower, BKC, Mumbai – 400051
  Phone   : +91-97300-66666
  Account : HDFC-XXXX-4003
  Role    : FINANCIAL BRIDGE — transfers between Cluster A and Cluster B

Accused No. 2
  Name    : Rohit J.               [NOTE: Alias — canon: Rohit Jain, Cluster B]
  Address : 8, Manek Nagar, Vile Parle (E), Mumbai – 400057
  Phone   : +91-97300-77777
  Account : SBI-XXXX-4004

Accused No. 3 (Entity)
  Name    : Sigma Holdings (also: Sigma Hold.)
  Account : YES-XXXX-5002
  Address : Same as A. Krishnan (Suite 12B, Platina Tower, BKC)

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
Continuing investigation from FIR 0211 (hawala network, Cluster A) and
FIR 0229 (courier F. Qureshi), the EOW has identified a financial
intermediary, one A. Krishnan, who appears to serve as the sole linking
node between the Vikram S. / M. Nambiar network (Cluster A) and a
previously unconnected financial fraud operation in the Vile Parle area.

Account HDFC-XXXX-4003 (A. Krishnan) received exactly Rs. 10,00,000 on
15/03/2025 from YES-XXXX-5001 (Delta Finance Ltd, Cluster A), and within
24 hours transferred exactly Rs. 10,00,000 to SBI-XXXX-4004 (Rohit J.,
Cluster B). This same pattern repeated on 01/04/2025 for Rs. 5,00,000.

Without this node, Cluster A and Cluster B would show no documented
financial connection. A. Krishnan is believed to have no awareness of the
ultimate criminal nature of either network, though this is contested by
the IO based on the round-number transfer pattern and timing.

Rohit J. and his associate N. Gupta (Cluster B) are separately under
investigation under EOW file EOW-2025-B-041.

NOTE TO GRAPH ANALYST: A. Krishnan / +91-97300-66666 / HDFC-XXXX-4003 is
the bridge between Cluster A and Cluster B. Without graph traversal,
this link is not visible in any single FIR or account statement.

═══════════════════════════════════════════════════════════════════
4. DOCUMENTS ATTACHED
═══════════════════════════════════════════════════════════════════
  – Account statements HDFC-XXXX-4003 (Jan–Apr 2025)
  – Wire transfer confirmations (15/03/2025, 01/04/2025)
  – Subscriber details for +91-97300-66666

Signature of Complainant : Insp. S. Tawde, EOW
Signature of IO          : PI Sandeep Rane
Date/Time Recorded       : 24/04/2025 / 18:30 hrs
"""

# ─────────────────────────────────────────────────────────────────────────────
# CASE 3 – OPERATION MIRAGE (Identity Fraud / SIM-Swap)
# Entities: R001=Imran Khan, R002=Pooja Desai, R003=Arun Tiwari,
#           R004=Sanjay Yadav, R005=Kavya Nair (victim), R006=Thomas Mathew (victim)
# ORG005=Apex Digital Services, ORG006=NextGen Solutions
# ─────────────────────────────────────────────────────────────────────────────

firs["fir_mirage_1.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0088/2025/0091
Date of Filing : 02/05/2025
Time of Filing : 10:15
Police Station : Bandra Police Station
District       : Mumbai (Suburban)
State          : Maharashtra
Section of BNS : Section 66C, 66D IT Act; Section 420, 468 IPC

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : Kavya Nair
Age       : 34
Address   : 12, Hill Road Residency, Bandra West, Mumbai – 400050
Phone     : +91-96200-55555
Occupation: Software Engineer

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1 (identified from telecom records)
  Name    : Imraan Khan            [NOTE: Alias — canon: Imran Khan]
  Address : Under investigation
  Phone   : +91-96200-11111
  Account : PNB-XXXX-6001

Accused No. 2
  Name    : P. Desai
  Address : 33, Sion Koliwada, Sion, Mumbai – 400022
  Phone   : +91-96200-22222
  Role    : SIM swap facilitator (telecom insider, alleged)

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
The complainant Kavya Nair states that on 30/04/2025 at approximately
02:30 hours, her mobile number (+91-96200-55555) suddenly stopped
receiving network signal. She was unable to make or receive calls for
approximately 4 hours.

Upon visiting the telecom service centre the next morning, she was
informed that a SIM replacement for her number had been issued the
previous evening to an individual presenting a forged Aadhaar card
in her name.

During the period of SIM outage (02:30–06:45 hours on 30/04/2025), the
following transactions were processed via her bank's mobile OTP system:
  – Rs. 4,50,000 transferred from complainant's savings account to
    PNB-XXXX-6001 (linked to mobile +91-96200-11111, subscriber: Imraan Khan)
  – Rs. 4,50,000 transferred from complainant's FD linked account to
    KOTAK-XXXX-7001 (entity: Apex Digital Svcs)

The transactions were authenticated via OTPs sent to the cloned SIM
and are not recognised by the complainant. The timing (02:30–04:00 hours)
and the recipients (a new account and a services company) are anomalous.

P. Desai is suspected to be an insider at the telecom service centre
who facilitated the SIM swap without proper verification.

═══════════════════════════════════════════════════════════════════
4. WITNESSES
═══════════════════════════════════════════════════════════════════
1. Telecom service centre manager (identity withheld, statement recorded)
2. Bank Officer Sharma, Branch Manager, Bandra West branch

Signature of Complainant : Kavya Nair
Signature of IO          : SI Rekha Patil, Bandra PS
Date/Time Recorded       : 02/05/2025 / 10:15 hrs
"""

firs["fir_mirage_2.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0088/2025/0099
Date of Filing : 05/05/2025
Time of Filing : 14:50
Police Station : Bandra Police Station
District       : Mumbai (Suburban)
State          : Maharashtra
Section of BNS : Section 66C, 66D IT Act; Section 420 IPC; Section 120-B IPC

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : Thomas Mathew
Age       : 48
Address   : 5A, St. Mary's CHS, Khar West, Mumbai – 400052
Phone     : +91-96200-66666
Occupation: Businessman

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name    : I. Khan               [NOTE: Alias — canon: Imran Khan]
  Phone   : +91-96200-11111
  Account : PNB-XXXX-6001

Accused No. 2
  Name    : A. Tiwari             [NOTE: Alias — canon: Arun Tiwari]
  Address : 77, Laxmi Nagar, Ghatkopar East, Mumbai – 400077
  Phone   : +91-96200-33333
  Account : BOI-XXXX-6003
  Role    : Money mule

Accused No. 3
  Name    : Sanjay Y.             [NOTE: Alias — canon: Sanjay Yadav]
  Address : 12, Gokul Nagar, Mulund West, Mumbai – 400080
  Phone   : +91-96200-44444
  Account : BOI-XXXX-6004
  Role    : Money mule

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
The complainant Thomas Mathew states that on 30/04/2025 between
03:10 hours and 04:20 hours, his mobile number (+91-96200-66666)
went dead. He discovered the next morning that Rs. 4,50,000 had been
debited from his account via an OTP transaction he did not initiate.

Investigation revealed the funds were transferred to BOI-XXXX-6003
(A. Tiwari), from where Rs. 2,00,000 was immediately forwarded to
BOI-XXXX-6004 (Sanjay Y.) within 3 hours. The remainder was withdrawn
as cash.

Both A. Tiwari and Sanjay Y. appear to be money mules — their accounts
show no prior transaction history of this size. Both are linked via
phone records to +91-96200-11111 (I. Khan), receiving 4 calls and
3 calls respectively in the 72 hours preceding the fraud.

Note: This incident occurred on the same night as FIR 0091 (Kavya Nair).
The coincidence in timing (02:30–04:30 hours), the amount (Rs. 4,50,000),
and the involvement of entity Apex Digital Svcs (KOTAK-XXXX-7001) in FIR
0091 and NextGen Sol. (KOTAK-XXXX-7002) in this case — both sharing a
registered agent — warrants a consolidated investigation.

All 4 phones of suspects (R001–R004) were co-located at Tower BKC-112
on 29/04/2025 between 22:00 and 23:30, as per CDR tower records —
approximately 3 hours before the fraud commenced.

═══════════════════════════════════════════════════════════════════
4. WITNESSES
═══════════════════════════════════════════════════════════════════
1. Bank Officer Sharma (same as FIR 0091)
2. Telecom service centre (Bandra West branch)

Signature of Complainant : Thomas Mathew
Signature of IO          : SI Rekha Patil
Date/Time Recorded       : 05/05/2025 / 14:50 hrs
"""

firs["fir_mirage_3.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0088/2025/0114
Date of Filing : 12/05/2025
Time of Filing : 11:00
Police Station : Bandra Police Station
District       : Mumbai (Suburban)
State          : Maharashtra
Section of BNS : Section 66C, 66D IT Act; Section 420, 471 IPC

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : B.O. Sharma
Designation: Branch Manager, Canara Bank, Bandra West Branch
Phone     : +91-22-2640-4411
Address   : Canara Bank, Turner Road, Bandra West, Mumbai – 400050

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name    : Imraan Khan            [NOTE: Alias — canon: Imran Khan]
  Phone   : +91-96200-11111
  Account : PNB-XXXX-6001
  Status  : Warrant issued; location under investigation

Accused No. 2
  Name    : Pooja D.              [NOTE: Alias — canon: Pooja Desai]
  Phone   : +91-96200-22222
  Address : 33, Sion Koliwada, Sion, Mumbai – 400022
  Status  : Arrested 11/05/2025

Accused No. 3 (Entity)
  Name    : Apex Digital Svcs     [NOTE: Alias — canon: Apex Digital Services]
  Account : KOTAK-XXXX-7001
  Address : 402, Trade Wings, BKC, Mumbai – 400051
  Director: Listed as Arun Tiwary  [NOTE: Alias — canon: Arun Tiwari]

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
Bank Officer Sharma reports that a pattern of fraudulent SIM-swap
enabled transactions was identified across 6 Canara Bank customers
between 15/04/2025 and 10/05/2025.

In each case, the customer's mobile number was cloned between 02:00
and 04:00 hours, and funds were immediately transferred out via OTP.
All receiving accounts trace back to:
  (a) PNB-XXXX-6001 (Imraan Khan)
  (b) KOTAK-XXXX-7001 (Apex Digital Svcs, director: Arun Tiwary)
  (c) KOTAK-XXXX-7002 (NextGen Sol., same registered agent)

Pooja D. was arrested on 11/05/2025 following identification from
CCTV at the telecom service centre. She facilitated at least 4 SIM
swaps using forged documentation.

Analysis of KOTAK-XXXX-7001 (Apex Digital Svcs) shows 8 inward credits
between Rs. 4,00,000 and Rs. 4,80,000, all received between 02:00 and
04:00 hours — an anomalous time window for commercial transactions —
followed by immediate outward IMPS transfers in round-number amounts.

All transactions flagged by bank's automated system but not escalated
in time. STR filed with FIU-IND (Ref: STR-MH-2025-08822).

═══════════════════════════════════════════════════════════════════
4. DOCUMENTS ATTACHED
═══════════════════════════════════════════════════════════════════
  – Account statements KOTAK-XXXX-7001, KOTAK-XXXX-7002
  – CCTV screenshots of Pooja D. at telecom service centre
  – STR-MH-2025-08822

Signature of Complainant : B.O. Sharma, Canara Bank
Signature of IO          : PI Avinash Kadam, Bandra PS
Date/Time Recorded       : 12/05/2025 / 11:00 hrs
"""

firs["fir_mirage_4.txt"] = """\
FIRST INFORMATION REPORT
(Under Section 154 Cr.P.C. / BNSS 2023)
═══════════════════════════════════════════════════════════════════

FIR No         : MH-0088/2025/0131
Date of Filing : 20/05/2025
Time of Filing : 16:20
Police Station : Bandra Police Station
District       : Mumbai (Suburban)
State          : Maharashtra
Section of BNS : Section 3, 4 PMLA; Section 66C IT Act; Section 120-B IPC

═══════════════════════════════════════════════════════════════════
1. COMPLAINANT DETAILS
═══════════════════════════════════════════════════════════════════
Name      : Inspector Meena Subramaniam
Badge No. : MH-CID-0301
Unit      : Cyber Crime Division, Mumbai
Phone     : +91-98400-90005

═══════════════════════════════════════════════════════════════════
2. ACCUSED DETAILS
═══════════════════════════════════════════════════════════════════
Accused No. 1
  Name    : I. Khan              [NOTE: Alias — canon: Imran Khan]
  Phone   : +91-96200-11111
  Account : PNB-XXXX-6001
  Status  : Arrested 19/05/2025

Accused No. 2
  Name    : Arun Tiwary          [NOTE: Alias — canon: Arun Tiwari]
  Phone   : +91-96200-33333
  Account : BOI-XXXX-6003
  Status  : Arrested 19/05/2025

Accused No. 3
  Name    : S. Yadav             [NOTE: Alias — canon: Sanjay Yadav]
  Phone   : +91-96200-44444
  Account : BOI-XXXX-6004
  Status  : Arrested 19/05/2025

═══════════════════════════════════════════════════════════════════
3. DESCRIPTION OF INCIDENT
═══════════════════════════════════════════════════════════════════
Cyber Crime Division investigation consolidates findings from FIR 0091,
0099, and 0114 into a single organised ring.

CDR analysis confirms that I. Khan (+91-96200-11111), Arun Tiwary
(+91-96200-33333), S. Yadav (+91-96200-44444), and P. Desai
(+91-96200-22222) were co-located at Tower BKC-112 on 29/04/2025
(22:00–23:30) and Tower MLW-88 on 08/05/2025 (21:30–22:45).
Physical co-location immediately before fraud execution on both dates.

Transaction velocity analysis on PNB-XXXX-6001 (I. Khan):
  – 8 inward credits between Rs. 4,00,000 and Rs. 4,80,000
  – All received between 02:00 and 04:00 hours (anomalous time window)
  – All to new recipient accounts with no prior transaction history
  – All within a 35-day window (15/04/2025 – 20/05/2025)

I. Khan was apprehended at Chhatrapati Shivaji International Airport
on 19/05/2025 attempting to board a flight to Dubai.
Arun Tiwary and S. Yadav were arrested simultaneously at their residences.

Apex Digital Svcs and NextGen Sol. are to be deregistered. Their accounts
are frozen pending PMLA proceedings.

═══════════════════════════════════════════════════════════════════
4. WITNESSES
═══════════════════════════════════════════════════════════════════
1. Kavya Nair (FIR 0091 complainant)
2. Thomas Mathew (FIR 0099 complainant)
3. B.O. Sharma (FIR 0114 complainant)
4. Airport Security – CSIA (arrest confirmed)

Signature of Complainant : Insp. M. Subramaniam, Cyber Crime
Signature of IO          : PI Avinash Kadam
Date/Time Recorded       : 20/05/2025 / 16:20 hrs
"""

# ─────────────────────────────────────────────────────────────────────────────
# Write all files
# ─────────────────────────────────────────────────────────────────────────────
for fname, content in firs.items():
    path = os.path.join(BASE, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {fname}  ({len(content):,} bytes)")

print(f"\nDone. {len(firs)} FIR files written to {BASE}")
