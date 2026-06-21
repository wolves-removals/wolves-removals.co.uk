# -*- coding: utf-8 -*-
"""Per-service content for Wolves Removals service pages.
Authored from the live site copy + removals domain knowledge; real facts preserved
(e.g. Man and Van from £80). Shared sections (why-choose, related, CTA, schema) are
added by tools/render_services.py. HTML uses triple-quoted strings to avoid quote issues.
"""

SERVICES = [
{
  "slug": "house-removals", "name": "House Removals", "video": "packing-sofa-promo",
  "h1": "House Removals in Sussex",
  "title": "House Removals Sussex | Wolves Removals",
  "meta": "Professional, fully insured house removals across Sussex, Surrey, Hampshire & Kent. Family-run Wolves Removals: planning, packing, transport & storage. Free quote.",
  "teaser": "Fully managed home moves with planning, packing, transport and storage under one roof.",
  "lead": """<p>Seamless, stress-free managed <strong>house removals in Sussex</strong> and beyond. We help families move smoothly with expert planning, packing, transport and storage &mdash; all under one roof.</p>""",
  "included": ["Planning, packing, collection, storage and delivery under one roof",
               "Responsive, dedicated move coordinators",
               "Nationwide and international delivery options",
               "Flexible moving plans to suit your timeline",
               "Extremely cost-effective, fully insured service"],
  "sections": [
    ("Why Sussex Prefers Wolves Removals",
     """<p>We provide prompt, reliable house removals across Sussex, Surrey, Kent and Hampshire. Whether you&rsquo;re moving from a large family home, a flat, or anything in between, our experienced team delivers a smooth, well-organised move from start to finish.</p>
        <p>Moving house can feel stressful &mdash; but with the right planning and the right team, it doesn&rsquo;t have to be. At Wolves Removals we focus on preparation, clear communication and practical solutions to keep your move on track and reduce unnecessary worry. Book your free, no-obligation home visit with a Wolves move coordinator to receive a tailored quote.</p>"""),
    ("Better Removals Start With Better Planning",
     """<p>A successful move begins long before moving day. Our structured planning process considers every detail &mdash; from access and timing to packing requirements and special items &mdash; so your move runs smoothly and efficiently.</p>
        <ul class="tick-list"><li>Dedicated move coordinator from start to finish</li><li>Pre-move assessment to understand your exact needs</li><li>Clear scheduling and realistic timelines</li><li>Packing, storage and transport tailored to you</li><li>Experienced team ready to handle the unexpected</li></ul>
        <p>We also offer full <a href="/services/full-packing-service/">packing</a> and <a href="/services/full-unpacking-service/">unpacking</a>, secure <a href="/services/storage/">storage</a> and specialist handling for <a href="/services/piano-moving/">pianos</a> and <a href="/services/specialised-antiques-moving/">antiques</a>.</p>"""),
    ("A Smooth Moving Day With No Surprises",
     """<p>Moving day should feel organised and predictable. With careful preparation and our experienced team, every stage is planned in advance so your move runs without unnecessary pressure. We operate a modern, fully maintained fleet and our trained crews protect floors, doorways and furniture as standard.</p>
        <p>For added reassurance we are fully insured, and we&rsquo;re happy to talk through cover so you feel completely confident throughout your move. Keeping promises since 2016, we combine up-to-date working practices with traditional standards of reliability and care.</p>"""),
  ],
  "faqs": [
    ("How much do house removals cost in Sussex?", """<p>Costs depend on the size of your home, distance, access and any packing or storage required. The best way to get an accurate figure is a free, no-obligation quote &mdash; <a href="/get-a-quote/">request yours here</a> or see our <a href="/pricing/">pricing guide</a>.</p>"""),
    ("Do you provide packing for house moves?", """<p>Yes &mdash; we offer <a href="/services/full-packing-service/">full packing</a>, <a href="/services/fragile-packing/">fragile-only packing</a> and <a href="/services/packing-materials/">packing materials</a> from our <a href="/box-shop/">box shop</a>, so you can do as much or as little as you like.</p>"""),
    ("How far in advance should I book?", """<p>We recommend booking as early as possible, especially over summer and month-ends. That said, we can often accommodate short-notice moves &mdash; get in touch and we&rsquo;ll do our best to fit you in.</p>"""),
    ("Can you store my belongings between moves?", """<p>Absolutely. Our clean, dry, containerised <a href="/services/storage/">storage</a> covers <a href="/services/storage/short-term-storage/">short</a> and <a href="/services/storage/long-term-storage/">long-term</a> needs, ideal when completion dates don&rsquo;t line up.</p>"""),
    ("Are my belongings insured during the move?", """<p>Yes, every move is fully insured and carried out by our trained team. We&rsquo;re also a LAPADA member and Checkatrade-verified for added peace of mind.</p>"""),
  ],
  "related": ["commercial-removals", "man-and-van", "full-packing-service", "storage", "international-removals", "piano-moving"],
},
{
  "slug": "commercial-removals", "name": "Commercial Removals",
  "intro_video": "commercial-removals-intro",
  "h1": "Commercial & Office Removals in Sussex",
  "title": "Commercial Removals Sussex | Wolves Removals",
  "meta": "Office & commercial removals across Sussex and the South East. Minimal downtime, careful IT and equipment handling, fully insured. Get a free business move quote.",
  "teaser": "Office and business relocations planned for minimal downtime.",
  "lead": """<p>Get your business up and running quickly with <strong>commercial removals</strong> built around minimal downtime. We streamline the entire office relocation, including unpacking, and offer custom crating for delicate equipment.</p>""",
  "included": ["Planned out-of-hours and weekend moves to limit downtime",
               "Careful handling of IT, equipment and confidential files",
               "Custom crates for delicate or high-value items",
               "Fully insured, fully managed relocation"],
  "sections": [
    ("Office Moves Planned Around Your Business",
     """<p>Every commercial move is planned to keep disruption to an absolute minimum. We work around your operating hours &mdash; including evenings and weekends &mdash; and assign a dedicated coordinator to manage logistics, access and timings so your team is back to work fast.</p>
        <p>From single offices to multi-floor premises, we handle desks, storage units, server racks and specialist equipment with care, labelling and a clear floor plan so everything lands in the right place at your new premises.</p>"""),
    ("Who Our Commercial Service Suits",
     """<p>Our commercial relocation service is built for organisations that cannot afford a chaotic move &mdash; professional services firms, retailers, distributors, healthcare and care providers, schools, charities and growing SMEs across Sussex, Surrey, Hampshire and Kent, as well as longer-distance moves throughout the UK and into Europe. We are equally at home with a ten-person studio relocating across town and a multi-floor headquarters moving in phases over several weekends. Because we also handle <a href="/services/house-removals/">domestic and house removals</a>, business owners and directors who have used us personally know the standard of care we bring before they trust us with their company. Whatever the scale, the formula is the same: one coordinator, a written plan, the right crates and vehicles, and a crew that works out of hours so your business keeps trading.</p>"""),
  ],
  "faqs": [
    ("Can you move our office outside business hours?", """<p>Yes &mdash; we regularly run evening and weekend office moves to keep downtime to a minimum. We&rsquo;ll plan timings around your operations.</p>"""),
    ("Do you handle IT and server equipment?", """<p>We handle IT, equipment and confidential files with care, and offer <a href="/services/custom-crate-service/">custom crating</a> for sensitive items. We recommend your IT team manages disconnection/reconnection of servers.</p>"""),
    ("Can you store business stock or furniture?", """<p>Yes, our <a href="/services/storage/business-and-commercial-storage/">business and commercial storage</a> is ideal for phased moves, refurbishments or surplus stock and furniture.</p>"""),
    ("Is the commercial move insured?", """<p>Every commercial move is fully insured and carried out by our trained, experienced team. Request a free quote to discuss your requirements.</p>"""),
  ],
  "related": ["house-removals", "custom-crate-service", "storage", "contract-delivery-services", "full-packing-service", "man-and-van"],
},
{
  "slug": "european-removals", "name": "European Removals",
  "h1": "European Removals from Sussex",
  "title": "European Removals | Wolves Removals Sussex",
  "meta": "Door-to-door European removals from Sussex. Expert export packing, customs guidance and secure transport across the EU. Fully insured. Get a free European move quote.",
  "teaser": "Door-to-door moves across the EU with export packing and customs guidance.",
  "lead": """<p>Moving to or from Europe? Our <strong>European removals</strong> service handles your relocation door to door &mdash; with expert export packing, customs paperwork guidance and secure, tracked transport across the EU.</p>""",
  "included": ["Door-to-door European relocations", "Expert export packing and inventory",
               "Customs documentation guidance", "Part-load and full-load options", "Fully insured transport"],
  "sections": [
    ("Stress-Free Moves Across Europe",
     """<p>Relocating abroad brings extra considerations &mdash; paperwork, timing and the safe transport of your belongings over long distances. Our experienced team manages each stage, from a detailed inventory and professional <a href="/services/export-packing-service/">export packing</a> to coordinating delivery at your new European home.</p>
        <p>Whether you have a full household or a part-load, we&rsquo;ll plan the most efficient route and keep you updated throughout. Flexible <a href="/services/storage/">storage</a> is available at either end if your dates don&rsquo;t align.</p>"""),
    ("Packing & Paperwork Done Properly",
     """<p>Long-distance moves demand robust packing. Our export packing protects fragile and valuable items for the journey, and we provide guidance on the customs documentation you&rsquo;ll need. For antiques and fine art, our <a href="/services/specialised-antiques-moving/">specialist team</a> and <a href="/services/custom-crate-service/">custom crating</a> ensure everything arrives in the condition it left.</p>"""),
  ],
  "faqs": [
    ("Which European countries do you cover?", """<p>We arrange moves across the EU. Tell us your destination and we&rsquo;ll plan the route, timing and paperwork &mdash; <a href="/get-a-quote/">request a quote</a> to get started.</p>"""),
    ("Do you handle customs paperwork?", """<p>We guide you through the customs documentation required for your move. Requirements vary by destination, so we&rsquo;ll advise based on where you&rsquo;re heading.</p>"""),
    ("Can I move just a few items (part-load)?", """<p>Yes &mdash; we offer part-load options so you only pay for the space you need, which can be more cost-effective for smaller moves.</p>"""),
    ("Is my shipment insured?", """<p>Yes, your move is fully insured. We&rsquo;ll talk through cover so you&rsquo;re confident for the whole journey.</p>"""),
  ],
  "related": ["international-removals", "export-packing-service", "custom-crate-service", "full-packing-service", "storage", "specialised-antiques-moving"],
},
{
  "slug": "international-removals", "name": "International Removals",
  "h1": "International Removals from Sussex",
  "title": "International Removals | Wolves Removals",
  "meta": "Worldwide international removals from Sussex. Expert export packing, customs guidance, sea & air freight options. Fully insured. Get a free international move quote.",
  "teaser": "Worldwide relocations with export packing, freight and customs support.",
  "lead": """<p>We expertly handle your <strong>international move</strong> with great care &mdash; packing and loading your items securely, and unpacking them on arrival so everything is set up as needed, wherever in the world you&rsquo;re heading.</p>""",
  "included": ["Worldwide door-to-door relocations", "Sea and air freight options",
               "Professional export packing and crating", "Customs documentation guidance", "Fully insured shipments"],
  "sections": [
    ("Worldwide Moves, Handled With Care",
     """<p>An international move is a major undertaking, and the details matter. Our team plans your relocation end to end &mdash; a thorough inventory, professional <a href="/services/export-packing-service/">export packing</a>, the right freight option for your budget and timeline, and clear updates along the way.</p>
        <p>We protect fragile and high-value items with quality materials and <a href="/services/custom-crate-service/">bespoke crating</a>, and arrange secure <a href="/services/storage/">storage</a> at either end if needed.</p>"""),
    ("Freight, Customs & Delivery",
     """<p>Depending on your destination, budget and timescale we&rsquo;ll recommend sea or air freight and explain the trade-offs. We guide you through the customs paperwork and coordinate delivery and unpacking at your new home so the process feels manageable from start to finish.</p>"""),
  ],
  "faqs": [
    ("How long does an international move take?", """<p>Transit time depends on destination and freight method &mdash; air is faster, sea is more economical for larger loads. We&rsquo;ll give you a realistic timeline with your quote.</p>"""),
    ("Do you pack for international shipping?", """<p>Yes &mdash; robust <a href="/services/export-packing-service/">export packing</a> and crating are essential for long journeys, and our team handles it for you.</p>"""),
    ("Can you store items before shipping?", """<p>Yes, our secure <a href="/services/storage/">storage</a> bridges any gap before or after shipping.</p>"""),
    ("Is international transport insured?", """<p>Yes, your shipment is fully insured. We&rsquo;ll discuss the right level of cover for your move.</p>"""),
  ],
  "related": ["european-removals", "export-packing-service", "custom-crate-service", "specialised-antiques-moving", "storage", "full-packing-service"],
},
{
  "slug": "student-removals", "name": "Student Removals",
  "h1": "Student Removals in Sussex",
  "title": "Student Removals Sussex | Wolves Removals",
  "meta": "Affordable student removals across Sussex. Flexible moves to and from halls and shared houses, with optional storage between terms. Fully insured. Free quote.",
  "teaser": "Affordable, flexible moves to and from halls and shared houses.",
  "lead": """<p>Moving to or from university? Our affordable, flexible <strong>student removals</strong> take the hassle out of moving to and from halls and shared houses &mdash; with optional <a href="/services/student-storage/">storage between terms</a>.</p>""",
  "included": ["Affordable, flexible student moves", "Ideal for halls and shared houses",
               "Optional storage between terms", "Fully insured and reliable"],
  "sections": [
    ("Moves That Fit a Student Budget & Timetable",
     """<p>Student moves are often smaller and time-pressured &mdash; perfect for our cost-effective <a href="/services/man-and-van/">man and van</a> service. We&rsquo;ll move you between halls, shared houses and home efficiently, treating your belongings with the same care as a full house move.</p>
        <p>Need somewhere to keep things over summer or between tenancies? Our <a href="/services/student-storage/">student storage</a> is secure, flexible and affordable, so you don&rsquo;t have to haul everything home.</p>"""),
  ],
  "faqs": [
    ("How much do student removals cost?", """<p>Student moves are usually smaller, so they&rsquo;re among our most affordable jobs. <a href="/get-a-quote/">Request a quote</a> with your details for an accurate price.</p>"""),
    ("Can you store my things over summer?", """<p>Yes &mdash; our <a href="/services/student-storage/">student storage</a> is ideal for keeping belongings safe between terms or tenancies.</p>"""),
    ("Do you move single items or small loads?", """<p>Absolutely &mdash; our <a href="/services/man-and-van/">man and van</a> service is perfect for smaller loads and single items.</p>"""),
    ("Are student moves insured?", """<p>Yes, every move is fully insured and handled by our trained team.</p>"""),
  ],
  "related": ["man-and-van", "student-storage", "full-packing-service", "house-removals", "storage", "packing-materials"],
},
{
  "slug": "man-and-van", "name": "Man and Van",
  "h1": "Man and Van Services in Sussex",
  "title": "Man and Van Sussex | Wolves Removals",
  "meta": "Fully equipped man and van services across Sussex from £80. Ideal for small moves, students and single items. Trained, insured drivers. Get a free quote.",
  "teaser": "Cost-effective, fully equipped man and van for smaller moves.",
  "lead": """<p>Looking for the best <strong>man and van in Sussex</strong>? Our vans are in pristine condition, mechanically sound and fully equipped with blankets and straps for secure transport &mdash; bringing the same care as a full removal.</p>""",
  "included": ["Competitive prices with no hidden fees &mdash; from £80",
               "Fully equipped man and van services across Sussex",
               "Trained drivers and packers", "Ideal for small moves, students and single items"],
  "sections": [
    ("About Our Man and Van Services",
     """<p>Our man and van service across Sussex is ideally suited to students and people moving in and out of rental properties who have fewer items to move, making it an extremely cost-effective option. It&rsquo;s tempting to move items yourself by hiring a van and asking friends to help &mdash; but that often risks damage or injury.</p>
        <p>With Wolves Man and Van you get peace of mind that your belongings are handled by professionals, and you don&rsquo;t have to worry about hurting yourself or causing any damage. Our service is also ideal for office moves and business relocation &mdash; we can move anything to anywhere.</p>"""),
    ("Pricing & Key Terms",
     """<p>Transparent pricing with no hidden fees, starting from £80. A few key terms to note:</p>
        <ul class="tick-list"><li>Hourly charges apply from depot to depot</li><li>£0.45 per mile from depot to depot for fuel</li><li>Goods-in-transit insurance excluded if you choose the van and driver only option</li><li>Bookings are based on receipt of your deposit for our minimum charge</li></ul>
        <p>Please don&rsquo;t hesitate to <a href="/contact-us/">contact us</a> with any specific queries about our man and van or courier service.</p>"""),
  ],
  "faqs": [
    ("How much is a man and van in Sussex?", """<p>Our man and van service starts from £80, with hourly charges from depot to depot plus £0.45 per mile for fuel. <a href="/get-a-quote/">Request a quote</a> for your exact price.</p>"""),
    ("Is it suitable for a few items only?", """<p>Yes &mdash; it&rsquo;s ideal for single items, small loads, students and rental moves.</p>"""),
    ("Can you help with loading and lifting?", """<p>Yes, our trained team loads, secures and transports your items &mdash; you don&rsquo;t risk injury or damage doing it yourself.</p>"""),
    ("Do you cover business and office moves?", """<p>Absolutely &mdash; man and van is great for smaller office moves; for larger jobs see our <a href="/services/commercial-removals/">commercial removals</a>.</p>"""),
  ],
  "related": ["student-removals", "house-removals", "removal-services", "contract-delivery-services", "packing-materials", "storage"],
},
{
  "slug": "specialised-antiques-moving", "name": "Specialist Antique Moving", "video": "packing-paintings-promo",
  "h1": "Specialist Antique & Fine Art Moving",
  "title": "Antique & Fine Art Moving | Wolves Removals",
  "meta": "LAPADA-accredited specialist antique and fine art moving. Bespoke crating, white-glove handling and secure transport across Sussex and beyond. Free quote.",
  "teaser": "LAPADA-accredited handling of antiques, fine art and valuables.",
  "lead": """<p>As a <strong>LAPADA member</strong>, we move antiques, fine art and valuables with bespoke packing, crating and white-glove handling &mdash; the expertise your most precious items deserve.</p>""",
  "included": ["LAPADA-accredited antiques handling", "Bespoke crating and custom packing",
               "White-glove, condition-checked service", "Fully insured specialist transport"],
  "sections": [
    ("The Care Your Valuables Deserve",
     """<p>Antiques, fine art and heirlooms need more than ordinary packing. Our specialist team assesses each piece and uses the right materials and techniques &mdash; acid-free wrapping, made-to-measure <a href="/services/custom-crate-service/">crates</a> and padded transport &mdash; to protect against knocks, vibration and climate during the move.</p>
        <p>Our LAPADA membership reflects our commitment to the standards expected by dealers, collectors and estate agents such as Fine &amp; Country. We also offer a dedicated <a href="/services/white-glove-service/">white-glove service</a> for the highest level of care.</p>"""),
    ("Trusted by Collectors & Estate Agents",
     """<p>We&rsquo;re regularly recommended for delicate moves across Sussex, including <a href="/services/antiques-in-west-sussex/">antiques in West Sussex</a>. Every item is inventoried and condition-checked, and your move is fully insured for complete peace of mind.</p>"""),
  ],
  "faqs": [
    ("What does LAPADA accreditation mean?", """<p>LAPADA is the Association of Art &amp; Antiques Dealers. Our membership reflects recognised standards in handling and transporting valuable items.</p>"""),
    ("Do you make custom crates?", """<p>Yes &mdash; our <a href="/services/custom-crate-service/">custom crate service</a> builds made-to-measure crates for fragile and high-value pieces.</p>"""),
    ("Can you move a single valuable item?", """<p>Yes, from a single painting or clock to a full collection &mdash; <a href="/get-a-quote/">request a quote</a> and we&rsquo;ll tailor the service.</p>"""),
    ("Are antiques insured in transit?", """<p>Yes, your items are fully insured. We&rsquo;ll discuss appropriate cover given their value.</p>"""),
  ],
  "related": ["antiques-in-west-sussex", "white-glove-service", "custom-crate-service", "piano-moving", "fragile-packing", "international-removals"],
},
{
  "slug": "antiques-in-west-sussex", "name": "Antiques in West Sussex",
  "h1": "Antiques Moving in West Sussex",
  "title": "Antiques Moving West Sussex | Wolves Removals",
  "meta": "LAPADA-accredited antiques moving in West Sussex. Bespoke crating, white-glove handling and insured transport for dealers, collectors and homes. Free quote.",
  "teaser": "Local LAPADA-accredited antiques handling across West Sussex.",
  "lead": """<p>Based near Pulborough, we offer LAPADA-accredited <strong>antiques moving in West Sussex</strong> &mdash; bespoke crating, white-glove handling and fully insured transport for dealers, collectors and private homes.</p>""",
  "included": ["Local West Sussex antiques specialists", "LAPADA-accredited handling",
               "Bespoke crating and condition checks", "Fully insured transport"],
  "sections": [
    ("West Sussex's Antiques Moving Specialists",
     """<p>West Sussex has a rich antiques trade, and we&rsquo;re proud to serve dealers, auction houses, collectors and homeowners across the county. Our <a href="/services/specialised-antiques-moving/">specialist antiques team</a> handles everything from a single piece of furniture to a full collection with care, discretion and the right equipment.</p>
        <p>We use made-to-measure <a href="/services/custom-crate-service/">crates</a>, acid-free materials and our <a href="/services/white-glove-service/">white-glove service</a> for the most delicate items, and we&rsquo;re trusted by leading estate agents including Fine &amp; Country and Mansell McTaggart.</p>"""),
  ],
  "faqs": [
    ("Do you serve antiques dealers and auction houses?", """<p>Yes &mdash; we work with dealers, auction houses, collectors and private clients across West Sussex and beyond.</p>"""),
    ("Can you crate valuable pieces?", """<p>Yes, our <a href="/services/custom-crate-service/">custom crate service</a> protects high-value and fragile pieces for transport or storage.</p>"""),
    ("Are you accredited?", """<p>We are a LAPADA member, reflecting recognised standards in antiques and fine-art handling.</p>"""),
    ("Is the service insured?", """<p>Yes, every antiques move is fully insured. We&rsquo;ll talk through cover for valuable items.</p>"""),
  ],
  "related": ["specialised-antiques-moving", "white-glove-service", "custom-crate-service", "fragile-packing", "piano-moving", "storage"],
},
{
  "slug": "white-glove-service", "name": "White Glove Service",
  "h1": "White Glove Removals & Delivery Service",
  "title": "White Glove Service | Wolves Removals",
  "meta": "Premium white-glove removals and delivery: careful handling, placement, unpacking and debris removal for high-value items. Fully insured across Sussex. Free quote.",
  "teaser": "Premium, fully managed handling, placement and unpacking.",
  "lead": """<p>Our premium <strong>white-glove service</strong> is the highest level of care we offer &mdash; meticulous handling, room placement, assembly and unpacking, with all packaging removed so you can simply enjoy your new space.</p>""",
  "included": ["Premium, fully managed handling", "Placement, assembly and unpacking",
               "Packaging and debris removed", "Ideal for high-value and delicate items"],
  "sections": [
    ("Total Care, From Door to Final Placement",
     """<p>White-glove is ideal for high-value furniture, fine art, antiques and delicate items, or simply when you want a completely hands-off move. We handle every detail &mdash; protective packing, careful transport, precise placement in the right room, assembly where needed and full unpacking &mdash; then remove all packaging and debris.</p>
        <p>Combined with our <a href="/services/specialised-antiques-moving/">antiques expertise</a> and <a href="/services/custom-crate-service/">custom crating</a>, it&rsquo;s the most thorough, considerate service we provide.</p>"""),
  ],
  "faqs": [
    ("What's included in the white-glove service?", """<p>Protective packing, transport, room placement, assembly, full unpacking and removal of all packaging &mdash; a completely hands-off experience.</p>"""),
    ("Is it suitable for high-value items?", """<p>Yes &mdash; it&rsquo;s designed for high-value furniture, art and antiques, paired with our specialist handling and crating.</p>"""),
    ("Do you remove the packaging afterwards?", """<p>Yes, we take away all boxes and packaging so you can enjoy your new space straight away.</p>"""),
    ("Is the service insured?", """<p>Yes, fully insured throughout, with cover discussed for high-value items.</p>"""),
  ],
  "related": ["specialised-antiques-moving", "antiques-in-west-sussex", "custom-crate-service", "full-unpacking-service", "piano-moving", "house-removals"],
},
{
  "slug": "piano-moving", "name": "Piano Moving",
  "h1": "Piano Moving in Sussex",
  "title": "Piano Moving Sussex | Wolves Removals",
  "meta": "Expert piano moving across Sussex: uprights and grands moved safely with specialist equipment and trained movers. Fully insured. Get a free piano moving quote.",
  "teaser": "Safe, specialist moving of uprights and grand pianos.",
  "lead": """<p>Pianos are heavy, delicate and awkward &mdash; our specialist <strong>piano moving</strong> team uses the right equipment and technique to move uprights and grands safely, whatever the access.</p>""",
  "included": ["Uprights, baby grands and grand pianos", "Specialist equipment and trained movers",
               "Careful planning for tight access and stairs", "Fully insured handling"],
  "sections": [
    ("Moving Pianos Safely, Whatever the Access",
     """<p>A piano can weigh several hundred kilograms and is easily damaged if handled incorrectly &mdash; and it can injure people who try to move it without the right equipment. Our trained team uses piano boards, skates, padding and careful planning to navigate doorways, stairs and tight access safely.</p>
        <p>We move pianos as part of a full <a href="/services/house-removals/">house removal</a> or as a standalone job, and can arrange secure <a href="/services/storage/">storage</a> if needed. For other heavy or delicate items, ask about our <a href="/services/specialised-antiques-moving/">specialist handling</a>.</p>"""),
  ],
  "faqs": [
    ("Can you move a grand piano?", """<p>Yes &mdash; we move uprights, baby grands and full grands with the right equipment and trained movers.</p>"""),
    ("What about stairs or difficult access?", """<p>We plan each piano move around access &mdash; stairs, narrow doorways and tight turns &mdash; using boards, skates and padding to keep it safe.</p>"""),
    ("Will my piano need retuning after moving?", """<p>Pianos often benefit from tuning a few weeks after a move once they&rsquo;ve settled. We handle the move; you can arrange a tuner afterwards.</p>"""),
    ("Is piano moving insured?", """<p>Yes, fully insured. We&rsquo;ll discuss cover given the value of your instrument.</p>"""),
  ],
  "related": ["specialised-antiques-moving", "white-glove-service", "custom-crate-service", "house-removals", "man-and-van", "storage"],
},
{
  "slug": "custom-crate-service", "name": "Custom Crate Service", "video": "packing-mirror-promo",
  "h1": "Custom Crate Service",
  "title": "Custom Crate Service | Wolves Removals",
  "meta": "Made-to-measure custom crates for fragile, valuable and awkward items: antiques, art, equipment and machinery. Fully insured transport across Sussex. Free quote.",
  "teaser": "Made-to-measure crating for fragile, valuable and awkward items.",
  "lead": """<p>For the most fragile, valuable or awkward items, our <strong>custom crate service</strong> builds made-to-measure crates that protect against knocks, vibration and climate &mdash; for transport or long-term storage.</p>""",
  "included": ["Made-to-measure crates for any item", "Ideal for art, antiques, equipment and machinery",
               "Acid-free and cushioned internal packing", "Suitable for shipping and storage"],
  "sections": [
    ("Protection Built to Fit",
     """<p>Off-the-shelf boxes can&rsquo;t protect everything. We design and build bespoke crates around your item &mdash; fine art, antiques, sculptures, sensitive equipment or machinery &mdash; with cushioned, acid-free internal packing to hold it securely in place.</p>
        <p>Custom crating is essential for <a href="/services/international-removals/">international</a> and <a href="/services/european-removals/">European</a> shipping, and pairs with our <a href="/services/specialised-antiques-moving/">antiques</a> and <a href="/services/white-glove-service/">white-glove</a> services for total peace of mind.</p>"""),
  ],
  "faqs": [
    ("What items need a custom crate?", """<p>Fine art, antiques, sculptures, mirrors, sensitive equipment and machinery &mdash; anything fragile, high-value or awkwardly shaped.</p>"""),
    ("Can crates be used for shipping?", """<p>Yes &mdash; bespoke crates are ideal for <a href="/services/international-removals/">international</a> and <a href="/services/european-removals/">European</a> transport.</p>"""),
    ("Do you crate on-site?", """<p>We assess each item and build crating to suit; we&rsquo;ll advise the best approach when you request a quote.</p>"""),
    ("Is crated transport insured?", """<p>Yes, fully insured, with cover discussed for high-value items.</p>"""),
  ],
  "related": ["specialised-antiques-moving", "white-glove-service", "export-packing-service", "international-removals", "fragile-packing", "piano-moving"],
},
{
  "slug": "contract-delivery-services", "name": "Contract Delivery Services",
  "h1": "Contract Delivery Services",
  "title": "Contract Delivery Services | Wolves Removals",
  "meta": "Reliable contract delivery and courier services for businesses across Sussex and the South East. Careful handling, flexible scheduling, fully insured. Free quote.",
  "teaser": "Reliable B2B delivery and courier services with careful handling.",
  "lead": """<p>Our <strong>contract delivery services</strong> give businesses a reliable, careful delivery partner &mdash; from regular scheduled runs to one-off deliveries of furniture, equipment and high-value goods across Sussex and beyond.</p>""",
  "included": ["Regular scheduled or one-off deliveries", "Careful, white-glove handling available",
               "Flexible scheduling around your business", "Fully insured transport"],
  "sections": [
    ("A Delivery Partner You Can Rely On",
     """<p>For retailers, manufacturers, interior designers and offices, dependable delivery matters. We handle furniture, equipment and high-value goods with the same care as a full removal, and can provide <a href="/services/white-glove-service/">white-glove</a> placement and assembly where required.</p>
        <p>Whether you need recurring scheduled runs or occasional deliveries, we&rsquo;ll build a flexible arrangement around your business. Secure <a href="/services/storage/business-and-commercial-storage/">business storage</a> is also available.</p>"""),
  ],
  "faqs": [
    ("Do you offer regular scheduled deliveries?", """<p>Yes &mdash; we set up recurring runs or handle one-off deliveries to suit your business.</p>"""),
    ("Can you provide white-glove delivery?", """<p>Yes, with placement, assembly and packaging removal via our <a href="/services/white-glove-service/">white-glove service</a>.</p>"""),
    ("Do you store goods between deliveries?", """<p>Yes, our <a href="/services/storage/business-and-commercial-storage/">business storage</a> can hold stock between deliveries.</p>"""),
    ("Is delivery insured?", """<p>Yes, fully insured. Request a quote to discuss your contract requirements.</p>"""),
  ],
  "related": ["commercial-removals", "white-glove-service", "man-and-van", "storage", "custom-crate-service", "house-removals"],
},
{
  "slug": "house-clearance", "name": "House Clearance",
  "h1": "House Clearance in Sussex",
  "title": "House Clearance Sussex | Wolves Removals",
  "meta": "Respectful, responsible house clearance across Sussex. Full or part clearances, probate and downsizing, with recycling and donation where possible. Free quote.",
  "teaser": "Respectful full or part clearances, with responsible disposal.",
  "lead": """<p>Our <strong>house clearance</strong> service is handled respectfully and responsibly &mdash; whether you&rsquo;re downsizing, managing a probate property or clearing a rental, we&rsquo;ll do it sensitively and recycle or donate wherever possible.</p>""",
  "included": ["Full or part house clearances", "Sensitive probate and downsizing clearances",
               "Recycling and donation where possible", "Optional removals and storage combined"],
  "sections": [
    ("Sensitive, Responsible Clearances",
     """<p>Clearing a home can be an emotional and practical challenge, particularly after a bereavement or when downsizing. Our team works with care and discretion, sorting items for keeping, donating, recycling or disposal, and leaving the property clean and ready.</p>
        <p>We can combine clearance with a <a href="/services/house-removals/">house removal</a> and secure <a href="/services/storage/">storage</a> for items you wish to keep, making the whole process simpler at a difficult time.</p>"""),
  ],
  "faqs": [
    ("Do you handle probate clearances?", """<p>Yes &mdash; we carry out probate and bereavement clearances sensitively and discreetly, working to your timescale.</p>"""),
    ("What happens to the items?", """<p>We sort items for keeping, donation, recycling or responsible disposal, diverting from landfill wherever possible.</p>"""),
    ("Can you clear part of a property?", """<p>Yes, we offer full or part clearances to suit your needs.</p>"""),
    ("Can clearance be combined with a move?", """<p>Absolutely &mdash; we can clear, move and store in one coordinated service.</p>"""),
  ],
  "related": ["house-removals", "storage", "man-and-van", "full-packing-service", "removal-services", "commercial-removals"],
},
{
  "slug": "removal-services", "name": "Removal Services",
  "h1": "Removal Services in Sussex",
  "title": "Removal Services Sussex | Wolves Removals",
  "meta": "The full range of Wolves removal services across Sussex: home, commercial, man and van, packing, storage and specialist moves. Fully insured. Get a free quote.",
  "teaser": "An overview of our complete range of removal services.",
  "lead": """<p>Wolves Removals offers a complete range of professional <strong>removal services</strong> &mdash; whatever you need to move, however far, we can help, with one team and one point of contact from start to finish.</p>""",
  "included": ["Home, commercial and specialist removals", "Local, long-distance and international",
               "Packing, storage and delivery options", "Fully insured, family-run since 2016"],
  "sections": [
    ("Everything You Need to Move, Under One Roof",
     """<p>From a single item to a full home or office, we tailor our service to your move. Our core services include <a href="/services/house-removals/">house removals</a>, <a href="/services/commercial-removals/">commercial removals</a>, flexible <a href="/services/man-and-van/">man and van</a>, and long-distance, <a href="/services/european-removals/">European</a> and <a href="/services/international-removals/">international</a> moves.</p>
        <p>Add professional <a href="/services/full-packing-service/">packing</a>, secure <a href="/services/storage/">storage</a> and specialist handling for <a href="/services/piano-moving/">pianos</a> and <a href="/services/specialised-antiques-moving/">antiques</a>, and you have a single, reliable partner for the whole move.</p>"""),
  ],
  "faqs": [
    ("What types of move do you cover?", """<p>Home, commercial, student and specialist moves &mdash; local, long-distance, European and worldwide.</p>"""),
    ("Can you pack and store too?", """<p>Yes &mdash; we offer full <a href="/services/full-packing-service/">packing</a> and secure <a href="/services/storage/">storage</a> alongside removals.</p>"""),
    ("Do you move single items?", """<p>Yes, our <a href="/services/man-and-van/">man and van</a> service is perfect for single items and small loads.</p>"""),
    ("Are all services insured?", """<p>Yes, every service is fully insured and delivered by our trained team.</p>"""),
  ],
  "related": ["house-removals", "commercial-removals", "man-and-van", "international-removals", "storage", "full-packing-service"],
},
{
  "slug": "full-packing-service", "name": "Full Packing Service", "video": ["packing-plates-promo", "packing-books-promo"],
  "h1": "Full Packing Service",
  "title": "Full Packing Service | Wolves Removals Sussex",
  "meta": "Professional full packing service across Sussex. Trained packers, quality materials and careful labelling protect your belongings. Fully insured. Get a free quote.",
  "teaser": "Trained packers and quality materials for a hassle-free move.",
  "lead": """<p>Let our trained team take the strain with our <strong>full packing service</strong> &mdash; we carefully pack every room with quality materials and clear labelling, so your belongings are protected and your move runs smoothly.</p>""",
  "included": ["Whole-home professional packing", "Quality materials and clear labelling",
               "Careful handling of fragile items", "Optional unpacking on arrival"],
  "sections": [
    ("Packing Done Properly, Room by Room",
     """<p>Packing is where most moving damage is prevented or caused. Our experienced packers use sturdy boxes, bubble wrap, paper and purpose-made cartons for items like glass, china and wardrobes, labelling everything by room for a smooth unload.</p>
        <p>Prefer to pack some yourself? You can buy <a href="/services/packing-materials/">packing materials</a> from our <a href="/box-shop/">box shop</a>, or add <a href="/services/fragile-packing/">fragile-only packing</a> for your most delicate items. We can also <a href="/services/full-unpacking-service/">unpack</a> at the other end.</p>"""),
  ],
  "faqs": [
    ("How long does packing take?", """<p>It depends on the size of your home &mdash; typically a day for an average house. We&rsquo;ll schedule packing before moving day.</p>"""),
    ("Do you supply the materials?", """<p>Yes &mdash; all boxes and materials are included in the packing service, or buy them separately from our <a href="/box-shop/">box shop</a>.</p>"""),
    ("Can you pack just the fragile items?", """<p>Yes, see our <a href="/services/fragile-packing/">fragile packing</a> service for delicate items only.</p>"""),
    ("Do you unpack as well?", """<p>Yes &mdash; add our <a href="/services/full-unpacking-service/">unpacking service</a> to settle in faster.</p>"""),
  ],
  "related": ["fragile-packing", "full-unpacking-service", "packing-materials", "export-packing-service", "house-removals", "storage"],
},
{
  "slug": "full-unpacking-service", "name": "Full Unpacking Service",
  "h1": "Full Unpacking Service",
  "title": "Full Unpacking Service | Wolves Removals",
  "meta": "Professional unpacking service across Sussex: we unpack, place items and remove packaging so you settle into your new home fast. Fully insured. Get a free quote.",
  "teaser": "We unpack, place your items and take away the packaging.",
  "lead": """<p>Settle in faster with our <strong>full unpacking service</strong> &mdash; we unpack your boxes, place items where you want them and remove all the packaging, so your new home is ready to enjoy.</p>""",
  "included": ["Complete unpacking on arrival", "Items placed where you want them",
               "All packaging removed", "Pairs perfectly with our packing service"],
  "sections": [
    ("Walk Into a Home That's Ready",
     """<p>Unpacking is often the most daunting part of a move. Our team makes short work of it &mdash; unpacking room by room, placing items thoughtfully and removing all the boxes and packaging so you&rsquo;re not left with a mountain of cardboard.</p>
        <p>Combine it with our <a href="/services/full-packing-service/">full packing service</a> for a truly hands-free move, or our premium <a href="/services/white-glove-service/">white-glove service</a> for placement and assembly too.</p>"""),
  ],
  "faqs": [
    ("Do you take the boxes away?", """<p>Yes &mdash; we remove all packaging and boxes so you can enjoy your new home straight away.</p>"""),
    ("Can you unpack only certain rooms?", """<p>Yes, we&rsquo;ll unpack as much or as little as you like &mdash; just tell us your priorities.</p>"""),
    ("Is unpacking available with any move?", """<p>Yes, it can be added to any removal. It pairs especially well with our <a href="/services/full-packing-service/">packing service</a>.</p>"""),
    ("Is it insured?", """<p>Yes, every service is fully insured and handled by our trained team.</p>"""),
  ],
  "related": ["full-packing-service", "white-glove-service", "house-removals", "packing-materials", "fragile-packing", "storage"],
},
{
  "slug": "fragile-packing", "name": "Fragile Packing",
  "h1": "Fragile Packing Service",
  "title": "Fragile Packing Service | Wolves Removals",
  "meta": "Expert fragile packing across Sussex: glassware, china, art and delicate items packed with specialist materials by trained packers. Fully insured. Free quote.",
  "teaser": "Specialist packing for glassware, china, art and delicates.",
  "lead": """<p>Some things need extra care. Our <strong>fragile packing</strong> service protects glassware, china, mirrors, art and delicate items with specialist materials and techniques, so they arrive exactly as they left.</p>""",
  "included": ["Specialist packing for delicate items", "Glassware, china, mirrors and art",
               "Quality cushioning and purpose-made cartons", "Fully insured handling"],
  "sections": [
    ("Extra Protection Where It Matters",
     """<p>Fragile items are the most common casualties of a move. Our trained packers wrap and cushion each piece individually, using purpose-made cartons, dividers and plenty of padding, and label boxes clearly so they&rsquo;re handled with care throughout.</p>
        <p>For especially valuable or awkward pieces, we offer <a href="/services/custom-crate-service/">custom crating</a> and <a href="/services/specialised-antiques-moving/">specialist antiques handling</a>. Need everything packed? See our <a href="/services/full-packing-service/">full packing service</a>.</p>"""),
  ],
  "faqs": [
    ("What counts as fragile?", """<p>Glassware, china, ceramics, mirrors, framed art, lamps and ornaments &mdash; anything breakable or delicate.</p>"""),
    ("Can you pack only the fragile items?", """<p>Yes &mdash; fragile-only packing lets you pack the rest yourself while we protect the delicate items.</p>"""),
    ("Do you crate very valuable pieces?", """<p>Yes, our <a href="/services/custom-crate-service/">custom crate service</a> is ideal for high-value or awkward items.</p>"""),
    ("Are fragile items insured?", """<p>Yes, fully insured. We&rsquo;ll discuss cover for high-value pieces.</p>"""),
  ],
  "related": ["full-packing-service", "non-fragile-packing-service", "custom-crate-service", "specialised-antiques-moving", "packing-materials", "export-packing-service"],
},
{
  "slug": "non-fragile-packing-service", "name": "Non-Fragile Packing Service",
  "h1": "Non-Fragile Packing Service",
  "title": "Non-Fragile Packing | Wolves Removals Sussex",
  "meta": "Efficient non-fragile packing across Sussex: books, clothing, linens and everyday items boxed and labelled by our team. Save time on moving day. Free quote.",
  "teaser": "Efficient boxing of books, clothes, linens and everyday items.",
  "lead": """<p>Our <strong>non-fragile packing service</strong> takes care of the bulky, time-consuming items &mdash; books, clothing, linens and everyday belongings &mdash; boxed and labelled efficiently so moving day runs smoothly.</p>""",
  "included": ["Efficient packing of everyday items", "Books, clothing, linens and kitchenware",
               "Clear room-by-room labelling", "Combine with fragile packing as needed"],
  "sections": [
    ("Save Time on the Heavy Lifting of Packing",
     """<p>Even non-fragile items take hours to pack well. Our team boxes books, clothes, linens, kitchenware and general belongings quickly and neatly, labelling by room so unloading is straightforward.</p>
        <p>Pair it with our <a href="/services/fragile-packing/">fragile packing</a> for delicate items, or step up to our <a href="/services/full-packing-service/">full packing service</a> to have everything done for you. Materials are available from our <a href="/box-shop/">box shop</a>.</p>"""),
  ],
  "faqs": [
    ("What's the difference from fragile packing?", """<p>Non-fragile covers durable, everyday items; <a href="/services/fragile-packing/">fragile packing</a> uses specialist materials for breakables.</p>"""),
    ("Can I combine both services?", """<p>Yes &mdash; many customers use non-fragile packing plus fragile packing for the best of both.</p>"""),
    ("Do you label the boxes?", """<p>Yes, everything is labelled by room for a smooth, organised unload.</p>"""),
    ("Is it insured?", """<p>Yes, fully insured and handled by our trained team.</p>"""),
  ],
  "related": ["fragile-packing", "full-packing-service", "packing-materials", "full-unpacking-service", "house-removals", "storage"],
},
{
  "slug": "export-packing-service", "name": "Export Packing Service", "video": "packing-wine-glasses-promo",
  "hero": "wrapping-framed-picture-for-export",
  "video_writeup": """<h2 class="relative leading-tight text-black">Wrapping &amp; Protecting Items for Export</h2>
<p>Before anything is crated for shipping, our packers protect it by hand &mdash; furniture wrapped in Furni-Soft padding, fragile pieces cushioned in bubble and foam, and every corner and edge covered. It&rsquo;s the same hands-on care you can see in the video.</p>
<p>That preparation is what gets your belongings through the knocks of long-distance and overseas transport. Each item is then load-secured and, where it&rsquo;s needed, sealed inside a bespoke <a href="/services/custom-crate-service/">export crate</a> &mdash; so it arrives exactly as it left.</p>""",
  "h1": "Export Packing Service",
  "title": "Export Packing Service | Wolves Removals",
  "meta": "Professional export packing for international and European moves: robust materials, crating and inventory for long-distance transport. Fully insured. Free quote.",
  "teaser": "Robust packing and crating for international shipping.",
  "lead": """<p>Long journeys demand stronger protection. Our <strong>export packing service</strong> prepares your belongings for <a href="/services/international-removals/">international</a> and <a href="/services/european-removals/">European</a> transport with robust materials, crating and a detailed inventory.</p>""",
  "included": ["Robust packing for long-distance transport", "Custom crating for fragile and valuable items",
               "Detailed inventory for customs", "Fully insured shipments"],
  "sections": [
    ("Packed to Travel the Distance",
     """<p>Items shipped overseas face handling, vibration and changing climates. Our export packing uses heavy-duty materials, moisture protection and made-to-measure <a href="/services/custom-crate-service/">crates</a> for fragile and high-value pieces, with a detailed inventory to support customs clearance.</p>
        <p>It&rsquo;s an essential part of any <a href="/services/international-removals/">international</a> or <a href="/services/european-removals/">European</a> move, and pairs with our <a href="/services/specialised-antiques-moving/">antiques</a> expertise for valuables.</p>"""),
  ],
  "faqs": [
    ("Why is export packing different?", """<p>It uses stronger materials, crating and moisture protection to withstand long journeys, handling and climate changes.</p>"""),
    ("Do you provide an inventory?", """<p>Yes &mdash; a detailed inventory supports customs clearance and insurance.</p>"""),
    ("Can you crate valuables?", """<p>Yes, our <a href="/services/custom-crate-service/">custom crate service</a> protects fragile and high-value items for shipping.</p>"""),
    ("Is the shipment insured?", """<p>Yes, fully insured. We&rsquo;ll discuss appropriate cover for your move.</p>"""),
  ],
  "related": ["international-removals", "european-removals", "custom-crate-service", "fragile-packing", "full-packing-service", "specialised-antiques-moving"],
},
{
  "slug": "packing-materials", "name": "Packing Materials (Box Shop)",
  "h1": "Packing Materials & Box Shop",
  "title": "Packing Materials & Box Shop | Wolves Removals",
  "meta": "Quality packing materials from the Wolves box shop: moving boxes, tape, bubble wrap, paper and wardrobe cartons. Pick up locally in Sussex. Get in touch.",
  "teaser": "Quality moving boxes and materials for a DIY pack.",
  "lead": """<p>Packing yourself? Our <a href="/box-shop/"><strong>box shop</strong></a> supplies quality <strong>packing materials</strong> &mdash; sturdy moving boxes, tape, bubble wrap, packing paper and wardrobe cartons &mdash; so your belongings travel safely.</p>""",
  "included": ["Sturdy double-walled moving boxes", "Tape, bubble wrap and packing paper",
               "Wardrobe cartons and specialist boxes", "Local pick-up in Sussex"],
  "sections": [
    ("Everything You Need to Pack Well",
     """<p>Good materials make all the difference. We supply strong, double-walled boxes in various sizes, plus tape, bubble wrap, packing paper and purpose-made cartons for wardrobes, glass and china &mdash; the same quality our own packers use.</p>
        <p>Prefer to leave it to us? Our <a href="/services/full-packing-service/">full</a>, <a href="/services/fragile-packing/">fragile</a> and <a href="/services/non-fragile-packing-service/">non-fragile</a> packing services take care of everything.</p>"""),
  ],
  "faqs": [
    ("Where do I collect packing materials?", """<p>Materials can be collected locally &mdash; <a href="/contact-us/">contact us</a> to arrange what you need and pick-up.</p>"""),
    ("What boxes do you recommend?", """<p>Double-walled small boxes for heavy items like books, larger boxes for light bulky items, and wardrobe cartons for hanging clothes.</p>"""),
    ("Do you offer a packing service too?", """<p>Yes &mdash; see our <a href="/services/full-packing-service/">full packing service</a> if you&rsquo;d rather not pack yourself.</p>"""),
    ("Can I get materials with my move?", """<p>Yes, we can supply materials as part of your booking &mdash; just ask when you request a quote.</p>"""),
  ],
  "related": ["full-packing-service", "fragile-packing", "non-fragile-packing-service", "house-removals", "man-and-van", "storage"],
},
{
  "slug": "storage", "name": "Storage", "video": "storage-container-promo-b",
  "hero": "containerised-storage-units-wolves-store",
  "h1": "Secure Storage in Sussex",
  "title": "Secure Storage Sussex | Wolves Removals",
  "meta": "Clean, dry, ultra-secure containerised storage in Sussex. Short and long-term options for home and business, fully managed including packing. Get a free quote.",
  "teaser": "Clean, dry, containerised storage for home and business.",
  "lead": """<p>Need somewhere to keep your belongings? Our clean, dry, ultra-secure <strong>containerised storage</strong> in Sussex suits both home and business, short or long-term, and is fully managed including packing and handling.</p>""",
  "included": ["Clean, dry, ultra-secure containerised storage", "Short and long-term flexible terms",
               "Fully managed including packing and handling", "Home and business storage"],
  "sections": [
    ("Storage That Flexes Around Your Move",
     """<p>Whether you&rsquo;re between properties, downsizing, renovating or freeing up space, our containerised storage keeps your belongings safe and accessible. Items are professionally packed and sealed into containers, protected from damp and damage, and stored securely.</p>
        <p>Choose <a href="/services/storage/short-term-storage/">short-term storage</a> for moving delays, <a href="/services/storage/long-term-storage/">long-term storage</a> for extended needs, or <a href="/services/storage/business-and-commercial-storage/">business storage</a> for stock and equipment. Use our free <a href="/storage-calculator/">storage calculator</a> to estimate the space you need.</p>"""),
  ],
  "faqs": [
    ("How is my furniture stored?", """<p>Items are professionally packed and sealed into containers, kept clean, dry and secure &mdash; not loose on open shelving.</p>"""),
    ("Can I access my belongings?", """<p>Access can be arranged &mdash; let us know your needs and we&rsquo;ll explain how it works for your storage.</p>"""),
    ("How much storage will I need?", """<p>Use our free <a href="/storage-calculator/">storage calculator</a> for an estimate, or we&rsquo;ll assess it during your quote.</p>"""),
    ("Is stored property insured?", """<p>Yes &mdash; we&rsquo;ll talk through insurance options for items in storage.</p>"""),
  ],
  "related": ["storage/short-term-storage", "storage/long-term-storage", "storage/business-and-commercial-storage", "student-storage", "house-removals", "full-packing-service"],
},
{
  "slug": "storage/long-term-storage", "name": "Long-Term Storage",
  "h1": "Long-Term Storage in Sussex",
  "title": "Long-Term Storage Sussex | Wolves Removals",
  "meta": "Affordable long-term storage in Sussex from 3 months. Clean, dry, ultra-secure containerised storage for home and business, fully managed. Get a free quote.",
  "teaser": "Affordable containerised storage from 3 months or more.",
  "lead": """<p>Ideal for storage between moves, downsizing or freeing up space, our <strong>long-term storage</strong> offers flexible, affordable terms from three months or more &mdash; clean, dry and ultra-secure.</p>""",
  "included": ["Flexible terms from 3 months or more", "Clean, dry, ultra-secure containers",
               "Fully managed including packing", "Affordable long-term rates"],
  "sections": [
    ("Long-Term Storage That's Simple & Secure",
     """<p>When you need to store belongings for an extended period &mdash; during a long renovation, an overseas posting, or while you decide on next steps &mdash; our containerised long-term storage keeps everything protected from damp and damage at affordable rates.</p>
        <p>We pack and seal your items into containers, and can combine storage with a <a href="/services/house-removals/">house removal</a>. For shorter needs, see <a href="/services/storage/short-term-storage/">short-term storage</a>; for stock and equipment, <a href="/services/storage/business-and-commercial-storage/">business storage</a>.</p>"""),
  ],
  "faqs": [
    ("What's the minimum term?", """<p>Long-term storage starts from three months, with flexible, affordable rates for longer periods.</p>"""),
    ("Is my furniture protected?", """<p>Yes &mdash; items are packed and sealed into clean, dry, secure containers, protected from damp and damage.</p>"""),
    ("Can I add or remove items later?", """<p>Access and adjustments can be arranged &mdash; just let us know your needs.</p>"""),
    ("How much will I need?", """<p>Use our <a href="/storage-calculator/">storage calculator</a> or we&rsquo;ll assess it with your quote.</p>"""),
  ],
  "related": ["storage", "storage/short-term-storage", "storage/business-and-commercial-storage", "student-storage", "house-removals", "full-packing-service"],
},
{
  "slug": "storage/short-term-storage", "name": "Short-Term Storage",
  "h1": "Short-Term Storage in Sussex",
  "title": "Short-Term Storage Sussex | Wolves Removals",
  "meta": "Flexible short-term storage in Sussex from a few days. Clean, dry, secure containerised storage for moving delays and renovations. Get a free quote.",
  "teaser": "Flexible storage from a couple of days to a few months.",
  "lead": """<p>Perfect for moving delays, renovations or temporary transitions, our <strong>short-term storage</strong> covers anything from a couple of days to a few months &mdash; clean, dry and secure.</p>""",
  "included": ["Flexible terms from a couple of days", "Clean, dry, secure containers",
               "Ideal for moving delays and renovations", "Fully managed handling"],
  "sections": [
    ("Bridge the Gap Between Properties",
     """<p>Completion dates rarely line up perfectly. Short-term storage bridges the gap &mdash; we keep your belongings safe and sealed in containers until you&rsquo;re ready, whether that&rsquo;s a few days or a few months.</p>
        <p>It pairs naturally with a <a href="/services/house-removals/">house removal</a>, and you can move up to <a href="/services/storage/long-term-storage/">long-term storage</a> if your plans change. Estimate your space with our <a href="/storage-calculator/">storage calculator</a>.</p>"""),
  ],
  "faqs": [
    ("How short can I store for?", """<p>From just a couple of days &mdash; short-term storage is fully flexible to your timeline.</p>"""),
    ("Is it secure for valuables?", """<p>Yes &mdash; clean, dry, sealed containers in a secure facility, with insurance options available.</p>"""),
    ("Can I extend if needed?", """<p>Yes, you can extend or move to <a href="/services/storage/long-term-storage/">long-term storage</a> if your plans change.</p>"""),
    ("How much space will I need?", """<p>Try our <a href="/storage-calculator/">storage calculator</a> or we&rsquo;ll assess it with your quote.</p>"""),
  ],
  "related": ["storage", "storage/long-term-storage", "storage/business-and-commercial-storage", "student-storage", "house-removals", "man-and-van"],
},
{
  "slug": "storage/business-and-commercial-storage", "name": "Business & Commercial Storage",
  "h1": "Business & Commercial Storage",
  "title": "Business & Commercial Storage | Wolves Removals",
  "meta": "Secure business and commercial storage in Sussex for stock, equipment, office furniture and archives. Fully managed, flexible terms. Get a free quote.",
  "teaser": "Secure, managed storage for stock, equipment and archives.",
  "lead": """<p>Our <strong>business and commercial storage</strong> provides secure space for stock, equipment, office furniture and archives &mdash; a fully managed service, including packing and unpacking, that flexes with your business.</p>""",
  "included": ["Secure storage for stock and equipment", "Office furniture and archive storage",
               "Fully managed, including packing", "Flexible terms for phased moves"],
  "sections": [
    ("Storage That Works for Your Business",
     """<p>Whether you&rsquo;re relocating, refurbishing or simply short on space, our containerised business storage keeps stock, equipment, furniture and records secure and accessible. We can collect, pack and store, and deliver back when you need it.</p>
        <p>It works hand in hand with our <a href="/services/commercial-removals/">commercial removals</a> and <a href="/services/contract-delivery-services/">contract delivery</a> services for a seamless, fully managed solution.</p>"""),
  ],
  "faqs": [
    ("What can I store?", """<p>Stock, equipment, office furniture, archives and records &mdash; we&rsquo;ll advise on the right setup for your items.</p>"""),
    ("Can you collect and deliver?", """<p>Yes &mdash; combined with our <a href="/services/commercial-removals/">commercial removals</a> and <a href="/services/contract-delivery-services/">delivery</a> services.</p>"""),
    ("Is it flexible for phased moves?", """<p>Yes, flexible terms suit refurbishments, relocations and seasonal stock.</p>"""),
    ("Is business storage insured?", """<p>We&rsquo;ll discuss insurance options for stored business goods.</p>"""),
  ],
  "related": ["storage", "commercial-removals", "contract-delivery-services", "storage/long-term-storage", "storage/short-term-storage", "custom-crate-service"],
},
{
  "slug": "student-storage", "name": "Student Storage",
  "h1": "Student Storage in Sussex",
  "title": "Student Storage Sussex | Wolves Removals",
  "meta": "Affordable, secure student storage in Sussex between terms and tenancies. Flexible short-term storage plus collection and delivery. Get a free quote.",
  "teaser": "Affordable, secure storage between terms and tenancies.",
  "lead": """<p>Don&rsquo;t lug everything home for the holidays. Our affordable, secure <strong>student storage</strong> keeps your belongings safe between terms and tenancies &mdash; with flexible terms and optional collection and delivery.</p>""",
  "included": ["Affordable, secure student storage", "Flexible terms between terms and tenancies",
               "Optional collection and delivery", "Clean, dry containers"],
  "sections": [
    ("Storage Built Around Student Life",
     """<p>End of term, a year abroad or a gap between tenancies &mdash; student storage saves you carting everything home and back. We keep your belongings clean, dry and secure, and our <a href="/services/man-and-van/">man and van</a> service can collect and deliver to make it effortless.</p>
        <p>It pairs perfectly with our affordable <a href="/services/student-removals/">student removals</a>, and you can choose <a href="/services/storage/short-term-storage/">short</a> or <a href="/services/storage/long-term-storage/">long-term</a> terms to suit.</p>"""),
  ],
  "faqs": [
    ("Can you collect from my halls or house?", """<p>Yes &mdash; our <a href="/services/man-and-van/">man and van</a> service can collect and deliver your belongings.</p>"""),
    ("How long can I store for?", """<p>As long as you need &mdash; flexible short and long-term terms cover summers, years abroad and gaps between tenancies.</p>"""),
    ("Is it affordable for students?", """<p>Yes, student storage is among our most affordable options. <a href="/get-a-quote/">Request a quote</a> for details.</p>"""),
    ("Is my stuff secure?", """<p>Yes &mdash; clean, dry, secure containers, with insurance options available.</p>"""),
  ],
  "related": ["student-removals", "storage", "storage/short-term-storage", "man-and-van", "packing-materials", "storage/long-term-storage"],
},
]

# expose all slugs for nav/audit if needed
SLUGS = [s["slug"] for s in SERVICES]
