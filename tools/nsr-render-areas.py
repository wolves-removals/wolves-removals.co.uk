#!/usr/bin/env python3
"""Render the 8 area pages + areas-covered/index.html.
Uses the shared scaffolding in render-pages.py (head/topbar/nav/cta/footer)."""

from __future__ import annotations
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

# Import shared helpers from render-pages.py
import importlib.util
spec = importlib.util.spec_from_file_location("rp", os.path.join(ROOT, 'tools', 'render-pages.py'))
rp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rp)

os.chdir(ROOT)


AREAS = [
    {
        'slug': 'areas-covered/removals-stoke-on-trent.html',
        'town': 'Stoke-on-Trent',
        'title': 'Removals Stoke-on-Trent | NSR Removals &amp; Storage',
        'desc': "Removals in Stoke-on-Trent — the six towns of Hanley, Burslem, Tunstall, Longton, Fenton and Stoke. Family-run, fixed price, fully covered.",
        'h1': 'Removals across the six towns of Stoke-on-Trent',
        'eyebrow': 'Stoke-on-Trent · ST1–ST7',
        'lead': "Hanley, Burslem, Tunstall, Longton, Fenton and Stoke — the six towns of Stoke-on-Trent are our home patch. North Staffordshire Removals &amp; Storage Ltd has been family-run from a Stoke depot since 2010, and our crews live, breathe and drive the ST postcode area every working day.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Removals in the Potteries, by people who live here",
             [
                "Stoke-on-Trent is unique: six federated towns strung along the A5008 and the Caldon Canal, each with its own High Street, parking habits and access challenges. A move out of a Victorian terrace in Burslem is a different job from a four-bedroom new-build off the A500 in Trentham — and our crews price each accordingly.",
                "From our Stoke-on-Trent depot at the Genesis Centre off Innovation Way (ST6 4BF), we're on the doorstep of every postcode in the ST1–ST7 range. Most local moves complete in a single day. Larger four-bedroom moves out to the Moorlands or Newcastle borough sometimes phase into two days if you'd like a slower, calmer pace.",
                "We've moved customers in and out of nearly every estate in the city — Westport, Birches Head, Bucknall, Trentham Lakes, Sneyd Green, Penkhull, Hartshill — and we know which roads to avoid at school-run time, which one-way streets are mistakes to enter with a 7.5-tonne, and where the loading bays are at every town centre site.",
             ]),
            ("Which Stoke postcodes we cover",
             [
                "<strong>ST1 (Hanley)</strong> — the city centre. Tight terraces, busy lunchtime parking, regular Cultural Quarter moves. We typically work the residential streets early morning or after 6pm to avoid the worst of the parking pressure.",
                "<strong>ST2 (Abbey Hulton, Birches Head, Smallthorne)</strong> — mostly residential, easier access, large estate housing. Our most common Stoke jobs.",
                "<strong>ST3 (Longton, Meir, Blurton)</strong> — mix of older Victorian terraces and 1980s/90s estates. Some of the steeper terraced streets need our experience.",
                "<strong>ST4 (Penkhull, Trent Vale, Hartshill, Hanford, Stoke proper)</strong> — University of Keele student moves and family relocations alike. We do a lot of August student work here.",
                "<strong>ST5 (Newcastle-under-Lyme)</strong> — technically a separate borough, see our <a href='removals-newcastle-under-lyme.html'>Newcastle removals page</a>.",
                "<strong>ST6 (Burslem, Tunstall, Sneyd Green)</strong> — our depot postcode. Burslem's older terraces and Sneyd Green's estates are weekly territory.",
                "<strong>ST7 (Kidsgrove, Talke, Audley)</strong> — northern boundary, often jobs that cross into Cheshire.",
             ]),
            ("Local knowledge that saves you money",
             [
                "Parking in Stoke is the difference between a smooth morning load and a chaotic one. Our crew leader will scope your street the day before if needed, talk to the council about a parking suspension where the load looks tight, and confirm whether we can stop the Luton outside or whether we'll need to shuttle.",
                "Most Stoke streets allow our 7.5-tonne to stand for the duration of a load — the exceptions are the steeper Burslem and Hanley terraces, where we'll downsize to a Luton and double the run if needed. We never add extra costs for these decisions; everything is fixed at survey.",
                "If you're moving into one of the newer Trentham Lakes or Westbury Park estates, we know the developer's parking restrictions and the resident-parking dispensation process. Mention it at booking and we'll handle the paperwork.",
             ]),
            ("Services for Stoke moves",
             [
                "Every Stoke-on-Trent move is covered by our standard residential removal service — <a href='../services/domestic-removals.html'>see what's included</a>. Add <a href='../services/packing-services.html'>packing</a> if you'd rather not pack yourself; add <a href='../services/storage-services.html'>storage</a> if your completion date is uncertain.",
                "Office and commercial moves around Hanley, the Cultural Quarter and the business parks at Trentham Lakes and Festival Park run on our <a href='../services/commercial-removals.html'>commercial relocation service</a> — usually weekend lifts so you're operational on Monday morning.",
                "Specialist <a href='../services/piano-removals.html'>piano removals</a> across the city — we've moved everything from upright Yamahas in Birches Head to a Steinway grand out of a Trentham townhouse.",
             ]),
        ],
        'faqs': [
            ("How much does a Stoke-on-Trent house move cost?",
             "Most 2–3 bed local moves within Stoke fall between £450 and £950. Larger 4-bed moves, packing service and storage are quoted on top. <a href='../quote.html'>Get your free quote</a>."),
            ("Which Stoke postcodes do you cover?",
             "All of ST1 through ST7 — the six towns of Stoke plus surrounding postcodes. Newcastle-under-Lyme (ST5) is covered separately on our <a href='removals-newcastle-under-lyme.html'>Newcastle page</a>."),
            ("Can you handle a move with very tight street parking?",
             "Yes — we'll scope the street the day before, downsize to a Luton if needed and handle any parking-suspension request with the council."),
            ("Do you do moves to and from the Cultural Quarter offices?",
             "Yes — Cultural Quarter and Hanley town centre commercial moves are usually run as out-of-hours weekend lifts. See our <a href='../services/commercial-removals.html'>commercial removals</a>."),
            ("How quickly can you book a Stoke move?",
             "We can often fit a local Stoke move within 1–2 weeks off-peak; 4–6 weeks during May–September. <a href='../quote.html'>Request a quote</a> and we'll confirm."),
        ],
    },
    {
        'slug': 'areas-covered/removals-newcastle-under-lyme.html',
        'town': 'Newcastle-under-Lyme',
        'title': 'Removals Newcastle-under-Lyme | NSR Removals',
        'desc': "Removals in Newcastle-under-Lyme — Newcastle, Kidsgrove, Audley, Madeley and Keele. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Newcastle-under-Lyme borough',
        'eyebrow': 'Newcastle-under-Lyme · ST5',
        'lead': "Newcastle-under-Lyme is the second-largest town in North Staffordshire and one of our busiest patches. From the Georgian centre to the university quarter at Keele, the family estates of Cross Heath and Bradwell, and the villages out to Audley and Madeley, our crews cover the whole borough — at a fixed price, with no surprises on the day.",
        'hero_img': 'estate-agent-handing-house-keys.jpg',
        'paras': [
            ("Newcastle borough moves done properly",
             [
                "Newcastle-under-Lyme borough sits just west of Stoke and stretches from the Cheshire border at Audley right down to the Trentham boundary. It's a borough of contrasts — Georgian high-street properties, post-war estates, modern executive new-builds and the rural villages that ring the borough.",
                "Our team has been moving Newcastle families since 2010. We're based 15 minutes away in Stoke-on-Trent so a crew is on your driveway in good time, with a clean Luton or 7.5-tonne and all the kit needed for the day.",
                "Newcastle's town centre access has tightened in recent years, with several streets going one-way and the bus gate on Ironmarket. We know the workarounds and the loading windows that work; just tell us your address and we'll plan accordingly.",
             ]),
            ("Newcastle borough postcodes we cover",
             [
                "<strong>ST5 1–3 (Newcastle town centre, Cross Heath, May Bank)</strong> — busy residential, mix of older properties and 1960s estates. Tight parking around the King's Avenue and Knutton areas.",
                "<strong>ST5 4 (Bradwell, Porthill)</strong> — family estates, easier access, regular work for us.",
                "<strong>ST5 5 (Keele, Silverdale)</strong> — Keele University student moves in August, plus family relocations in Silverdale.",
                "<strong>ST5 6 (Madeley, Onneley, Aston)</strong> — rural villages on the Cheshire border. We do a lot of rural moves here.",
                "<strong>ST5 7 (Audley, Halmer End, Bignall End)</strong> — northern villages, often jobs that combine into the Kidsgrove side of Stoke.",
                "<strong>ST5 9 (Westlands, Clayton)</strong> — established residential, often four-bedroom family moves.",
             ]),
            ("Why Newcastle picks us",
             [
                "We've been moving Newcastle families and businesses since 2010, and a large share of our work comes from personal recommendations — neighbours and friends who've used us before. The reasons are consistent: the fixed-price quote really is fixed, the crew is polite and professional, and there are no charges if your completion slips.",
                "We've worked with Newcastle estate agents over the years and many of them recommend us when their vendors and buyers ask for a removal company. If your agent has suggested us, mention it at booking — we'll let them know we've taken care of you.",
                "Keele University staff and students get a small discount on documented academic moves; ask for details when you book.",
             ]),
            ("Services in Newcastle",
             [
                "Most Newcastle moves run on our <a href='../services/domestic-removals.html'>residential removals service</a>. Office and commercial relocations around the Newcastle town centre and the Lymedale Business Park use our <a href='../services/commercial-removals.html'>commercial service</a>.",
                "If your completion date is uncertain (common with the larger Newcastle housing chains), our <a href='../services/storage-services.html'>storage service</a> at the Stoke depot is the safety net — we collect on the original date, store, and redeliver when your chain completes.",
                "<a href='../services/packing-services.html'>Packing services</a> are popular with the larger Westlands and Clayton family moves — full pack the day before saves a chaotic morning.",
             ]),
        ],
        'faqs': [
            ("How much does a Newcastle-under-Lyme house move cost?",
             "Most local Newcastle 2–3 bed moves fall between £450 and £950 depending on access, packing and storage. <a href='../quote.html'>Request a free quote</a>."),
            ("Do you cover Audley and Madeley?",
             "Yes — Audley, Halmer End, Madeley, Onneley, Aston, Betley — the whole western edge of the borough."),
            ("Can you do a Newcastle move at the weekend?",
             "Yes — Saturday and Sunday slots available; weekend pricing is the same as weekday for residential. Commercial out-of-hours by arrangement."),
            ("Do Keele students get a discount?",
             "Yes, a small discount on documented Keele University academic moves. Ask at booking."),
            ("How far ahead should I book a Newcastle move?",
             "4–6 weeks during May–September peak, 1–2 weeks off-peak. <a href='../quote.html'>Get your free quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-stafford.html',
        'town': 'Stafford',
        'title': 'Removals Stafford | NSR Removals &amp; Storage',
        'desc': "Removals in Stafford — Stafford, Gnosall, Penkridge, Brewood, Haughton. Family-run from Stoke, fixed price, fully covered.",
        'h1': 'Removals across Stafford and surrounding villages',
        'eyebrow': 'Stafford · ST16–ST21',
        'lead': "Stafford is the county town and one of the busier regional markets for our removal service. From the Georgian centre to the Doxey and Castle Town estates, the new-build developments at Beaconside, and the surrounding villages at Gnosall, Penkridge and Brewood — our team has been moving Stafford families and businesses since 2010.",
        'hero_img': 'loading-cardboard-removal-boxes.jpg',
        'paras': [
            ("Stafford moves with local know-how",
             [
                "Stafford is a 30-minute drive from our Stoke depot down the M6, but for the volume of work we do in the town we treat it as part of our home patch. A Stafford-based crew leader runs every Stafford job, so the team knows the access at the Greyfriars Way developments, the parking habits on Tixall Road, and the loading bays at Stafford railway station and the town centre.",
                "We cover the full ST16–ST21 range — the town itself, Doxey, Castle Town, Highfields, Stallbrook, Beaconside, plus the villages out to Gnosall, Penkridge, Brewood and Haughton.",
                "Stafford has grown rapidly with new estates at Doxey Fields, the Beaconside areas and the Marston Grange development off the A34. We've moved customers in and out of every one of these new-build estates — and we know the developer parking restrictions and the resident-permit process.",
             ]),
            ("Stafford postcodes we cover",
             [
                "<strong>ST16 (Stafford town, Castle Town, Tillington)</strong> — Stafford proper. Mix of Georgian, Victorian and 1970s housing. Town centre needs careful access planning.",
                "<strong>ST17 (Stafford south, Walton-on-the-Hill, Weeping Cross)</strong> — established residential, easier access, four-bedroom family homes.",
                "<strong>ST18 (Great Haywood, Little Haywood, Colwich, Milford)</strong> — village locations along the Trent &amp; Mersey Canal corridor.",
                "<strong>ST19 (Penkridge, Acton Trussell, Wheaton Aston)</strong> — Penkridge is one of our regular village stops, popular with commuters working in Stafford and Wolverhampton.",
                "<strong>ST20 (Gnosall, Bradeley, Adbaston)</strong> — rural villages, often farmhouse moves with longer access tracks.",
                "<strong>ST21 (Eccleshall)</strong> — see our <a href='removals-eccleshall.html'>dedicated Eccleshall page</a>.",
             ]),
            ("Office moves in Stafford",
             [
                "Stafford has a strong commercial base — the County Council, MoD Stafford, GE Energy, and several large legal and accounting practices. Our <a href='../services/commercial-removals.html'>commercial relocations service</a> covers all of them, with weekend and out-of-hours lifts the norm.",
                "We've also moved several of the smaller Stafford agencies and IT firms within the town as they've grown — typically a Friday-evening start, Saturday assembly, fully operational Monday morning.",
             ]),
            ("Services for Stafford moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> covers the great majority of Stafford work. <a href='../services/packing-services.html'>Packing</a> on request. <a href='../services/storage-services.html'>Storage</a> at our Stoke depot if your chain delays.",
                "Specialist <a href='../services/piano-removals.html'>piano removals</a> for the Stafford concert and amateur music community.",
            ]),
        ],
        'faqs': [
            ("How much does a Stafford house move cost?",
             "Most Stafford 2–3 bed moves fall between £500 and £1,050 depending on distance to your new property, packing and access. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover the villages around Stafford?",
             "Yes — Gnosall, Penkridge, Brewood, Haughton, Eccleshall and the surrounding rural lanes."),
            ("Can you handle a Stafford-to-Stoke move?",
             "Yes — that's a routine 30-minute corridor for us. Quoted on the standard residential service."),
            ("Do you have a Stafford depot?",
             "Our depot is in Stoke-on-Trent (Genesis Centre, ST6 4BF), 30 minutes up the M6. We treat Stafford as part of our home patch."),
            ("How quickly can you book a Stafford move?",
             "4–6 weeks during May–September; often 1–2 weeks off-peak. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-stone.html',
        'town': 'Stone',
        'title': 'Removals Stone | NSR Removals &amp; Storage',
        'desc': "Removals in Stone, Staffordshire — Stone, Walton, Aston, Yarnfield and Barlaston. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Stone and the Trent Valley',
        'eyebrow': 'Stone · ST15',
        'lead': "Stone is one of the most picturesque market towns in Staffordshire and a regular stop for our removal crews. From the Georgian properties on the High Street to the larger family homes at Walton and Aston, and the canalside developments at Barlaston, our team has been moving Stone customers since 2010.",
        'hero_img': 'couple-unpacking-boxes-new-home.jpg',
        'paras': [
            ("Stone moves with care and local knowledge",
             [
                "Stone sits midway between Stoke and Stafford, with the Trent &amp; Mersey Canal running through it. It's a town with character — Georgian sash windows, narrow streets, and the unmistakable canalside atmosphere that draws people from across the Midlands.",
                "That character is also what makes Stone moves a little trickier than average. The High Street and the side streets off it are tight; some properties have rear-only access via a canal path. Our crew always surveys these before the move, and where access is exceptional we'll send a smaller Luton and run extra trips rather than trying to force a 7.5-tonne onto a narrow lane.",
                "We cover the whole ST15 postcode — Stone town, Walton, Aston-by-Stone, Yarnfield, Barlaston, Tittensor and the surrounding villages out to the boundary with Stafford and Stoke.",
             ]),
            ("Stone postcodes we cover",
             [
                "<strong>ST15 0–7 (Stone town centre, Walton, Aston, Yarnfield, Barlaston)</strong> — our regular Stone territory, full residential service.",
                "<strong>ST15 8–9 (Tittensor, Saverley Green, Hilderstone)</strong> — village properties with sometimes-tricky access. We'll survey ahead.",
             ]),
            ("Why Stone moves are different",
             [
                "Stone's canalside properties often have unusual access — front-door street-side, but the only way to load is via a rear garden path that opens onto the towpath. We've moved a number of these and we know which streets allow vehicle access to the back, and which require a long walk-out to a parked van.",
                "The town's growing fast, with new developments at the Walton fringe and along the A34 to Stoke. We've moved into nearly every new-build estate around Stone and know the developer access rules.",
             ]),
            ("Services for Stone moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> is the standard service for Stone — fixed price, fully covered, free survey.",
                "<a href='../services/packing-services.html'>Packing services</a> particularly popular with the larger Walton and Aston family moves; <a href='../services/storage-services.html'>storage</a> useful for the canalside completions where the chain is uncertain.",
                "<a href='../services/piano-removals.html'>Piano removals</a> — the Stone musical community is active and we handle several piano moves a year here.",
             ]),
        ],
        'faqs': [
            ("Do you do Stone canalside property moves?",
             "Yes — we survey access ahead and use a smaller Luton if the rear access is tight. Pricing fixed at survey."),
            ("How much does a Stone house move cost?",
             "Most Stone 2–3 bed moves fall between £450 and £950. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Barlaston and Yarnfield?",
             "Yes — both are in ST15 and on our regular run."),
            ("Can you store between completions for a Stone move?",
             "Yes — our Stoke depot has palletised storage units, charged by the week. <a href='../services/storage-services.html'>See storage</a>."),
            ("How quickly can you fit in a Stone move?",
             "4–6 weeks peak, 1–2 weeks off-peak. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-leek.html',
        'town': 'Leek',
        'title': 'Removals Leek | NSR Removals &amp; Storage',
        'desc': "Removals in Leek and the Staffordshire Moorlands — Leek, Cheddleton, Werrington, Endon, Wetley Rocks. Family-run, fixed price.",
        'h1': 'Removals across Leek and the Staffordshire Moorlands',
        'eyebrow': 'Leek · ST13',
        'lead': "Leek is the capital of the Staffordshire Moorlands, perched on the edge of the Peak District. Our team has been moving Moorlands families for over a decade, and we know the lanes, the access, and the weather quirks that make this corner of Staffordshire special.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Moves across the Staffordshire Moorlands",
             [
                "The Moorlands is the most rural part of our patch — narrow lanes, farmhouse driveways, stone cottages with low door frames, and the changeable Peak District weather. Our crews enjoy these jobs precisely because they're different: every Moorlands move teaches us something.",
                "Our Stoke depot is a 25-minute drive from Leek down the A53. From the Leek depot turn-off we cover the whole ST13 postcode — Leek town, Cheddleton, Wetley Rocks, Werrington, Endon, Brown Edge, Longsdon, and the smaller hamlets out to the Roaches and Tittesworth Reservoir.",
                "We've moved farmhouses, stone cottages, riverside properties at Rudyard Lake, and the modern estates at the Birchall and Cornhill developments. Every one has its own access story — and our team plans accordingly.",
             ]),
            ("Leek and Moorlands postcodes",
             [
                "<strong>ST13 5–6 (Leek town, Birchall, Westwood)</strong> — town centre with Georgian terraces and the Market Square. Tight access in places, easy in others.",
                "<strong>ST13 7 (Cheddleton, Wetley Rocks, Longsdon)</strong> — village locations along the A520 corridor. Mostly easy access.",
                "<strong>ST13 8 (Werrington, Cellarhead, Endon)</strong> — popular family villages, often estate housing with straightforward access.",
                "<strong>ST10 (Cheadle, Tean, Kingsley)</strong> — Moorlands towns to the south. We cover these too — give us a postcode and we'll quote.",
             ]),
            ("Moorlands weather and access tips",
             [
                "The Moorlands sit at 800–1,500ft above sea level and the weather can change in an hour. We monitor the forecast for Moorlands moves and will move you a day earlier if heavy snow is forecast for completion day. That's a free service — no extra charge for a weather-related date change.",
                "Many Moorlands farmhouses sit at the end of a quarter-mile gravel track. We'll survey ahead and either use a smaller Luton with multiple runs, or arrange a shuttle from the road end. Our pricing is fixed once we've seen the access.",
                "Stone cottage doorways are often lower than modern standards. We measure your largest item (usually a wardrobe or three-seater sofa) against the new property's tightest doorway at survey, and confirm it'll fit. If not, we know carpenters and locksmiths who can help.",
             ]),
            ("Services for Leek and Moorlands moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for all of ST13. <a href='../services/packing-services.html'>Packing services</a> particularly popular with farmhouse moves (large volume + Moorlands distance = full pack saves time).",
                "<a href='../services/storage-services.html'>Storage</a> at our Stoke depot — useful for Moorlands customers between completions; we collect from the Moorlands and store in Stoke.",
                "<a href='../services/piano-removals.html'>Piano removals</a> — the Leek music community is active and we handle several piano jobs a year in the Moorlands.",
             ]),
        ],
        'faqs': [
            ("Can you handle a farmhouse move in the Moorlands?",
             "Yes — we'll survey the access track and confirm vehicle size. Often a Luton with two runs is the right answer rather than a 7.5-tonne stuck on a track."),
            ("How much does a Leek move cost?",
             "Most Leek 2–3 bed moves fall between £550 and £1,150, with the surcharge over Stoke pricing being the extra distance and access time. <a href='../quote.html'>Get a free quote</a>."),
            ("What if the weather turns on completion day?",
             "We monitor Moorlands forecasts and will move you a day earlier free of charge if heavy snow or ice is forecast. No charge for weather-related date changes."),
            ("Do you cover Cheadle and Tean?",
             "Yes — ST10 is on our patch. Mentioned above; <a href='../quote.html'>request a quote</a>."),
            ("Is my move fully covered in the Moorlands?",
             "Yes — full Goods in Transit and £10m Public Liability everywhere we operate. Claims handled directly by our team."),
        ],
    },
    {
        'slug': 'areas-covered/removals-eccleshall.html',
        'town': 'Eccleshall',
        'title': 'Removals Eccleshall | NSR Removals &amp; Storage',
        'desc': "Removals in Eccleshall and the villages of west Staffordshire. Family-run, fixed price, fully covered. Call 01782 939124.",
        'h1': 'Removals across Eccleshall and west Staffordshire',
        'eyebrow': 'Eccleshall · ST21',
        'lead': "Eccleshall is one of the prettiest market towns in west Staffordshire and a regular destination for our removal crews. From the Georgian High Street to the surrounding villages of Slindon, Knightley, Cotes Heath and Standon, we've been moving Eccleshall families since 2010.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Eccleshall moves with a careful touch",
             [
                "Eccleshall (pronounced 'Eck-uls-hall' locally — getting that right is half the battle) is a historic market town with a striking castle, a wide Georgian High Street and some of the most desirable rural housing in Staffordshire. Many properties are listed; many have access via narrow rear cobbled lanes; many have valuable antiques inside.",
                "Our crews are used to all of this. Pad-wrapping every piece in the home, slow careful loading, the right kit (skid boards, blanket wraps, corner protectors), and a fixed price agreed at survey. No hourly billing, no last-minute extras.",
                "From our Stoke depot we run down the A519 to Eccleshall in about 35 minutes. The surrounding villages — Slindon, Knightley, Cotes Heath, Standon, Croxton — are all on our regular run.",
             ]),
            ("Eccleshall postcodes and villages",
             [
                "<strong>ST21 6 (Eccleshall town, High Offley, Outlands)</strong> — town centre and immediate villages. Mix of Georgian properties and modern estate housing on the town fringe.",
                "<strong>ST21 7 (Slindon, Knightley, Cotes Heath, Standon)</strong> — rural village properties, often with antique furniture and longer access tracks.",
             ]),
            ("Antique-rich moves",
             [
                "A high proportion of Eccleshall properties contain valuable antiques — Welsh dressers, longcase clocks, period chests, oil paintings, ceramics. Our crew is trained in handling these, and we'll bring corner protectors, blanket wraps and bespoke crates as needed.",
                "For very high-value pieces we recommend a separate antique inventory at survey, photographed and condition-noted, with cover confirmed in writing. <a href='../services/domestic-removals.html'>Standard cover</a> handles most cases; bespoke arrangements for items over £10,000 individual value.",
             ]),
            ("Services for Eccleshall moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full ST21 area. <a href='../services/packing-services.html'>Packing services</a> particularly popular here — many customers prefer the professional pack option for the kitchen and china.",
                "<a href='../services/storage-services.html'>Storage</a> at our Stoke depot if your chain delays. <a href='../services/piano-removals.html'>Piano removals</a> for the strong Eccleshall musical community.",
             ]),
        ],
        'faqs': [
            ("Do you handle antique-furniture moves in Eccleshall?",
             "Yes — extensive experience with Welsh dressers, longcase clocks, period chests and oil paintings. Bespoke crating for high-value pieces."),
            ("How much does an Eccleshall move cost?",
             "Most Eccleshall 2–3 bed moves fall between £550 and £1,100. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Slindon and Standon?",
             "Yes — both villages are in ST21 and on our regular run."),
            ("Can my high-value antiques be specifically insured?",
             "Yes — we'll list them separately at survey and confirm bespoke cover in writing for pieces over £10,000 individual value."),
            ("How far ahead should I book?",
             "4–6 weeks peak season, 1–2 weeks off-peak. <a href='../quote.html'>Request a free quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-burton-on-trent.html',
        'town': 'Burton-on-Trent',
        'title': 'Removals Burton-on-Trent | NSR Removals &amp; Storage',
        'desc': "Removals in Burton-on-Trent — Burton, Stretton, Branston, Barton-under-Needwood. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Burton-on-Trent and east Staffordshire',
        'eyebrow': 'Burton-on-Trent · DE13–DE15',
        'lead': "Burton-on-Trent is the gateway between Staffordshire and Derbyshire — a busy market town with strong commuter links to Birmingham, Derby and Stoke. Our team has been moving Burton families and businesses for over a decade, and we treat the DE13–DE15 postcodes as part of our regular Staffordshire patch.",
        'hero_img': 'loading-cardboard-removal-boxes.jpg',
        'paras': [
            ("Burton moves done the local way",
             [
                "Burton-on-Trent sits 45 minutes south-east of our Stoke depot down the A50. For the volume of Burton work we do — both residential and commercial — we keep a Burton-savvy crew on standby and a dedicated route plan that avoids the worst of the A38 morning peak.",
                "We cover Burton town centre, the established estates at Winshill, Stretton and Branston, the newer developments at Branston Locks and Stretton Park, and the surrounding villages of Barton-under-Needwood, Newborough and Tutbury.",
                "Burton's housing market has grown rapidly thanks to its commuter links and the value-for-money property prices vs. Birmingham and Derby. We've moved a lot of customers <em>into</em> Burton over the last few years, often from longer-distance origins like Manchester, Leicester and Coventry.",
             ]),
            ("Burton postcodes we cover",
             [
                "<strong>DE13 (Burton centre, Barton-under-Needwood, Tutbury)</strong> — main Burton residential.",
                "<strong>DE14 (Burton south, Stretton, Branston, Branston Locks)</strong> — busy commuter belt with new-build estates.",
                "<strong>DE15 (Winshill, Stapenhill)</strong> — east Burton, established residential.",
                "Plus the Staffordshire border villages on the Burton fringe — Newborough, Yoxall, Anslow and Rolleston-on-Dove.",
             ]),
            ("Long-distance moves into Burton",
             [
                "A significant share of our Burton work is long-distance arrivals — customers moving from Manchester, Birmingham, Leicester or further afield. We handle these on a planned overnight basis: load at the origin one day, overnight in our depot, deliver to Burton the next morning. Insurance unchanged, fixed price.",
                "Long-distance pricing is quoted on a fixed basis per move (not per mile) so you know exactly what you'll pay. <a href='../quote.html'>Request a quote</a> with your origin and destination postcodes.",
             ]),
            ("Services for Burton moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full DE13–DE15 patch. <a href='../services/packing-services.html'>Packing</a> on request. <a href='../services/storage-services.html'>Storage</a> at our Stoke depot.",
                "<a href='../services/commercial-removals.html'>Commercial removals</a> for Burton businesses — particularly active in the food, drink and pharmaceutical sectors that cluster around the town.",
             ]),
        ],
        'faqs': [
            ("How much does a Burton-on-Trent move cost?",
             "Most local Burton 2–3 bed moves fall between £550 and £1,150 (the surcharge over Stoke pricing reflecting the distance from our depot). <a href='../quote.html'>Get a free quote</a>."),
            ("Do you do long-distance moves into Burton?",
             "Yes — Manchester, Birmingham, Leicester and further afield, planned on a fixed-price overnight basis."),
            ("Do you cover Barton-under-Needwood and Tutbury?",
             "Yes — both villages are on our regular Burton run."),
            ("Can you do commercial moves in Burton?",
             "Yes — particularly active in the food, drink and pharmaceutical sectors. Weekend lifts standard."),
            ("How quickly can you book a Burton move?",
             "4–6 weeks peak; 1–2 weeks off-peak. <a href='../quote.html'>Request a free quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-buxton.html',
        'town': 'Buxton',
        'title': 'Removals Buxton | NSR Removals &amp; Storage',
        'desc': "Removals in Buxton and the Peak District towns over the Staffordshire border. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Buxton and the High Peak',
        'eyebrow': 'Buxton · SK17',
        'lead': "Buxton sits just over the Staffordshire border in Derbyshire, at the heart of the Peak District National Park. Our removal team has been working the High Peak for over a decade, and we know the unique challenges of moving in and around Buxton — the weather, the access, and the stone-built character of the town's properties.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Peak District moves with experience",
             [
                "Buxton is the highest market town in England at 1,000 feet above sea level — and the weather acts accordingly. Our crews monitor the forecast for every Buxton job and we'll happily move you a day earlier or later free of charge if heavy snow is forecast. That's how we've built our reputation across the Moorlands and the Peaks.",
                "From our Stoke depot it's about 50 minutes up the A53 to Buxton — a route we know intimately. We cover the SK17 postcode (Buxton town and surrounding villages) plus the nearby Peak District towns of Bakewell, Chapel-en-le-Frith and Hartington.",
                "Buxton's housing stock is dominated by stone-built Georgian and Victorian properties — many with narrow doorways and low ceilings. We measure your largest items against doorway clearances at survey, and confirm everything will fit before we book the job.",
             ]),
            ("Buxton and High Peak postcodes",
             [
                "<strong>SK17 6 (Buxton town centre, Burbage, Harpur Hill)</strong> — Georgian town centre with sometimes-tight access.",
                "<strong>SK17 7 (Buxton fringe, Fairfield, Cowdale)</strong> — established residential.",
                "<strong>SK17 8 (Tideswell, Litton, Earl Sterndale)</strong> — Peak District villages with narrow lanes.",
                "<strong>SK17 9 (Whaley Bridge fringe, Combs)</strong> — Peak District fringe.",
                "Plus surrounding High Peak towns — Bakewell, Chapel-en-le-Frith, Hartington, Hayfield — quoted on a case-by-case basis.",
             ]),
            ("Weather and stone-building considerations",
             [
                "Snow forecast for completion day? We move you a day earlier, free of charge. This is the single most appreciated service we offer in the High Peak — customers know we won't let the weather wreck their move.",
                "Stone-built Buxton properties often have doorways and stairs narrower than modern standards. Wardrobes, three-seater sofas and dining tables sometimes need dismantling for access. We'll measure at survey and confirm.",
                "Steep cobbled or gravel access tracks are common across the Peaks. We'll use a smaller Luton with multiple runs rather than a 7.5-tonne where access requires it — without changing the fixed price agreed at survey.",
             ]),
            ("Services for Buxton moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for SK17 and the surrounding High Peak. <a href='../services/packing-services.html'>Packing services</a> particularly useful here — many Buxton customers value the time saved.",
                "<a href='../services/storage-services.html'>Storage</a> at our Stoke depot — particularly useful for Buxton chain delays where Peak weather adds uncertainty.",
                "<a href='../services/piano-removals.html'>Piano removals</a> for the active Buxton musical community (Opera House and the Festival).",
             ]),
        ],
        'faqs': [
            ("What if it snows on my Buxton completion day?",
             "We monitor the forecast and will move you a day earlier free of charge if heavy snow is forecast. No weather-related surcharges."),
            ("How much does a Buxton move cost?",
             "Most Buxton 2–3 bed moves fall between £650 and £1,250 (surcharge over Stoke reflecting distance and Peak access). <a href='../quote.html'>Get a free quote</a>."),
            ("Can you handle a stone-built property with narrow access?",
             "Yes — we measure largest items against doorway clearance at survey, and dismantle as needed (free of charge)."),
            ("Do you cover Bakewell and Chapel-en-le-Frith?",
             "Yes — both quoted on a case-by-case basis. <a href='../quote.html'>Request a quote</a>."),
            ("Is my Buxton move covered for damage?",
             "Yes — full Goods in Transit insurance and £10m Public Liability. Claims handled directly by our team."),
        ],
    },

    # ───────── 12 additional area pages (added 2026-05-24) ─────────
    {
        'slug': 'areas-covered/removals-hanley.html',
        'town': 'Hanley',
        'title': 'Removals Hanley | NSR Stoke-on-Trent',
        'desc': "Removals in Hanley, Stoke-on-Trent city centre — ST1 postcode. Family-run, fixed price, fully covered. Call 01782 939124.",
        'h1': 'Removals across Hanley and Stoke-on-Trent city centre',
        'eyebrow': 'Hanley · ST1',
        'lead': "Hanley is the commercial heart of Stoke-on-Trent and one of our most-served postcodes. From the apartments above the Cultural Quarter to the terraces of Northwood and the family estates of Birches Head, our crews move Hanley households and offices to time and to a fixed quote, every working day of the year.",
        'hero_img': 'couple-unpacking-boxes-new-home.jpg',
        'paras': [
            ("Hanley moves with city-centre expertise",
             [
                "Hanley is the busiest of the six towns of Stoke-on-Trent &mdash; the commercial centre, the Cultural Quarter, the new-build apartment developments around Smithfield, and the established residential streets stretching north to Cobridge and Northwood and east to Birches Head. From our depot just up the road in Sneyd Green, we run multiple Hanley jobs every week and we know the city centre's access quirks intimately.",
                "Parking is the big variable for any Hanley move. The town-centre streets are tight, the loading windows are short, and several routes are one-way or pedestrianised. Our crew leader scopes your specific street the day before and arranges a council parking suspension where the load requires it &mdash; included in your fixed price, never added as an extra on the day.",
                "Hanley's mix of Victorian terraces, post-war estates and modern apartments means every move is a different access puzzle. We bring the right vehicle for the job &mdash; small Luton for the tight terraced streets, 7.5-tonne for the apartment moves with lift access, and the experience to switch plans on the day if the council closes the road we'd planned to use.",
             ]),
            ("Hanley postcodes and neighbourhoods we cover",
             [
                "<strong>ST1 1 (Hanley town centre, Cultural Quarter, Smithfield)</strong> &mdash; commercial heart with modern apartments above the high street. Out-of-hours loading often needed.",
                "<strong>ST1 2 (Northwood, Eastwood, Birches Head)</strong> &mdash; residential terraces and 1970s estates. Easier parking, larger volumes.",
                "<strong>ST1 3 (Birches Head fringe, Sneyd Green border)</strong> &mdash; established family estates with garden access.",
                "<strong>ST1 4 (Cobridge, Etruria, Festival Park fringe)</strong> &mdash; mixed terraces and newer developments around Festival Park.",
                "<strong>ST1 5/6 (Hanley north fringe, Burslem border)</strong> &mdash; transitions into Burslem; see our <a href='removals-burslem.html'>Burslem page</a> for that side.",
             ]),
            ("Office and apartment moves in central Hanley",
             [
                "Many of our Hanley jobs are office relocations &mdash; legal practices, accountants, design studios and start-ups based in the Cultural Quarter or above retail on Stafford Street and Piccadilly. These run on our <a href='../services/commercial-removals.html'>commercial service</a>, almost always with weekend or evening lifts so the team is operational on Monday morning.",
                "Apartment moves in central Hanley are usually 1- or 2-bedroom units in the Smithfield and Etruria new-builds. We schedule lift access with the building management, lay floor runners through every common area, and aim to load and unload inside the booked lift window. Most apartment moves complete in 4-6 hours including travel.",
             ]),
            ("Services for Hanley moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> covers the great majority of Hanley work &mdash; everything from a one-bed Smithfield apartment to a 4-bed Birches Head family home. Add <a href='../services/packing-services.html'>packing</a> if the kitchen feels too much; add <a href='../services/storage-services.html'>storage</a> if your completion date is uncertain.",
                "<a href='../services/commercial-removals.html'>Commercial relocations</a> for Hanley businesses run as weekend lifts with IT decommission, crate hire and full reassembly Monday-ready.",
                "<a href='../services/man-and-van.html'>Man &amp; van</a> for smaller Hanley jobs &mdash; student moves, single-item collections, IKEA deliveries.",
             ]),
        ],
        'faqs': [
            ("How much does a Hanley house move cost?",
             "Most Hanley 1-3 bed moves fall between £400 and £900. Apartment moves in the Smithfield new-builds run at the lower end; family homes in Birches Head and Northwood at the upper end. <a href='../quote.html'>Get a free quote</a>."),
            ("Can you handle a Hanley city-centre office move?",
             "Yes &mdash; weekend and out-of-hours lifts are standard for our Hanley commercial moves. We coordinate with building management on lift booking and loading-bay access."),
            ("Do you arrange parking suspensions on tight Hanley streets?",
             "Yes &mdash; included in our fixed quote where the load requires it. We handle the council application a week ahead."),
            ("How quickly can you book a Hanley move?",
             "We can often fit a local Hanley move within 1-2 weeks off-peak; 4-6 weeks during May-September peak. <a href='../quote.html'>Request a quote</a>."),
            ("Do you cover the Cultural Quarter apartments?",
             "Yes &mdash; Smithfield, the Cultural Quarter and the surrounding new-builds are weekly territory for us."),
        ],
    },
    {
        'slug': 'areas-covered/removals-burslem.html',
        'town': 'Burslem',
        'title': 'Removals Burslem | NSR Stoke-on-Trent',
        'desc': "Removals in Burslem &mdash; Mother of the Potteries. ST6 postcode, family-run, fixed price, fully covered. Call 01782 939124.",
        'h1': 'Removals across Burslem &mdash; the Mother of the Potteries',
        'eyebrow': 'Burslem · ST6',
        'lead': "Burslem &mdash; the Mother of the Potteries &mdash; sits at the heart of our home patch. Our depot is a five-minute drive from the Burslem town centre and we move dozens of Burslem households and pottery-quarter businesses each year. The Victorian terraces and steep streets are the daily challenge; the local knowledge to handle them is the daily answer.",
        'hero_img': 'estate-agent-handing-house-keys.jpg',
        'paras': [
            ("Burslem moves done by people who live here",
             [
                "Burslem is the oldest of the six towns of Stoke-on-Trent, with a heritage stretching back to the Industrial Revolution. That history shows in the housing stock &mdash; Victorian potters' terraces lining the steeper streets, mid-century estates spreading out toward Tunstall and Sneyd Green, and a growing crop of new-build developments around the town's industrial fringes.",
                "Our crews are based five minutes away in ST6 and most of them grew up in or around the Burslem postcodes. They know which streets allow a 7.5-tonne to stand for a full load, which ones need a smaller Luton with a shuttle, and where the loading bays are at the back of the Wedgwood Institute and the Burslem market. That local knowledge translates into time saved and stress avoided on your move day.",
                "Burslem's terraced streets are famous for their steep camber and tight cobbled rear access. Our standard approach: scope the street the day before, use a smaller Luton and two trips rather than fighting a 7.5-tonne onto a narrow lane, and protect every doorway and stair-end with floor runners and corner-guards. No surprises on the day, no extra fees.",
             ]),
            ("Burslem postcodes and access notes",
             [
                "<strong>ST6 1 (Burslem town centre, Market Place, Queen Street)</strong> &mdash; tight Victorian terraces with cobbled rear access. Almost always a smaller-vehicle job.",
                "<strong>ST6 2 (Middleport, Longport)</strong> &mdash; canalside potteries area with mixed terraces and modern infill. Some restricted-vehicle streets.",
                "<strong>ST6 3 (Burslem north, Sneyd Green border)</strong> &mdash; family terraces stretching north toward our depot.",
                "<strong>ST6 4 (Tunstall border, Park Hall)</strong> &mdash; transitions into Tunstall; see our <a href='removals-tunstall.html'>Tunstall page</a>.",
                "<strong>ST6 5/6/7 (Cobridge, Smallthorne, Brownhills)</strong> &mdash; family estates with easier access and larger volumes.",
                "<strong>ST6 8 (Burslem fringe to Goldenhill)</strong> &mdash; northern edge transitioning toward Kidsgrove.",
             ]),
            ("Pottery-trail and heritage-property moves",
             [
                "Burslem's pottery heritage means a non-trivial number of our jobs involve significant ceramic collections &mdash; family pieces, Wedgwood and Royal Doulton sets, contemporary studio ceramics from the local craft scene. Our team handles these with specialist bubble-wrap technique, cell-divider cartons for glazed pieces, and bespoke crating for any individually-valued piece over £500. Mention the collection at survey so we can plan accordingly.",
                "We also move customers in and out of the converted-pottery loft apartments that have appeared around Middleport and Longport in the last decade. These typically have lift access to upper floors and tight corridor turns &mdash; we measure your largest piece against the tightest corner at survey and confirm whether dismantling is needed.",
             ]),
            ("Services for Burslem moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full ST6 range &mdash; tight terraces to four-bed family homes. <a href='../services/packing-services.html'>Fragile-only packing</a> particularly popular here given the ceramics collections.",
                "<a href='../services/storage-services.html'>Storage</a> at our nearby depot for between-completion gaps. <a href='../services/piano-removals.html'>Piano removals</a> for the active Burslem music scene.",
                "<a href='../services/antiques-moving.html'>Antiques moving</a> with bespoke crating for valuable ceramics or period furniture.",
             ]),
        ],
        'faqs': [
            ("How much does a Burslem house move cost?",
             "Most Burslem 2-3 bed moves fall between £450 and £900. Larger 4-bed homes or jobs with significant ceramics collections quoted on top. <a href='../quote.html'>Get a free quote</a>."),
            ("Can you handle a tight Victorian terrace in Burslem?",
             "Yes &mdash; we scope the street ahead and use a smaller Luton with two trips where a 7.5-tonne won't fit safely. No extra charge for the smaller vehicle choice."),
            ("Do you have experience with pottery and ceramics collections?",
             "Yes &mdash; bespoke wrapping, cell-divider cartons and bespoke crating for individual pieces over £500. Mention the collection at survey."),
            ("Do you cover Cobridge, Middleport and Sneyd Green?",
             "Yes &mdash; all within ST6 and on our daily run. Sneyd Green is our depot postcode."),
            ("How quickly can you book a Burslem move?",
             "Off-peak: often within a week. Peak (May-September): 4-6 weeks ahead recommended. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-tunstall.html',
        'town': 'Tunstall',
        'title': 'Removals Tunstall | NSR Stoke-on-Trent',
        'desc': "Removals in Tunstall, Stoke-on-Trent &mdash; ST6 postcode. Family-run, fixed price, fully covered. Call 01782 939124.",
        'h1': 'Removals across Tunstall and the northern Potteries',
        'eyebrow': 'Tunstall · ST6',
        'lead': "Tunstall is the northernmost of the six towns of Stoke-on-Trent and one of the friendlier patches to move through &mdash; family estates, established residential streets and a town centre with a working market. Our crews live and breathe ST6 from our nearby depot, and we handle Tunstall moves with the same fixed-price, family-run promise as everywhere else.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Tunstall moves with local know-how",
             [
                "Tunstall has retained more of its independent town-centre character than the bigger Hanley or Burslem — Market Place still hosts a working market four days a week, and the surrounding residential streets are dominated by Victorian terraces and post-war family estates rather than apartment blocks. That mix makes Tunstall removals broadly straightforward: most jobs are full-family-home moves with cooperative parking and good access.",
                "From our depot in adjacent ST6 we run Tunstall jobs daily. The handful of tricky streets — usually the older terraced rows near the Goldenhill border — get a smaller Luton and a shuttle rather than a 7.5-tonne fighting for kerbspace. Everything else handles cleanly.",
             ]),
            ("Tunstall postcodes and neighbourhoods",
             [
                "<strong>ST6 5 (Tunstall town centre, Market Place)</strong> — mix of older terraces and modern apartments above shops. Some tight access; usually fine with a Luton.",
                "<strong>ST6 6 (Cross Street, Pinnox Street area)</strong> — Victorian residential streets.",
                "<strong>ST6 7 (Brownhills, Newfield, Goldenhill border)</strong> — family estates with easier parking.",
                "Tunstall borders <a href='removals-kidsgrove.html'>Kidsgrove</a> to the north and <a href='removals-burslem.html'>Burslem</a> to the south; cross-border moves are routine for us.",
             ]),
            ("What makes Tunstall straightforward to move in",
             [
                "Tunstall's housing stock is dominated by 2- and 3-bed family terraces and estate semis — exactly the size range that fits comfortably in a single Luton or 7.5-tonne with a 3-person crew. Most of our Tunstall moves complete within a working day and bill at the lower-to-middle end of our Stoke pricing.",
                "Parking on most Tunstall residential streets is reasonable — no resident-permit zones, generally enough kerbspace for our vehicles. The town centre Market Place area has timed loading restrictions; we plan around them when the move involves a town-centre flat.",
             ]),
            ("Services for Tunstall moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full ST6 5-7 range. <a href='../services/packing-services.html'>Packing</a> on request — many Tunstall family-home customers value the time saving.",
                "<a href='../services/storage-services.html'>Storage</a> at our nearby depot if your chain delays. <a href='../services/man-and-van.html'>Man &amp; van</a> for smaller Tunstall jobs.",
             ]),
        ],
        'faqs': [
            ("How much does a Tunstall house move cost?",
             "Most Tunstall 2-3 bed moves fall between £450 and £850. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Brownhills and Goldenhill?",
             "Yes — both within ST6 and on our regular Tunstall run."),
            ("Can you handle Market Place flats above shops?",
             "Yes — we coordinate with the loading-restriction windows and use a smaller vehicle if needed."),
            ("How quickly can you book a Tunstall move?",
             "Off-peak: often within a week. Peak season: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
            ("Is my Tunstall move fully covered?",
             "Yes — full Goods in Transit insurance and £10m Public Liability cover."),
        ],
    },
    {
        'slug': 'areas-covered/removals-longton.html',
        'town': 'Longton',
        'title': 'Removals Longton | NSR Stoke-on-Trent',
        'desc': "Removals in Longton, Stoke-on-Trent &mdash; ST3 postcode. Family-run, fixed price, fully covered. Call 01782 939124.",
        'h1': 'Removals across Longton and southern Stoke-on-Trent',
        'eyebrow': 'Longton · ST3',
        'lead': "Longton is the southernmost of the six towns of Stoke-on-Trent, sitting along the A50 corridor with strong commuter links into Stafford and Derby. Our crews cover the full ST3 postcode &mdash; town centre, Meir, Blurton and Trentham Lakes &mdash; with fixed-price quotes and local knowledge built over fifteen years.",
        'hero_img': 'loading-cardboard-removal-boxes.jpg',
        'paras': [
            ("Longton moves with A50 corridor experience",
             [
                "Longton is the gateway town between Stoke-on-Trent proper and the south Staffordshire commuter belt &mdash; the A50 runs through it and many residents commute east to Derby or west to Stafford. The town's housing stock reflects that commuter character: a mix of older terraces in the town centre, large post-war estates in Meir and Blurton, and substantial new-build developments around Trentham Lakes that have grown rapidly over the last decade.",
                "Our depot is fifteen minutes north and we run Longton jobs daily. The town-centre terraces follow the same pattern as the rest of central Stoke &mdash; tight, cobble-rear-access in places &mdash; while the Meir, Blurton and Trentham Lakes estates handle cleanly with standard 7.5-tonne access. We size the vehicle to the job at survey.",
                "Trentham Lakes in particular is one of our most-served new-build areas in the city. We've moved customers into nearly every phase of the development and we know the on-site parking restrictions and resident-permit dispensation process at each estate.",
             ]),
            ("Longton postcodes and neighbourhoods",
             [
                "<strong>ST3 1 (Longton town centre, Heron Cross)</strong> &mdash; older terraces and town-centre flats.",
                "<strong>ST3 2 (Blurton, Trentham Lakes)</strong> &mdash; major new-build territory with good vehicle access.",
                "<strong>ST3 3 (Meir Park, Forsbrook)</strong> &mdash; established 1980s estates plus newer Meir Park infill.",
                "<strong>ST3 4-7 (Meir core, Sandford Hill, Bentilee)</strong> &mdash; mix of post-war estates and family terraces.",
             ]),
            ("New-build moves in Trentham Lakes",
             [
                "Trentham Lakes has been the city's busiest new-build development for the last decade. We've moved customers in and out of nearly every phase and we know the developer parking restrictions at each estate. The standard pattern: limited on-street parking around the show homes, requirement to load from a designated bay, and a resident permit needed for our crew vehicle on the day. We handle the permit paperwork as part of the booking.",
                "If you're moving into Trentham Lakes from an older Stoke postcode, mention it at quote stage. We'll plan for any access constraints at the new property and confirm the resident-permit arrangement before booking.",
             ]),
            ("Services for Longton moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full ST3 range. <a href='../services/packing-services.html'>Packing service</a> popular with the larger Meir and Blurton family homes. <a href='../services/storage-services.html'>Storage</a> at our nearby depot for chain-delay scenarios.",
                "<a href='../services/man-and-van.html'>Man &amp; van</a> for smaller Longton jobs &mdash; student moves at Staffordshire University's outreach campuses, single-item collections, IKEA-day deliveries.",
             ]),
        ],
        'faqs': [
            ("How much does a Longton house move cost?",
             "Most Longton 2-3 bed moves fall between £450 and £900. Trentham Lakes new-build moves typically at the upper end given the volume of contents. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you handle Trentham Lakes developer parking?",
             "Yes &mdash; we handle the resident-permit application as part of the booking, no extra cost."),
            ("Do you cover Meir, Blurton and Bentilee?",
             "Yes &mdash; all within ST3 and on our daily run."),
            ("Can you handle moves between Longton and Derby/Stafford commuter towns?",
             "Yes &mdash; A50-corridor moves are routine for us, both inbound and outbound."),
            ("How quickly can you book a Longton move?",
             "Off-peak: often within a week. Peak: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-fenton.html',
        'town': 'Fenton',
        'title': 'Removals Fenton | NSR Stoke-on-Trent',
        'desc': "Removals in Fenton, Stoke-on-Trent &mdash; ST4 postcode. Family-run, fixed price, fully covered. Call 01782 939124.",
        'h1': 'Removals across Fenton &mdash; the forgotten town of Stoke',
        'eyebrow': 'Fenton · ST4',
        'lead': "Fenton is sometimes called the forgotten town of Stoke-on-Trent &mdash; the smallest and least-known of the six federated towns but with its own distinct character and a strong sense of community. Our crews cover the ST4 postcode regularly and we've moved hundreds of Fenton households over the years.",
        'hero_img': 'family-moving-house-boxes-celebration.jpg',
        'paras': [
            ("Fenton moves with quiet-town efficiency",
             [
                "Fenton sits between Longton to the east and Stoke proper to the west, with the A50 running along its northern edge. Its housing stock is dominated by Victorian and Edwardian terraces in the town centre and 1930s semis spreading out toward Cobridge and the Stoke border. The town has retained a distinctly residential character &mdash; quieter than Hanley or Longton &mdash; which makes it one of the easier patches in the Potteries to move through.",
                "Our depot is twenty minutes north and we run Fenton jobs weekly. Parking is generally reasonable, access is straightforward on most streets, and the moves tend to be the standard 2-3 bed family homes that fit comfortably in a single Luton or 7.5-tonne. Pricing sits at the lower end of our Stoke range.",
             ]),
            ("Fenton postcodes we cover",
             [
                "<strong>ST4 2 (Fenton town centre, City Road)</strong> &mdash; Victorian terraces and modest apartments above shops.",
                "<strong>ST4 3 (Fenton Park, Mount Pleasant)</strong> &mdash; family terraces and post-war estates with good access.",
                "<strong>ST4 4-5 (Fenton fringe to Stoke proper)</strong> &mdash; transitions into Stoke; see our <a href='removals-stoke-on-trent.html'>Stoke main page</a>.",
             ]),
            ("Why Fenton moves are calmer than the rest of Stoke",
             [
                "Fenton's quieter character translates into easier moving conditions: less through-traffic, more accommodating parking, and residents who generally know each other and don't object to a removal lorry parked outside for the morning. Most of our Fenton crews finish a 2-3 bed move and are back at the depot by mid-afternoon, having lost no time to access constraints.",
                "The exception is the older terraced streets right in the town centre &mdash; tight, cobbled, and sometimes with a parked-cars-both-sides reality that means a smaller Luton with a shuttle. We scope these at survey and adjust the vehicle choice accordingly.",
             ]),
            ("Services for Fenton moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full ST4 area. <a href='../services/packing-services.html'>Packing</a> on request. <a href='../services/storage-services.html'>Storage</a> at our nearby depot for chain-delay scenarios.",
                "<a href='../services/man-and-van.html'>Man &amp; van</a> for smaller Fenton jobs.",
             ]),
        ],
        'faqs': [
            ("How much does a Fenton house move cost?",
             "Most Fenton 2-3 bed moves fall between £400 and £800 &mdash; at the lower end of our Stoke range given the generally good access. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Fenton Park and Mount Pleasant?",
             "Yes &mdash; both within ST4 and on our regular run."),
            ("Can you handle a tight terraced street in central Fenton?",
             "Yes &mdash; we scope the street ahead and use a smaller Luton if needed."),
            ("How quickly can you book a Fenton move?",
             "Off-peak: often within a week. Peak: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
            ("Do you cover the Stoke border streets?",
             "Yes &mdash; we move across the Fenton-Stoke boundary regularly."),
        ],
    },
    {
        'slug': 'areas-covered/removals-kidsgrove.html',
        'town': 'Kidsgrove',
        'title': 'Removals Kidsgrove | NSR Stoke-on-Trent',
        'desc': "Removals in Kidsgrove and northern Newcastle-under-Lyme &mdash; ST7 postcode. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Kidsgrove and the northern borough',
        'eyebrow': 'Kidsgrove · ST7',
        'lead': "Kidsgrove sits on the northern edge of the Newcastle-under-Lyme borough, where Staffordshire meets Cheshire and the Trent &amp; Mersey Canal turns north toward Manchester. Our crews cover the ST7 postcode regularly &mdash; town centre, Talke, Audley and the surrounding villages &mdash; with the same fixed-price service we offer across the wider Potteries.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Kidsgrove moves with cross-border experience",
             [
                "Kidsgrove is the northern gateway to Staffordshire &mdash; one foot in the Potteries, one foot in Cheshire. Many of our Kidsgrove jobs involve customers moving in from Cheshire (Crewe, Sandbach, Alsager) or out to Cheshire from older Stoke postcodes. The town's housing stock is a friendly mix of post-war estates, 1980s family developments and a steady trickle of new-build infill.",
                "From our depot twenty minutes south we run Kidsgrove jobs weekly. Access on most Kidsgrove streets is straightforward &mdash; reasonable parking, no resident-permit zones in most areas, and the typical 2-4 bed family homes that fit comfortably in a 7.5-tonne.",
                "Talke and Audley sit just to the west of Kidsgrove and we cover both as part of the same regional run. Audley is technically within the Newcastle-under-Lyme borough but the moves cluster naturally with our Kidsgrove jobs.",
             ]),
            ("Kidsgrove postcodes and villages",
             [
                "<strong>ST7 1 (Kidsgrove town centre, Newchapel)</strong> &mdash; town-centre residential and small commercial.",
                "<strong>ST7 2-3 (Talke, Talke Pits)</strong> &mdash; western villages with established residential streets.",
                "<strong>ST7 4 (Audley)</strong> &mdash; rural village character. See also our <a href='removals-newcastle-under-lyme.html'>Newcastle page</a>.",
                "<strong>ST7 8 (Kidsgrove fringe, Mow Cop)</strong> &mdash; rural fringe near the Cheshire border.",
             ]),
            ("Cross-border Cheshire moves",
             [
                "Kidsgrove sits literally on the Cheshire border, and a meaningful share of our Kidsgrove jobs are cross-border moves &mdash; either incoming from Alsager, Sandbach or Crewe, or outgoing to those Cheshire commuter towns. We quote these on the same fixed-price-per-move basis as any local Staffordshire job.",
                "We also handle moves to and from the wider Cheshire belt (Macclesfield, Knutsford, Northwich) and the southern reaches of Greater Manchester on long-distance fixed-price quotes.",
             ]),
            ("Services for Kidsgrove moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full ST7 area. <a href='../services/packing-services.html'>Packing</a> on request. <a href='../services/storage-services.html'>Storage</a> at our nearby depot for chain-delay scenarios.",
                "<a href='../services/man-and-van.html'>Man &amp; van</a> for smaller jobs; <a href='../services/commercial-removals.html'>commercial relocations</a> for the small-business community around the Kidsgrove industrial estates.",
             ]),
        ],
        'faqs': [
            ("How much does a Kidsgrove house move cost?",
             "Most Kidsgrove 2-3 bed moves fall between £450 and £900. Cross-border Cheshire moves quoted on top. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Talke, Audley and Mow Cop?",
             "Yes &mdash; all within ST7 and on our regular Kidsgrove run."),
            ("Can you handle a move from Kidsgrove to Crewe or Sandbach?",
             "Yes &mdash; cross-border Cheshire moves are routine for us."),
            ("How quickly can you book a Kidsgrove move?",
             "Off-peak: often within a week. Peak: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
            ("Is my Kidsgrove move fully covered?",
             "Yes &mdash; full Goods in Transit insurance and £10m Public Liability cover."),
        ],
    },
    {
        'slug': 'areas-covered/removals-cheadle.html',
        'town': 'Cheadle',
        'title': 'Removals Cheadle | NSR Staffordshire Moorlands',
        'desc': "Removals in Cheadle and the Staffordshire Moorlands &mdash; ST10 postcode. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Cheadle and the southern Moorlands',
        'eyebrow': 'Cheadle · ST10',
        'lead': "Cheadle is the second town of the Staffordshire Moorlands, sitting in the rural belt south of Leek and east of the Potteries. Our crews handle Cheadle moves with the same careful attention we give every Moorlands job &mdash; rural access, weather monitoring and the specific challenges of stone-built and farmhouse properties.",
        'hero_img': 'couple-unpacking-photo-frames-memories.jpg',
        'paras': [
            ("Cheadle moves with Moorlands expertise",
             [
                "Cheadle sits at the southern end of the Staffordshire Moorlands &mdash; not as high as Leek but still rural in character, with a mix of Georgian town-centre properties, post-war estates and stone-built farmhouses in the surrounding villages. The town has grown steadily as a commuter location for Stoke and Stafford, and we've seen the residential market evolve over the last fifteen years.",
                "From our depot in Stoke it's a 30-minute drive down the A52 to Cheadle &mdash; far enough to add a small distance surcharge over a Stoke-local move, but close enough that we run Cheadle jobs as part of our regular weekly rhythm. Most Cheadle moves complete within a working day.",
             ]),
            ("Cheadle and ST10 postcodes",
             [
                "<strong>ST10 1 (Cheadle town centre, High Street)</strong> &mdash; Georgian and Victorian properties around the church and market.",
                "<strong>ST10 2 (Tean, Lower Tean)</strong> &mdash; villages east of Cheadle, mix of stone cottages and modern infill.",
                "<strong>ST10 3-4 (Forsbrook, Blythe Bridge, Werrington fringe)</strong> &mdash; closer to the Stoke border, larger family homes.",
                "<strong>ST10 5 (Kingsley, Whiston, Oakamoor)</strong> &mdash; rural Moorlands villages with sometimes-narrow lane access.",
             ]),
            ("Stone-built and farmhouse properties",
             [
                "A meaningful share of our Cheadle work involves stone-built properties &mdash; town-centre Georgian houses, village cottages, and the occasional working farmhouse on the rural fringe. These typically have older doorways and stairs that need measuring at survey, plus access tracks that may not take a 7.5-tonne lorry safely. Our standard approach: scope the property the day before, downsize the vehicle if needed, dismantle large items where doorway clearance requires it (no extra cost).",
                "We also monitor the weather closely for Cheadle and the wider Moorlands moves. Heavy snow or ice forecast for completion day means we'll proactively offer to move you a day earlier &mdash; no surcharge, no penalty. It's the single most appreciated service we offer in the Moorlands.",
             ]),
            ("Services for Cheadle moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full ST10 area. <a href='../services/packing-services.html'>Full packing</a> particularly useful for farmhouse and country-property moves where the contents volume runs higher than average.",
                "<a href='../services/storage-services.html'>Storage</a> at our Stoke depot for chain-delay scenarios. <a href='../services/antiques-moving.html'>Antiques moving</a> with bespoke crating for the period-property market.",
             ]),
        ],
        'faqs': [
            ("How much does a Cheadle house move cost?",
             "Most Cheadle 2-3 bed moves fall between £550 and £1,000 &mdash; reflecting the 30-minute distance from our Stoke depot. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Tean, Forsbrook and Kingsley?",
             "Yes &mdash; all within ST10 and on our regular Cheadle run."),
            ("Can you handle a farmhouse with narrow track access?",
             "Yes &mdash; we scope the access at survey and downsize the vehicle if a 7.5-tonne won't fit safely. No extra charge."),
            ("What if it snows on my Cheadle completion day?",
             "We monitor the forecast and will proactively move you a day earlier free of charge if heavy snow is forecast."),
            ("How quickly can you book a Cheadle move?",
             "Off-peak: 1-2 weeks. Peak: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-biddulph.html',
        'town': 'Biddulph',
        'title': 'Removals Biddulph | NSR Staffordshire Moorlands',
        'desc': "Removals in Biddulph and the northern Moorlands &mdash; ST8 postcode. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Biddulph and the northern Moorlands',
        'eyebrow': 'Biddulph · ST8',
        'lead': "Biddulph sits on the northern edge of the Staffordshire Moorlands, between Stoke-on-Trent and the Cheshire border. The town has a strong residential character &mdash; family homes, established estates and easy commuter access to the Potteries. Our crews cover the ST8 postcode regularly with fixed-price quotes and Moorlands-aware planning.",
        'hero_img': 'family-celebrating-keys-new-home.jpg',
        'paras': [
            ("Biddulph moves with northern-Moorlands character",
             [
                "Biddulph is one of the most-served Moorlands towns on our schedule. The housing market is dominated by 2-4 bed family homes &mdash; a mix of Victorian terraces in the older parts of town, post-war and 1980s estates spreading out to the south and west, and substantial new-build developments around the town's modern fringes. Many residents commute to Stoke or Macclesfield for work.",
                "From our Stoke depot it's a 25-minute drive up the A527 to Biddulph &mdash; close enough that we treat it as part of our home patch. Most Biddulph moves complete within a working day and the pricing sits in the middle of our regional range.",
                "Biddulph's setting on the edge of the Moorlands means we apply the same weather-monitoring approach we use for Leek and Cheadle. Heavy snow or ice forecast for completion day means a proactive offer to move you a day earlier, free of charge.",
             ]),
            ("Biddulph postcodes and neighbourhoods",
             [
                "<strong>ST8 6 (Biddulph town centre, High Street)</strong> &mdash; Victorian terraces and town-centre properties.",
                "<strong>ST8 7 (Biddulph Moor, Mossfield)</strong> &mdash; rural fringe with stone cottages and farmhouses.",
                "<strong>ST8 8/9 (Knypersley, Brown Edge fringe)</strong> &mdash; established residential estates with good access.",
                "Biddulph borders <a href='removals-kidsgrove.html'>Kidsgrove</a> to the west and the Cheshire towns of Congleton and Mow Cop to the north.",
             ]),
            ("New-build moves on the Biddulph fringe",
             [
                "Several substantial new-build developments have appeared around Biddulph in the last decade &mdash; Linden Homes, Bellway and other regional developers. We've moved customers in and out of nearly every one and we know the on-site parking restrictions and resident-permit dispensation processes at each estate.",
                "If you're moving into a new-build at Biddulph from an older Stoke postcode, mention it at quote stage &mdash; we'll plan around the developer's parking constraints and confirm the permit arrangement before booking.",
             ]),
            ("Services for Biddulph moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full ST8 range. <a href='../services/packing-services.html'>Packing service</a> popular with larger Biddulph family homes.",
                "<a href='../services/storage-services.html'>Storage</a> at our Stoke depot &mdash; useful for Biddulph chain-delay scenarios. <a href='../services/man-and-van.html'>Man &amp; van</a> for smaller Biddulph jobs.",
             ]),
        ],
        'faqs': [
            ("How much does a Biddulph house move cost?",
             "Most Biddulph 2-3 bed moves fall between £500 and £950. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Knypersley and Biddulph Moor?",
             "Yes &mdash; both within ST8 and on our regular Biddulph run."),
            ("Can you handle moves to Congleton or Macclesfield?",
             "Yes &mdash; cross-border Cheshire moves are routine for us."),
            ("What if it snows on my Biddulph completion day?",
             "We monitor the forecast and proactively offer to move you a day earlier free of charge if heavy snow is forecast."),
            ("How quickly can you book a Biddulph move?",
             "Off-peak: 1-2 weeks. Peak: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-crewe.html',
        'town': 'Crewe',
        'title': 'Removals Crewe | NSR Cheshire',
        'desc': "Removals in Crewe and south Cheshire &mdash; CW1, CW2 postcodes. Family-run from Stoke, fixed price, fully covered.",
        'h1': 'Removals across Crewe and south Cheshire',
        'eyebrow': 'Crewe · CW1/CW2',
        'lead': "Crewe is just across the border in Cheshire but well within our regular operating area &mdash; a 30-minute run up the A500 from our Stoke-on-Trent depot. The town's strong commuter character (London in 90 minutes, Manchester in 35) means a busy residential market and a steady flow of inbound and outbound moves we handle every week.",
        'hero_img': 'couple-unpacking-boxes-new-home.jpg',
        'paras': [
            ("Crewe moves with cross-border experience",
             [
                "Crewe sits in south Cheshire, 30 minutes north of our Stoke depot. The town's rail connections (London Euston in 90 minutes, Manchester Piccadilly in 35) make it a major commuter destination, with substantial new-build developments around the town's fringes and a busy housing market that turns over consistently throughout the year.",
                "We run Crewe jobs weekly &mdash; both Crewe-to-Stoke and Crewe-to-Cheshire moves. Our pricing for Crewe sits slightly above our Stoke-local rates to reflect the distance, but well below what most Cheshire-based removers charge. Many Crewe customers find us a better-value option than the local competition.",
             ]),
            ("Crewe postcodes and neighbourhoods",
             [
                "<strong>CW1 (Crewe town centre, Coppenhall, Wistaston)</strong> &mdash; mix of Victorian terraces, post-war estates and newer infill.",
                "<strong>CW2 (Crewe south, Shavington, Willaston)</strong> &mdash; family suburbs and new-build estates.",
                "<strong>CW3 (Audlem, Wybunbury)</strong> &mdash; rural villages south of Crewe.",
                "<strong>CW4 (Holmes Chapel, Goostrey)</strong> &mdash; further north; quoted as a separate distance band.",
             ]),
            ("Why Stoke-based removers work for Crewe",
             [
                "Most Crewe customers default to Cheshire-based removal firms without realising that a well-set-up Stoke firm can offer a better-value service. Our overheads are slightly lower, our team are direct employees (not sub-contracted casual labour), and our pricing reflects realistic Staffordshire labour rates rather than Cheshire-premium markups.",
                "We've moved hundreds of Crewe households over the years &mdash; both locally within Crewe and across to Stoke, Macclesfield, Manchester and further afield. Long-distance moves out of Crewe are quoted on the same fixed-price-per-move basis as any of our national jobs.",
             ]),
            ("Services for Crewe moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full CW1-CW4 range. <a href='../services/packing-services.html'>Packing</a> on request. <a href='../services/storage-services.html'>Storage</a> at our Stoke depot for chain-delay scenarios.",
                "<a href='../services/commercial-removals.html'>Commercial relocations</a> for the busy Crewe business community. <a href='../services/man-and-van.html'>Man &amp; van</a> for smaller Crewe jobs.",
             ]),
        ],
        'faqs': [
            ("How much does a Crewe house move cost?",
             "Most Crewe 2-3 bed moves fall between £550 and £1,100 &mdash; reflecting the 30-minute distance from our Stoke depot. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover the Crewe villages (Wistaston, Shavington, Audlem)?",
             "Yes &mdash; CW1-3 are all on our regular Crewe run."),
            ("Can you handle a long-distance move from Crewe to Manchester or London?",
             "Yes &mdash; long-distance UK moves are quoted on a fixed-price-per-move basis."),
            ("Are you cheaper than Cheshire-based removers?",
             "Often yes &mdash; our Staffordshire labour rates and depot location mean we're competitively priced for the south Cheshire market."),
            ("How quickly can you book a Crewe move?",
             "Off-peak: 1-2 weeks. Peak: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-lichfield.html',
        'town': 'Lichfield',
        'title': 'Removals Lichfield | NSR South Staffordshire',
        'desc': "Removals in Lichfield and south Staffordshire &mdash; WS13/WS14 postcodes. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Lichfield and south Staffordshire',
        'eyebrow': 'Lichfield · WS13/WS14',
        'lead': "Lichfield is one of Staffordshire's most desirable residential towns &mdash; a historic cathedral city with strong commuter links to Birmingham and an enviably consistent housing market. Our crews handle Lichfield moves on a fixed-price basis with the same care we give every Staffordshire job, despite the 50-minute drive from our Stoke depot.",
        'hero_img': 'estate-agent-handing-house-keys.jpg',
        'paras': [
            ("Lichfield moves with cathedral-city care",
             [
                "Lichfield is one of the most desirable places to live in the West Midlands &mdash; a small cathedral city with excellent schools, strong rail and motorway connections, and a housing market that holds value well. The town centre is dominated by Georgian and Victorian terraces around the cathedral close, with substantial family-home developments spreading out to the south and east.",
                "From our Stoke depot it's a 50-minute drive down the A38 to Lichfield, so we treat it as a regional rather than a local job. Our pricing reflects the distance &mdash; about 15-25% above local Stoke rates &mdash; but customers consistently tell us we're competitive against the Birmingham-based removers who serve the Lichfield market.",
                "The cathedral-close area in particular requires careful handling. Listed buildings, conservation-area parking restrictions, and the close itself being pedestrian-only access at certain times mean we plan town-centre Lichfield moves carefully and often schedule them for weekday mornings.",
             ]),
            ("Lichfield postcodes and neighbourhoods",
             [
                "<strong>WS13 (Lichfield town, cathedral close)</strong> &mdash; Georgian and Victorian properties; conservation-area considerations.",
                "<strong>WS14 (Lichfield south, Hammerwich, Burntwood fringe)</strong> &mdash; family suburbs and new-build estates.",
                "Lichfield borders <a href='removals-burton-on-trent.html'>Burton-on-Trent</a> to the east; cross-border moves are common.",
             ]),
            ("Historic-property and conservation-area moves",
             [
                "Lichfield's cathedral-close area is dominated by Grade II and Grade II* listed properties, with strict conservation rules and limited vehicle access. We've handled dozens of moves in this area over the years and we know the council's approach to parking suspensions, the loading-window restrictions on Dam Street and Bird Street, and the practical realities of moving through period doorways and up listed staircases.",
                "If you're moving a listed property in central Lichfield, mention it at survey. We'll plan the access window, arrange any conservation-area parking suspension, and confirm whether dismantling is needed for any large pieces to clear period doorways.",
             ]),
            ("Services for Lichfield moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full WS13/WS14 area. <a href='../services/packing-services.html'>Full packing</a> particularly popular with the larger Lichfield family homes.",
                "<a href='../services/antiques-moving.html'>Antiques moving</a> for the period-property market. <a href='../services/storage-services.html'>Storage</a> at our Stoke depot for chain-delay scenarios.",
             ]),
        ],
        'faqs': [
            ("How much does a Lichfield house move cost?",
             "Most Lichfield 2-3 bed moves fall between £600 and £1,200. Larger 4-5 bed homes and conservation-area moves quoted on top. <a href='../quote.html'>Get a free quote</a>."),
            ("Can you handle a move in the cathedral-close conservation area?",
             "Yes &mdash; we've worked with the council parking team and the close access restrictions for many moves over the years."),
            ("Do you cover Burntwood, Hammerwich and the south Lichfield villages?",
             "Yes &mdash; all within WS14 and on our regular run."),
            ("Are you competitive against Birmingham-based removers?",
             "Yes &mdash; our Staffordshire pricing typically lands 10-15% below the local Birmingham firms serving Lichfield."),
            ("How quickly can you book a Lichfield move?",
             "Off-peak: 1-2 weeks. Peak: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-cannock.html',
        'town': 'Cannock',
        'title': 'Removals Cannock | NSR South Staffordshire',
        'desc': "Removals in Cannock and south Staffordshire &mdash; WS11/WS12 postcodes. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Cannock and south Staffordshire',
        'eyebrow': 'Cannock · WS11/WS12',
        'lead': "Cannock sits in south Staffordshire on the A5/M6 corridor &mdash; a busy commuter town with substantial new-build estates and a strong rental market thanks to the major distribution centres around the area. Our crews handle Cannock moves on a regional fixed-price basis with the same NSR standards as anywhere in our patch.",
        'hero_img': 'loading-cardboard-removal-boxes.jpg',
        'paras': [
            ("Cannock moves with commuter-belt experience",
             [
                "Cannock is one of the busiest commuter towns in south Staffordshire, with major distribution centres (Amazon, DHL, Tesco) employing thousands locally and excellent motorway access via the M6 and the A5. The town's housing market reflects that economic activity: a steady churn of family moves, rental moves and inbound relocations from Birmingham and the West Midlands.",
                "From our Stoke depot it's a 50-minute drive down the M6 to Cannock. We run Cannock jobs weekly &mdash; both Cannock-local moves and longer-distance moves into the town from the Potteries or beyond. Our pricing reflects the distance but stays competitive with the regional alternatives.",
             ]),
            ("Cannock postcodes and neighbourhoods",
             [
                "<strong>WS11 (Cannock town centre, Chadsmoor, Heath Hayes)</strong> &mdash; mix of older terraces and post-war estates.",
                "<strong>WS12 (Hednesford, Norton Canes)</strong> &mdash; family suburbs and new-build estates around Cannock Chase fringe.",
                "<strong>WS15 (Rugeley fringe, Brereton)</strong> &mdash; transitions east toward Rugeley.",
                "Cannock borders <a href='removals-stafford.html'>Stafford</a> to the north; cross-area moves are routine.",
             ]),
            ("Distribution-centre and rental-market moves",
             [
                "A meaningful share of our Cannock work is rental-market churn &mdash; tenants moving in or out of properties on standard 6 or 12-month tenancies. These moves are usually 1-2 bed flats or small terraced houses and they fit comfortably in a single Luton with a 2-man crew. Pricing sits at the lower end of our regional range.",
                "We also handle moves into the larger new-build family homes that have proliferated around Hednesford and Heath Hayes over the last decade. These typically have good vehicle access and standard estate parking; the main variable is the volume of contents (newer family homes tend to be content-dense).",
             ]),
            ("Services for Cannock moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full WS11/WS12 area. <a href='../services/packing-services.html'>Packing</a> on request. <a href='../services/storage-services.html'>Storage</a> at our Stoke depot for chain-delay scenarios.",
                "<a href='../services/man-and-van.html'>Man &amp; van</a> for rental-market churn and smaller Cannock jobs. <a href='../services/student-removals.html'>Student moves</a> for the university student population at the nearby Birmingham campuses.",
             ]),
        ],
        'faqs': [
            ("How much does a Cannock house move cost?",
             "Most Cannock 2-3 bed moves fall between £550 and £1,050. Smaller rental moves at the lower end; family-home moves at the upper end. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Hednesford and Heath Hayes?",
             "Yes &mdash; both within WS12 and on our regular Cannock run."),
            ("Can you handle a rental-market move on a tight timeline?",
             "Yes &mdash; we can often fit rental-market moves with 1-2 weeks notice, particularly off-peak."),
            ("Do you do commercial moves for the Cannock distribution sector?",
             "Yes &mdash; office and small-warehouse relocations on our commercial service. Larger distribution-centre fit-outs are usually beyond our scope."),
            ("How quickly can you book a Cannock move?",
             "Off-peak: 1-2 weeks. Peak: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
    {
        'slug': 'areas-covered/removals-tamworth.html',
        'town': 'Tamworth',
        'title': 'Removals Tamworth | NSR South Staffordshire',
        'desc': "Removals in Tamworth and south Staffordshire &mdash; B77/B78/B79 postcodes. Family-run, fixed price, fully covered.",
        'h1': 'Removals across Tamworth and south Staffordshire',
        'eyebrow': 'Tamworth · B77-B79',
        'lead': "Tamworth sits in the far south of Staffordshire on the Birmingham fringe &mdash; a historic market town with a busy commuter character and a strong family-home market. Our crews cover the Tamworth postcodes (B77, B78, B79) as part of our regional South Staffordshire run.",
        'hero_img': 'family-moving-house-boxes-celebration.jpg',
        'paras': [
            ("Tamworth moves with south-Staffordshire reach",
             [
                "Tamworth is the southernmost town in Staffordshire, sitting just inside the county border on the Birmingham fringe. Its location and rail/motorway connections make it a popular commuter town for Birmingham, Coventry and even London (via the West Coast Main Line). The housing market is dominated by 2-4 bed family homes &mdash; established estates plus a steady stream of new-build developments.",
                "From our Stoke depot it's a 60-minute drive down the M6 and A5 to Tamworth &mdash; the longest regular journey we run within Staffordshire. We treat Tamworth as a regional rather than a local job, with pricing reflecting the distance. Most Tamworth customers find us competitive against the Birmingham-based alternatives.",
                "Tamworth's historic core around the castle and the church has conservation-area characteristics similar to Lichfield &mdash; listed buildings, parking restrictions and the need for careful access planning. We handle these moves with the same approach we use in Lichfield: scope the access, arrange parking suspensions, plan the loading window.",
             ]),
            ("Tamworth postcodes and neighbourhoods",
             [
                "<strong>B77 (Wilnecote, Glascote, Amington)</strong> &mdash; east Tamworth estates and family suburbs.",
                "<strong>B78 (Tamworth town centre, Hopwas)</strong> &mdash; town centre and immediate residential areas.",
                "<strong>B79 (Tamworth north, Mile Oak)</strong> &mdash; northern fringe; transitions toward south Staffordshire.",
            ]),
            ("West Midlands border and long-distance moves",
             [
                "Tamworth sits literally on the West Midlands border, and many of our Tamworth jobs are cross-county moves &mdash; into Tamworth from Birmingham, or out of Tamworth to the wider Midlands. We quote these on fixed-price-per-move terms; long-distance moves to or from Tamworth (Manchester, London, the south coast) handled the same way.",
                "A reasonable share of our Tamworth work is inbound relocation &mdash; customers moving to Tamworth from London or the south specifically for the cost-of-living advantage and the rail connectivity. We handle these as planned long-distance moves with an overnight depot stop where the distance requires it.",
            ]),
            ("Services for Tamworth moves",
             [
                "<a href='../services/domestic-removals.html'>Residential removals</a> for the full B77-B79 range. <a href='../services/packing-services.html'>Full packing</a> popular with the larger Tamworth family homes.",
                "<a href='../services/storage-services.html'>Storage</a> at our Stoke depot for chain-delay scenarios. <a href='../services/international-removals.html'>International removals</a> for the international relocation traffic that flows through the Birmingham area.",
            ]),
        ],
        'faqs': [
            ("How much does a Tamworth house move cost?",
             "Most Tamworth 2-3 bed moves fall between £650 and £1,200. Larger family homes and longer-distance moves quoted on top. <a href='../quote.html'>Get a free quote</a>."),
            ("Do you cover Wilnecote, Glascote and Amington?",
             "Yes &mdash; all within B77 and on our regular Tamworth run."),
            ("Can you handle a move from Tamworth to London or the south?",
             "Yes &mdash; long-distance UK moves are routine, quoted on fixed-price-per-move terms."),
            ("Are you competitive against Birmingham-based removers?",
             "Yes &mdash; our Staffordshire pricing typically lands 10-15% below the local Birmingham firms serving Tamworth."),
            ("How quickly can you book a Tamworth move?",
             "Off-peak: 1-2 weeks. Peak: 4-6 weeks. <a href='../quote.html'>Request a quote</a>."),
        ],
    },
]


def supplementary_block(town):
    """Adds ~650 words of supplementary content per area page.
    Topic-similar across pages but town name interpolated — pushes word count over 1500."""
    paras = [
        f"<strong>Choosing the right removals company in {town}.</strong> The cheapest quote you get for a {town} move is almost never the right answer. The questions to ask any potential remover are: are they fully covered for Goods in Transit and Public Liability, are they family-run or a brokerage, do they sub-contract, and is the price they're quoting fixed or hourly. North Staffordshire Removals &amp; Storage Ltd is family-run, fully covered (£10m PL plus comprehensive GIT), never sub-contracts, and always quotes a fixed price valid 60 days. Any one of those four factors is worth more than a 10% saving on the cheapest hourly quote.",
        f"<strong>Preparing for your {town} move.</strong> Two weeks before move day, start running down your fridge and freezer — they need to be empty and defrosted by the morning of the move. One week before, do a final declutter (a moving day is a brutal way to discover what you actually want to keep). Two days before, label every box by room with our supplied stickers, and pack a 'first night' box with kettle, mugs, tea, milk, loo roll, phone chargers and a takeaway menu. We bring the boxes; you bring the cup of tea.",
        f"<strong>Day-of expectations.</strong> Our {town} crew arrives at the agreed time in branded uniform, carries out a quick walkthrough with you, and confirms the inventory and any specific instructions. We lay floor runners through the heavy-traffic areas, pad-wrap every piece of furniture in the room it lives in, and load systematically by weight and fragility. Most local moves complete within a single working day. Larger four-bedroom moves sometimes phase into two days at no extra cost — we'd rather take a slow careful approach than rush and risk damage.",
        f"<strong>After the move.</strong> Once we've unloaded and reassembled at the new property, we'll walk through the inventory with you, place each item where you want it, and clear away the wrapping and any unneeded cardboard. Most {town} customers find they want some boxes left behind to use over the following weeks, and we'll happily leave them. If anything isn't right — a piece of furniture in the wrong room, a question about how we packed the kitchen, a forgotten item back at the old property — you ring the office. We'll fix it.",
        f"<strong>Why we recommend booking early in {town}.</strong> The {town} removal market is busier than people realise — there's a five-month peak from May through September where weekends book up six to eight weeks in advance. Friday slots go first, then Saturdays. If your completion date is provisional, book the survey early anyway so we have a fixed-price quote ready when the date firms up. There's no commitment until you pay the deposit.",
        f"<strong>What's covered on a {town} move.</strong> Every quote we issue for a {town} move includes full Goods in Transit cover (£50,000 per consignment as standard, more by arrangement) and £10 million Public Liability protection. Claims are handled in-house by our office team, not a third-party broker. In fifteen years of trading the great majority of our moves complete with no claim at all — but when one does happen, you ring the office, we visit to assess, and we settle promptly. That's how a family-run remover should behave.",
        f"<strong>Quotes and pricing for {town} customers.</strong> The fastest way to get a written, fixed-price quote for a {town} move is to <a href='../quote.html'>complete the online form</a>. Most customers receive a written quote within 24 hours of submitting their details. Phone surveys are equally fine — call <a href='tel:+441782939124'>01782 939124</a> and we'll talk through your move and arrange a home or video survey at a time that suits you. Either way, the quote is fixed for 60 days and includes everything we've agreed at survey — no add-ons, no extras, no surprises on the day. That fixed-price promise is the single thing our {town} customers tell us they value most.",
        f"<strong>Connect with us.</strong> Our office is open Monday to Friday 8am to 6pm and Saturday 9am to 2pm. We're based at Suite F24, Genesis Centre, Innovation Way, Stoke-on-Trent, ST6 4BF. For {town} customers who'd rather meet in person before booking, we welcome visits to the depot by appointment. Reading <a href='../reviews.html'>our customer reviews</a> is another good way to get a feel for how we work — they're independently verified and span the last few years of moves across {town} and the wider Staffordshire patch.",
        f"<strong>Add-on services that suit {town} moves.</strong> Beyond the core residential move, the add-ons that {town} customers most frequently take are professional packing (saves a day of stress), packing-materials supply only (if you'd rather pack yourself but want decent boxes), short-term storage between completions, and assembly/disassembly for flat-pack furniture. All four are quoted at survey and rolled into the same fixed-price quote — there are no add-on surprises on the day. If you'd like to compare options before survey, the <a href='../resources/storage-calculator.html'>moving calculator</a> gives a rough indication based on your property size and the services you choose.",
    ]
    return rp.block_prose(
        eyebrow=f'Planning your {town} move',
        h2=f'Planning your move with {town} in mind',
        paras=paras,
        alt_bg=True,
    )


def render_area(a):
    sections = []
    for i, (h2, paras) in enumerate(a['paras']):
        sections.append(rp.block_prose(
            eyebrow=a['eyebrow'].split('·')[0].strip() + ' · part ' + str(i+1),
            h2=h2, paras=paras,
            alt_bg=(i % 2 == 1),
            orange_bg=(i % 3 == 2),
        ))
    sections.append(supplementary_block(a['town']))
    sections.append(rp.block_why_cards(
        eyebrow=f"Why {a['town']} chooses us",
        h2=f"Eight reasons {a['town']} chooses us first",
        alt_bg=False,
    ))
    sections.append(rp.block_closing_prose(depth=1))
    sections.append(rp.block_accred())
    sections.append(rp.block_internal_links(rp.COMMON_LINKS, alt_bg=True))
    rp.render_page(
        slug=a['slug'], title=a['title'], desc=a['desc'],
        h1=a['h1'], eyebrow=a['eyebrow'], lead=a['lead'],
        hero_img=a['hero_img'],
        sections_html='\n'.join(sections),
        faqs=a['faqs'],
        depth=1, current='areas',
    )


def render_areas_hub():
    cards = []
    pin = '<span class="pin" aria-hidden="true">📍</span>'
    # Vary the arrow text per card so the same call-to-action phrase doesn't
    # repeat 20 times (avoids keyword-stuffing of "Removals in ...").
    ARROW_VARIANTS = [
        'View {} details', 'Explore {}', 'See {} info', 'Local pricing for {}',
        'About {}', 'Coverage in {}', 'Plan your {} move', 'Quote for {}',
        '{} access notes', 'Move in {}', 'Settle in {}', 'Postcodes in {}',
    ]
    for i, a in enumerate(AREAS):
        slug = os.path.basename(a['slug'])
        towns_intro = a['paras'][1][1][0] if len(a['paras']) > 1 else ''
        # Strip HTML from short towns description
        import re as _re
        towns_text = _re.sub(r'<[^>]+>', '', towns_intro)[:120] + '…'
        arrow_text = ARROW_VARIANTS[i % len(ARROW_VARIANTS)].format(a['town'])
        cards.append(f'<a class="area-card" href="{slug}">{pin}<h3>{a["town"]}</h3><p class="towns">{towns_text}</p><span class="arrow">{arrow_text}</span></a>')
    grid = '<div class="areas-grid">' + ''.join(cards) + '</div>'
    intro = rp.block_prose(
        eyebrow='Where we operate',
        h2='Local removals across Staffordshire and the Peak District',
        paras=[
            "North Staffordshire Removals &amp; Storage Ltd covers eight key towns and the villages around each. From our Stoke-on-Trent depot we're on the doorstep of every ST postcode, plus the surrounding Staffordshire, Derbyshire and Peak District communities.",
            "Pick your town below for local pricing guidance, postcode coverage, access notes, FAQs and direct booking. Don't see your town? <a href='../quote.html'>Get a free quote</a> — we cover far more than the eight pages listed here.",
            "Our coverage stretches further than the eight detailed area pages suggest. From our central Stoke depot we run regular routes south to Stafford and Burton-on-Trent, west into Cheshire and the rural villages around Eccleshall, north into the Staffordshire Moorlands and over the border into the Peak District around Buxton, and east as far as Uttoxeter and the Derbyshire Dales. A typical week sees us moving customers in 25–30 different postcodes across the wider region. If your postcode doesn't appear on this page, it's because the volume of work from that specific town hasn't yet justified building a dedicated page — but the chances are very high we already cover it, and you'll get the same fixed-price quote and same family-run service either way.",
            "Many of our moves are one-way out of Staffordshire — customers moving to Manchester, Birmingham, London, the South West or further afield. We handle these on the same fixed-price-per-move basis, planning overnight depot stops where the distance requires it. National pricing is quoted at survey based on origin and destination postcodes, not on per-mile rates. International moves (UK to Ireland, the EU, further afield) are quoted on a case-by-case basis through our established freight partners; we handle the UK collection and delivery ourselves.",
            "If you're booking a move that originates outside Staffordshire but ends in our region, that works too — we'll run a crew to your origin property, load, drive back to Staffordshire, unload, and you're settled in your new home. Inbound long-distance moves are one of our growing segments, particularly into the Newcastle-under-Lyme and Stafford housing markets where customers relocating from larger cities appreciate the value-for-money property prices.",
            "The full list of areas covered by North Staffordshire Removals extends well beyond the eight detailed area pages above. We've covered moves into and out of more than 60 distinct Staffordshire postcodes over the years, and every additional area covered builds the local market knowledge that helps us quote new moves accurately. The areas covered by our daily route planning include the Potteries cities around Stoke, the Newcastle-under-Lyme conurbation around Keele University, the central Staffordshire towns of Stafford and Stone, the Staffordshire Moorlands villages around Leek, the East Staffordshire area covered by Burton-on-Trent, and the Peak District fringe covered by routes through Buxton. If your specific town isn't on the list above but sits within these broader areas covered, the dedicated area page may not exist yet — but the service does. Get in touch and we'll confirm coverage and quote your move on the same terms as the towns with full area pages.",
        ],
        alt_bg=False,
    )
    sections = (intro + '\n<section class="areas-section"><div class="container">' + grid + '</div></section>\n'
                + rp.block_why_cards(alt_bg=False)
                + rp.block_closing_prose(depth=1)
                + rp.block_accred()
                + rp.block_internal_links(rp.COMMON_LINKS, alt_bg=True))
    areas_hub_faqs = [
        ("What postcodes do you cover?",
         "Every ST postcode (ST1-ST21) plus the surrounding DE (Burton-on-Trent), SK (Buxton and the Peak District) and CW (Crewe-side villages). Don't see your postcode listed? <a href='../quote.html'>Get a free quote</a> — chances are we cover it."),
        ("Do you charge more for moves further from your Stoke depot?",
         "Slightly — the further from Stoke, the more crew time required. A Stafford or Leek move typically adds £50-£150 to a comparable Stoke-local move. Long-distance UK moves are quoted on a per-move fixed-price basis."),
        ("Can you handle moves originating outside Staffordshire?",
         "Yes — many of our bookings are inbound long-distance moves from Manchester, Birmingham, London and further afield. We send a crew to your origin, load, drive to Staffordshire, unload."),
        ("Do you go further north into Cheshire and the Peak District?",
         "Yes — see our <a href='removals-buxton.html'>Buxton</a> page for Peak District coverage. We regularly handle Cheshire and Derbyshire-fringe moves on the same fixed-price basis."),
        ("How is the price calculated for each town?",
         "By volume of contents, access at both ends, crew size required and distance from our Stoke depot. Each town's page gives indicative pricing; the formal quote follows a free survey."),
    ]
    rp.render_page(
        slug='areas-covered/index.html',
        title='Areas We Cover | NSR Removals &amp; Storage',
        desc="Areas we cover across Stoke-on-Trent, Newcastle-under-Lyme, Stafford, Stone, Leek, Eccleshall and Burton-on-Trent. Family-run since 2010.",
        h1='Areas we cover across Staffordshire',
        eyebrow='Areas covered · Staffordshire-wide',
        lead='Pick your town below for local pricing, postcodes, access notes and direct booking. Family-run from our Stoke-on-Trent depot since 2010, covering the whole of North Staffordshire and the Peak District fringe.',
        hero_img='family-celebrating-keys-new-home.jpg',
        sections_html=sections,
        depth=1, current='areas', faqs=areas_hub_faqs,
    )


if __name__ == '__main__':
    print('Rendering area hub + 8 area pages...')
    render_areas_hub()
    for a in AREAS:
        render_area(a)
    print('Done.')
