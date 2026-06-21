# -*- coding: utf-8 -*-
"""Build the helpful-tips hub + 7 advice articles, and the storage calculator.
Article content authored from the live topics + removals domain knowledge.
Each tip: hero + prose sections + FAQ (+schema) + related tips + CTA. URLs match live."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
from engine import esc, icon, img, section, prose, card_grid, cta_band, faq_block

HERO = "images/photos/professionally-packed-moving-boxes-ready.webp"

def hero(h1, lead, photo=None):
    src = ("images/photos/" + photo[0] + ".webp") if photo else HERO
    hero_img = img(src, "Wolves Removals moving tips in Sussex", cls="w-full h-full object-cover", eager=True)
    return ('<section class="relative w-full bg-darkgrey text-white overflow-hidden flex items-center min-h-[30rem] lg:min-h-[36rem]">'
            f'<div class="absolute inset-0">{hero_img}</div>'
            '<div class="container relative z-10 w-full py-[3.6rem] lg:py-[7.2rem]"><div class="grid grid-cols-12"><div class="col-span-12 lg:col-span-7 hero-panel">'
            f'<h1 class="text-3xl lg:text-5xl font-bold leading-tight">{h1}</h1>'
            f'<div class="mt-4 text-lg xl:text-xl max-w-3xl">{lead}</div>'
            f'{E.hero_review_row()}'
            '</div></div></div></section>')

TIPS = [
{
  "slug": "5-top-tips-for-moving-home", "name": "5 Top Tips for Moving Home",
  "title": "5 Top Tips for Moving Home | Wolves Removals",
  "meta": "Five practical tips for a smoother house move from Wolves Removals — plan early, declutter, pack smart, label clearly and pack an essentials box.",
  "lead": "Moving home should be exciting, not overwhelming. These five practical tips will help your move go smoothly.",
  "body": """<p>Moving to a new home is one of life&rsquo;s biggest events &mdash; exciting, but easily stressful without a plan. After thousands of moves across Sussex since 2016, we&rsquo;ve learned what makes the difference. Here are our five top tips for a smoother, calmer move.</p>
<h2>1. Start Planning Early</h2>
<p>The single biggest factor in a stress-free move is time. As soon as your date is confirmed, start a moving checklist and work backwards. Book your removals company early to secure your preferred date &mdash; especially over summer and at month-ends when demand peaks. Notify utilities, redirect your post, and update your address with banks, your GP and the DVLA in good time. A little planning now prevents a last-minute scramble later.</p>
<h2>2. Declutter Before You Pack</h2>
<p>There&rsquo;s no point paying to move things you no longer want. Go room by room and sort items to keep, donate, sell or recycle. Less to move means a quicker, cheaper move &mdash; and a fresh start in your new home. If you&rsquo;re unsure about bulky items, our <a href="/services/house-clearance/">house clearance</a> service can help.</p>
<h2>3. Pack Smart, Room by Room</h2>
<p>Use sturdy, good-quality boxes &mdash; small boxes for heavy items like books, larger ones for light, bulky things. Wrap fragile items individually and fill gaps so nothing shifts in transit. Pack one room at a time to stay organised. If packing feels daunting, our <a href="/services/full-packing-service/">full packing service</a> does it all for you, and you can buy <a href="/services/packing-materials/">quality materials</a> from our box shop.</p>
<h2>4. Label Everything Clearly</h2>
<p>Label each box with its contents and the room it belongs to &mdash; on the side, not just the top, so you can read it when boxes are stacked. Mark fragile boxes clearly. This makes unloading far quicker and means everything ends up in the right room, ready to unpack.</p>
<h2>5. Pack an Essentials Box</h2>
<p>Pack a clearly marked box of first-night essentials: kettle, mugs, tea and coffee, phone chargers, toiletries, medication, a change of clothes, basic tools and any children&rsquo;s or pets&rsquo; must-haves. Keep it with you so you&rsquo;re not hunting through boxes on your first tired evening.</p>
<p>Follow these five tips and your move will feel far more manageable. And if you&rsquo;d like an experienced, fully insured team to take the strain, <a href="/get-a-quote/">request a free quote</a> &mdash; we&rsquo;re always happy to help.</p>""",
  "faqs": [("How early should I book a removals company?", "<p>As early as you can &mdash; ideally several weeks ahead, especially for summer or month-end moves. <a href=\"/get-a-quote/\">Request a quote</a> to secure your date.</p>"),
           ("Should I pack myself or use a packing service?", "<p>Either works. Packing yourself saves money; our <a href=\"/services/full-packing-service/\">packing service</a> saves time and protects fragile items. Many customers mix the two.</p>"),
           ("What should go in my essentials box?", "<p>Kettle, mugs, tea/coffee, chargers, toiletries, medication, a change of clothes and basic tools &mdash; anything you&rsquo;ll need on your first night.</p>"),
           ("Can you help me declutter before moving?", "<p>Yes &mdash; our <a href=\"/services/house-clearance/\">house clearance</a> service can remove unwanted items responsibly before your move.</p>")],
},
{
  "slug": "money-saving-tips-when-moving-house", "name": "Money-Saving Tips When Moving House",
  "title": "Money-Saving Tips When Moving House | Wolves Removals",
  "meta": "Practical money-saving tips for your house move: declutter, be flexible on dates, pack yourself, compare quotes and book early. Advice from Wolves Removals Sussex.",
  "lead": "Moving doesn&rsquo;t have to break the bank. Here&rsquo;s how to keep the cost of your house move down without cutting corners.",
  "body": """<p>Moving home comes with plenty of costs, but with a little planning you can keep your removal affordable. Here are our practical money-saving tips, drawn from years of helping people move across Sussex.</p>
<h2>Declutter Before You Move</h2>
<p>Removal costs are driven largely by volume &mdash; the more you move, the more it costs. Decluttering before you pack is the easiest way to save. Sell, donate or recycle what you no longer need, and you&rsquo;ll cut both the size and the price of your move.</p>
<h2>Be Flexible on Your Moving Date</h2>
<p>Demand peaks on Fridays, at weekends and at the end of the month. If you can be flexible &mdash; a mid-week, mid-month move &mdash; you may find better availability and value. Booking early also helps you secure the date you want.</p>
<h2>Do Some of Your Own Packing</h2>
<p>Packing the non-fragile items yourself &mdash; books, clothes, linens &mdash; reduces the labour time on the day. Buy <a href="/services/packing-materials/">quality materials</a> from our <a href="/box-shop/">box shop</a> and leave the delicate items to our <a href="/services/fragile-packing/">fragile packing</a> service. It&rsquo;s a sensible balance of saving and protection.</p>
<h2>Get a Proper Quote &mdash; and Compare Fairly</h2>
<p>A vague phone estimate often hides extras. Insist on a clear, written quote based on a proper survey (video or in-home), and compare like for like &mdash; insurance, packing and any additional charges included. At Wolves Removals we quote transparently with <strong>no hidden fees</strong>, so the price you&rsquo;re given is the price you pay. See our <a href="/pricing/">pricing guide</a>.</p>
<h2>Consider a Man and Van for Smaller Moves</h2>
<p>If you&rsquo;re moving a flat, a few items or as a student, a full removal may be more than you need. Our <a href="/services/man-and-van/">man and van</a> service starts from £80 and brings the same care at a lower cost.</p>
<h2>Use Storage to Avoid a Double Move</h2>
<p>If your completion dates don&rsquo;t line up, paying for short bursts of accommodation or two separate moves can be costly. Flexible <a href="/services/storage/short-term-storage/">short-term storage</a> often works out cheaper and far less stressful.</p>
<p>With a little forethought, you can move well and spend wisely. <a href="/get-a-quote/">Request a free quote</a> and we&rsquo;ll help you find the most cost-effective option for your move.</p>""",
  "faqs": [("What&rsquo;s the cheapest day to move house?", "<p>Mid-week, mid-month moves are usually quieter and better value than Fridays, weekends and month-ends.</p>"),
           ("Does decluttering really reduce the cost?", "<p>Yes &mdash; removal pricing is largely based on volume, so moving less directly reduces the time, crew and vehicle needed.</p>"),
           ("Is a man and van cheaper than a full removal?", "<p>For smaller loads, yes. Our <a href=\"/services/man-and-van/\">man and van</a> service starts from £80 and suits flats, students and single items.</p>"),
           ("How do I avoid hidden moving costs?", "<p>Get a clear written quote after a proper survey and compare like for like. We quote with no hidden fees &mdash; see our <a href=\"/pricing/\">pricing</a>.</p>")],
},
{
  "slug": "choosing-a-removal-company", "name": "Choosing a Removal Company",
  "title": "How to Choose a Removal Company | Wolves Removals",
  "meta": "How to choose the right removal company: check insurance, accreditation, reviews and a clear written quote. A practical guide from Wolves Removals Sussex.",
  "lead": "Choosing the right removals company protects your belongings and your peace of mind. Here&rsquo;s what to look for.",
  "body": """<p>If you&rsquo;re packing up your life and moving to a new home, choosing a removals company might not seem like the most important decision &mdash; until something goes wrong. The right company protects your belongings, your timeline and your sanity. Here&rsquo;s how to choose well.</p>
<h2>Check They&rsquo;re Properly Insured</h2>
<p>Insurance is non-negotiable. Ask what cover is included as standard and what optional protection is available for your goods. A reputable mover will be happy to explain. Wolves Removals is <strong>fully insured with liability cover up to £10 million</strong>, with optional full damage insurance for added peace of mind.</p>
<h2>Look for Accreditations</h2>
<p>Accreditations signal recognised standards. We&rsquo;re a <strong>LAPADA member</strong> for antiques and fine-art handling and <strong>Checkatrade-verified</strong>, and we&rsquo;re recommended by leading estate agents including Fine &amp; Country, Justin Lloyd and Mansell McTaggart. These independent endorsements matter.</p>
<h2>Read Genuine Reviews</h2>
<p>Independent reviews tell you how a company really performs. Look on platforms like Google, Checkatrade and Facebook for honest, verified feedback &mdash; you can read ours on our <a href="/reviews/">reviews page</a>. Consistent praise for care, communication and reliability is a good sign.</p>
<h2>Insist on a Clear, Written Quote</h2>
<p>A trustworthy company will offer a proper survey &mdash; video or in person &mdash; and provide a clear written quote with no hidden fees. Be wary of vague phone estimates that balloon on the day. Our quotes are transparent and itemised; see our <a href="/pricing/">pricing guide</a>.</p>
<h2>Ask About Their Team and Equipment</h2>
<p>Experienced, trained staff and a well-maintained fleet make all the difference. Our movers are fully trained, uniformed and DBS-checked, and we run modern, properly equipped vehicles &mdash; so your move is in capable, professional hands.</p>
<h2>Choose a Company That Communicates</h2>
<p>Good communication reduces stress. From your first enquiry to settling in, you should have a clear point of contact who keeps you informed. We assign a dedicated coordinator to every move for exactly this reason.</p>
<p>Take your time, ask questions, and choose a company you trust. If that&rsquo;s us, we&rsquo;d be delighted to help &mdash; <a href="/get-a-quote/">request a free quote</a> today.</p>""",
  "faqs": [("What should I check before hiring a removals company?", "<p>Insurance, accreditations, genuine reviews, a clear written quote, and an experienced, vetted team. We tick all of these.</p>"),
           ("Are you insured and accredited?", "<p>Yes &mdash; fully insured (liability up to £10m), a LAPADA member and Checkatrade-verified.</p>"),
           ("Where can I read your reviews?", "<p>On Google, Checkatrade and Facebook &mdash; see our <a href=\"/reviews/\">reviews page</a> for links.</p>"),
           ("Will I have a single point of contact?", "<p>Yes &mdash; we assign a dedicated move coordinator to keep you informed from first enquiry to moving day.</p>")],
},
{
  "slug": "how-to-lift-objects", "name": "How to Lift Objects Safely",
  "title": "How to Lift Objects Safely When Moving | Wolves Removals",
  "meta": "Avoid injury on moving day with safe lifting techniques: plan the lift, bend your knees, keep loads close, and know when to ask for help. Wolves Removals Sussex.",
  "lead": "Moving day means heavy lifting &mdash; and back injuries are common. Here&rsquo;s how to lift safely (or when to leave it to the professionals).",
  "body": """<p>Every year, people hurt themselves moving house by lifting badly. A strained back can turn moving day into weeks of discomfort. Whether you&rsquo;re doing some of the lifting yourself or simply want to stay safe, here&rsquo;s how to lift properly.</p>
<h2>Plan the Lift First</h2>
<p>Before you pick anything up, think it through. How heavy is it? Where is it going? Is the route clear of obstacles, with doors propped open? If an item is too heavy or awkward for one person, don&rsquo;t risk it &mdash; get help or use equipment.</p>
<h2>Use the Correct Technique</h2>
<p>Stand close to the load with your feet shoulder-width apart. Bend at your knees and hips, not your back, keeping your back straight. Get a firm grip, then lift smoothly by straightening your legs &mdash; let your strong leg muscles do the work, not your spine. Keep the load close to your body throughout.</p>
<h2>Don&rsquo;t Twist or Overreach</h2>
<p>Twisting while carrying a load is a common cause of injury. Turn with your feet, not your waist. Avoid reaching above shoulder height with heavy items, and never carry so much that you can&rsquo;t see where you&rsquo;re going.</p>
<h2>Use the Right Equipment</h2>
<p>Sack trucks, trolleys, moving straps and furniture sliders make heavy items far safer to move. Our team arrives fully equipped with blankets, straps and the right tools &mdash; one reason a professional move is so much safer than going it alone.</p>
<h2>Know When to Call the Professionals</h2>
<p>Some items &mdash; pianos, large wardrobes, safes and white goods &mdash; are genuinely hazardous to move without training and equipment. Our team handles heavy and awkward items every day, including specialist <a href="/services/piano-moving/">piano moving</a>. If in doubt, leave it to us &mdash; it&rsquo;s not worth a serious injury.</p>
<p>Moving is hard work. If you&rsquo;d rather protect your back and let an experienced, fully insured team do the heavy lifting, <a href="/get-a-quote/">request a free quote</a>.</p>""",
  "faqs": [("What&rsquo;s the correct way to lift a heavy box?", "<p>Stand close, feet shoulder-width apart, bend your knees (not your back), grip firmly and lift with your legs, keeping the load close to your body.</p>"),
           ("How do I avoid back injury when moving?", "<p>Plan each lift, never twist while carrying, don&rsquo;t overload yourself, use equipment like trolleys and straps, and get help for heavy items.</p>"),
           ("Should I move a piano myself?", "<p>No &mdash; pianos are heavy and easily damaged. Use our specialist <a href=\"/services/piano-moving/\">piano moving</a> service.</p>"),
           ("Do your movers bring lifting equipment?", "<p>Yes &mdash; our team arrives with blankets, straps, trolleys and the right tools to move heavy items safely.</p>")],
},
{
  "slug": "how-to-prepare-a-washing-machine-or-dishwasher-to-be-moved", "name": "How to Prepare a Washing Machine or Dishwasher to Be Moved",
  "title": "Preparing a Washing Machine for Moving | Wolves Removals",
  "meta": "Step-by-step guide to preparing a washing machine or dishwasher for moving: disconnect, drain, fit transit bolts and secure the door. Wolves Removals Sussex.",
  "lead": "White goods need a little preparation before a move. Here&rsquo;s how to get your washing machine or dishwasher ready safely.",
  "body": """<p>Washing machines and dishwashers are heavy, full of water and easily damaged in transit if they aren&rsquo;t prepared properly. A little preparation the day before protects your appliance and prevents leaks. Here&rsquo;s how to do it.</p>
<h2>Switch Off and Disconnect</h2>
<p>Turn off the power at the socket and unplug the appliance. Turn off the water supply at the valve, then disconnect the inlet hose &mdash; have a towel and bowl ready, as some water will escape. Disconnect the waste/drain hose too.</p>
<h2>Drain Any Remaining Water</h2>
<p>Even after disconnecting, water remains inside. Run a short drain or spin cycle if possible before disconnecting, and check the filter at the bottom of a washing machine &mdash; place a shallow tray underneath and open it to drain residual water. For dishwashers, remove standing water from the base.</p>
<h2>Fit the Transit Bolts (Washing Machines)</h2>
<p>This step is essential. Washing machines have transit bolts that secure the drum during transport. If you removed them when the machine was installed, refit them now &mdash; moving a machine without them can wreck the drum suspension. If you no longer have the bolts, contact the manufacturer; in the meantime, tell your movers so they can take extra care.</p>
<h2>Secure Hoses, Cable and Door</h2>
<p>Coil the hoses and cable and tape them to the back of the appliance so they don&rsquo;t catch or trail. Tape the door closed (or wedge it slightly ajar to prevent mould if there&rsquo;ll be a delay before reconnection &mdash; but secure it for the move itself). Wipe the interior dry.</p>
<h2>Let the Professionals Handle the Heavy Part</h2>
<p>Once prepared, the appliance still needs moving safely &mdash; they&rsquo;re heavy and awkward. Our trained team will transport it carefully as part of your <a href="/services/house-removals/">house removal</a>. Just let us know at the <a href="/get-a-quote/">quote stage</a> so we can plan for it.</p>
<p>A few minutes of preparation saves a flooded floor and a damaged appliance. If you&rsquo;d like a hand with the whole move, <a href="/get-a-quote/">get in touch</a>.</p>""",
  "faqs": [("Do I need transit bolts to move a washing machine?", "<p>Yes &mdash; transit bolts secure the drum and prevent damage to the suspension. Refit them before the move, or tell us if you no longer have them.</p>"),
           ("How do I drain a washing machine before moving?", "<p>Run a short spin, then disconnect the hoses with a towel and tray ready, and drain residual water via the filter at the bottom.</p>"),
           ("Should I empty a dishwasher before moving?", "<p>Yes &mdash; disconnect the water and waste, remove standing water from the base, secure the hoses and tape the door.</p>"),
           ("Will you move my appliances for me?", "<p>Yes &mdash; once prepared, our team moves white goods safely as part of your <a href=\"/services/house-removals/\">removal</a>. Mention them at the quote stage.</p>")],
},
{
  "slug": "five-reasons-to-move-to-west-sussex", "name": "Five Reasons to Move to West Sussex",
  "title": "5 Reasons to Move to West Sussex | Wolves Removals",
  "meta": "Thinking of moving to West Sussex? Five great reasons: stunning coast and countryside, great connections, vibrant towns, culture and a brilliant lifestyle.",
  "lead": "Considering a move to West Sussex? Here are five reasons it&rsquo;s one of the most desirable places to live in the South East.",
  "body": """<p>West Sussex is one of England&rsquo;s most appealing counties &mdash; a blend of beautiful coast, rolling countryside, historic towns and easy access to London. As a Sussex removals company based near <a href="/locations/pulborough-removals/">Pulborough</a>, we help people move here all the time. Here are five reasons West Sussex might be your next home.</p>
<h2>1. Stunning Coast and Countryside</h2>
<p>From the beaches of <a href="/locations/worthing-removals/">Worthing</a>, <a href="/locations/bognor-regis-removals/">Bognor Regis</a> and <a href="/locations/littlehampton-removals/">Littlehampton</a> to the rolling hills of the South Downs National Park, West Sussex offers an enviable natural setting. Whether you love the sea or the countryside, it&rsquo;s all within easy reach.</p>
<h2>2. Great Transport Links</h2>
<p>West Sussex is brilliantly connected. Direct trains reach London in around an hour from towns like <a href="/locations/horsham-removals/">Horsham</a> and Haywards Heath, Gatwick Airport is on the doorstep, and the A23/M23 and A27 make getting around straightforward &mdash; perfect for commuters and travellers alike.</p>
<h2>3. Characterful Towns and Villages</h2>
<p>From the cathedral city of <a href="/locations/chichester-removals/">Chichester</a> to historic <a href="/locations/arundel-removals/">Arundel</a> with its castle, and bustling market towns like Horsham, West Sussex is full of character. There&rsquo;s a real mix of vibrant centres and peaceful villages to suit every lifestyle.</p>
<h2>4. Culture, History and Events</h2>
<p>West Sussex is rich in culture &mdash; Chichester Festival Theatre, Goodwood&rsquo;s racing and motorsport events, Arundel Castle, and festivals throughout the year. There&rsquo;s always something on, and the heritage runs deep.</p>
<h2>5. A Wonderful Place to Raise a Family</h2>
<p>With excellent schools, green space, a strong sense of community and a generally relaxed pace of life, West Sussex is a fantastic place to put down roots. It&rsquo;s no surprise so many families choose to move here.</p>
<p>Thinking of making the move? We know the county inside out and would love to help you settle in. Explore the <a href="/locations/west-sussex-removals/">areas we cover in West Sussex</a> or <a href="/get-a-quote/">request a free quote</a>.</p>""",
  "faqs": [("Is West Sussex a good place to live?", "<p>Yes &mdash; it combines coast, countryside, historic towns, great transport links and a relaxed lifestyle, making it one of the South East&rsquo;s most desirable counties.</p>"),
           ("How far is West Sussex from London?", "<p>Direct trains from towns like Horsham and Haywards Heath reach London in around an hour, and Gatwick Airport is close by.</p>"),
           ("Which West Sussex towns do you cover?", "<p>All of them &mdash; see our <a href=\"/locations/west-sussex-removals/\">West Sussex removals</a> page for the full list.</p>"),
           ("Can you help me move to West Sussex?", "<p>Absolutely &mdash; we move people into the county every week. <a href=\"/get-a-quote/\">Request a free quote</a> to get started.</p>")],
},
{
  "slug": "10-things-to-know-about-moving-to-worthing", "name": "10 Things to Know About Moving to Worthing",
  "title": "10 Things to Know About Moving to Worthing | Wolves Removals",
  "meta": "Moving to Worthing? Ten things to know — the seafront, transport, town centre, schools, parking and lifestyle. Local insight from Wolves Removals.",
  "lead": "Moving to Worthing? Here are ten things worth knowing about this popular West Sussex seaside town.",
  "body": """<p>Worthing has become one of West Sussex&rsquo;s most sought-after places to live &mdash; a classic seaside town with a fresh, modern energy. As a local removals company, we help people move to <a href="/locations/worthing-removals/">Worthing</a> regularly. Here are ten things to know before you go.</p>
<h2>1. The Seafront Is the Star</h2>
<p>Worthing&rsquo;s long pebble beach, Victorian pier and breezy promenade are at the heart of town life &mdash; perfect for walks, swims and watching the sunset.</p>
<h2>2. It&rsquo;s Well Connected</h2>
<p>Direct trains run to London Victoria and along the coast to Brighton and Chichester, and the A27 links you across the county &mdash; handy for commuters.</p>
<h2>3. A Thriving Town Centre</h2>
<p>The centre mixes high-street names with independent shops, cafés and a lively food and drink scene that has grown impressively in recent years.</p>
<h2>4. Plenty of Green Space</h2>
<p>Beyond the beach, Worthing has parks and the South Downs on its doorstep, with Cissbury Ring and Highdown Gardens nearby for walks and views.</p>
<h2>5. A Strong Arts and Culture Scene</h2>
<p>The Connaught Theatre, Worthing Museum and a busy calendar of festivals give the town a genuine cultural buzz.</p>
<h2>6. Schools and Families</h2>
<p>Worthing offers a good range of primary and secondary schools, making it popular with families relocating from busier or pricier areas.</p>
<h2>7. A Range of Property Styles</h2>
<p>From seafront flats and Victorian terraces to modern developments and family homes, there&rsquo;s a wide variety of housing to suit different budgets.</p>
<h2>8. Parking Takes Planning</h2>
<p>Like many seaside towns, parking near the centre and seafront can be restricted. On moving day, it&rsquo;s worth arranging permits in advance &mdash; something our team helps plan for.</p>
<h2>9. A Relaxed Coastal Lifestyle</h2>
<p>Worthing offers the calm of the coast with the convenience of a proper town &mdash; a big part of its growing appeal.</p>
<h2>10. A Friendly Local Mover Helps</h2>
<p>Knowing the town&rsquo;s roads, seafront access and parking makes a real difference on moving day. We move people to and from Worthing all the time &mdash; see our <a href="/locations/worthing-removals/">Worthing removals</a> page.</p>
<p>Ready to make the move? <a href="/get-a-quote/">Request a free quote</a> and let our local team take the strain.</p>""",
  "faqs": [("Is Worthing a good place to live?", "<p>Yes &mdash; it offers a classic seaside lifestyle, a thriving town centre, good transport and a range of housing, which is why it&rsquo;s increasingly popular.</p>"),
           ("How do I get to London from Worthing?", "<p>Direct trains run to London Victoria, with coastal services to Brighton and Chichester and the A27 for road travel.</p>"),
           ("Is parking difficult in Worthing?", "<p>Near the centre and seafront it can be restricted. We help plan permits and access for moving day &mdash; see our <a href=\"/locations/worthing-removals/\">Worthing removals</a> page.</p>"),
           ("Do you cover removals in Worthing?", "<p>Yes &mdash; Worthing is one of our core areas. <a href=\"/get-a-quote/\">Request a free quote</a> for your move.</p>")],
},
]

def _related(cur):
    others = [t for t in TIPS if t["slug"] != cur][:3]
    return [(t["name"], f"/helpful-tips/{t['slug']}/", "<p>Read our practical moving advice.</p>") for t in others]

def build_tip(t):
    pics = E.page_photos(t["slug"], 5)
    _exp = E.load_expansion("tips", t["slug"])
    tip_body = t["body"] + _exp.get("body", "")
    for _h2, _html in _exp.get("sections", []):
        tip_body += f'<h2 class="relative leading-tight text-black">{esc(_h2)}</h2>{_html}'
    tfaqs = list(t["faqs"]) + [tuple(x) for x in _exp.get("faqs", [])]
    faq_html, faq_schema = faq_block(tfaqs, heading=f"{t['name']} &mdash; FAQs", bg="bg-white")
    body = "\n".join([
        hero(t["name"], f"<p>{t['lead']}</p>", pics[0]),
        E.quote_bar(lead="Need a Hand Moving?", rest="Get a Free Quote",
                    subtext="Our trained Sussex team is ready to help — get a free quote."),
        E.media_body(tip_body, t["slug"], used={pics[0][0], pics[4][0]}),
        E.wolves_feature_panel(pics[4], reverse=False, bg="bg-beige"),
        faq_html,
        card_grid(_related(t["slug"]), cols=3, heading="More Helpful Moving Tips", bg="bg-beige"),
        E.photo_strip(pics[1:4], heading="Moving With Wolves Removals",
                      intro="Our trained, fully insured Sussex team in action.", bg="bg-lightgrey"),
        cta_band("Planning a Move?", "Get a free, no-obligation quote from our friendly Sussex team.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-white"),
    ])
    doc = E.render_page(title=t["title"], description=t["meta"], canonical_path=f"/helpful-tips/{t['slug']}/",
        body=body, og_image="images/photos/" + pics[0][0] + ".webp",
        breadcrumb=[("Home", "/"), ("Helpful Tips", "/helpful-tips/"), (t["name"], f"/helpful-tips/{t['slug']}/")],
        extra_schema=[faq_schema], active="about")
    return E.write(f"helpful-tips/{t['slug']}/index.html", doc)

def build_hub():
    cards = [(t["name"], f"/helpful-tips/{t['slug']}/", f"<p>{esc(t['lead'])}</p>") for t in TIPS]
    # pad to multiple of 3 to avoid orphan (7 -> add nothing, show 6+1? use 2-col fallback). 7 cards -> 3-col leaves 1 orphan.
    intro = ('<h2 class="relative leading-tight text-black">Helpful Moving Tips &amp; Advice</h2>'
             '<p>Moving home is easier with a little know-how. Our guides share practical advice from years of helping '
             'people move across Sussex &mdash; from packing and lifting safely to choosing a removals company and '
             'settling into a new area. Browse our tips below, and <a href="/get-a-quote/">get in touch</a> whenever '
             'you&rsquo;re ready to plan your move.</p>'
             '<p>Whether you&rsquo;re a first-time mover or an old hand, a little preparation goes a long way. Our guides '
             'cover the practical questions people ask us most: how to pack efficiently, how to lift heavy items without '
             'hurting yourself, how to keep costs down, how to prepare appliances like washing machines, and what to '
             'look for when <a href="/helpful-tips/choosing-a-removal-company/">choosing a removals company</a>. We also '
             'share local insight for people moving to the area, including '
             '<a href="/helpful-tips/five-reasons-to-move-to-west-sussex/">reasons to move to West Sussex</a> and what '
             'to know about <a href="/helpful-tips/10-things-to-know-about-moving-to-worthing/">moving to Worthing</a>.</p>'
             '<p>Of course, the simplest way to a stress-free move is to let an experienced, fully insured team handle '
             'it. We&rsquo;re a family-run Sussex removals company, LAPADA-accredited and Checkatrade-verified, and we '
             'cover the whole of <a href="/locations/">Sussex, Surrey, Hampshire and beyond</a>. Read on for our advice, '
             'and reach out whenever you need a hand.</p>')
    faqs = [
        ("How far in advance should I start planning my move?",
         "<p>Ideally four to six weeks ahead. That gives you time to declutter, gather packing materials, book your removals team and notify utilities and services &mdash; all of which make moving day far less stressful.</p>"),
        ("What&rsquo;s the best way to pack fragile items?",
         "<p>Wrap each item individually in bubble wrap or packing paper, use sturdy boxes, fill any gaps so nothing shifts, and clearly label boxes &lsquo;fragile&rsquo;. We also offer a <a href=\"/services/full-packing-service/\">full packing service</a> if you&rsquo;d rather leave it to the experts.</p>"),
        ("Should I pack myself or use a packing service?",
         "<p>Both work well &mdash; packing yourself saves money, while a professional packing service saves time and protects fragile and valuable items. Many customers pack the everyday items and let us handle the delicate ones.</p>"),
        ("How can I keep my moving costs down?",
         "<p>Declutter before you move, be flexible on dates, pack what you can yourself, and get a clear written quote up front so there are no surprises. <a href=\"/get-a-quote/\">Request a free quote</a> to compare.</p>"),
        ("Do I need to be home for a removals survey?",
         "<p>Not necessarily &mdash; as well as in-home surveys we offer free video surveys, so we can assess your move and quote without you taking time off work. <a href=\"/contact-us/\">Contact us</a> to arrange one.</p>"),
    ]
    body = "\n".join([
        hero("Helpful Moving Tips", "<p>Practical advice to make your move smoother, safer and less stressful.</p>"),
        E.quote_bar(lead="Moving Soon?", rest="Get a Free Quote",
                    subtext="Let Wolves Removals take the strain — request a free quote today."),
        E.media_body(intro, "tips-hub"),
        card_grid(cards, cols=3, heading="Our Moving Guides", bg="bg-lightgrey"),
        faq_block(faqs, heading="Moving Tips &mdash; Your Questions Answered", bg="bg-white")[0],
        cta_band("Ready to Move?", "Let our experienced, fully insured team take the strain.",
                 "Get a Free Quote", "/get-a-quote/", bg="bg-lightgrey"),
    ])
    doc = E.render_page(title="Helpful Moving Tips & Advice | Wolves Removals Sussex",
        description="Practical moving tips from Wolves Removals: packing, safe lifting, saving money, choosing a removals company and moving to West Sussex. Expert advice from Sussex movers.",
        canonical_path="/helpful-tips/", body=body, og_image=HERO,
        extra_schema=[faq_block(faqs, heading="x")[1]],
        breadcrumb=[("Home", "/"), ("Helpful Tips", "/helpful-tips/")], active="about")
    return E.write("helpful-tips/index.html", doc)

def build():
    build_hub()
    for t in TIPS:
        build_tip(t)
    print(f"built helpful-tips hub + {len(TIPS)} articles")

if __name__ == "__main__":
    build()
