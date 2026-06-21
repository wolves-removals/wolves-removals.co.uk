# -*- coding: utf-8 -*-
"""Location data model for Wolves Removals.
Each town: (url_slug, display_name, county). County hubs handled separately.
'nearby' is derived (same county) by the renderer for internal cross-linking.
Slugs match the live URLs exactly so nothing 301s.
"""

# (slug, display name, county)
TOWNS = [
    ("angmering-removals", "Angmering", "West Sussex"),
    ("arundel-removals", "Arundel", "West Sussex"),
    ("barnham-removals", "Barnham", "West Sussex"),
    ("billingshurst-removals", "Billingshurst", "West Sussex"),
    ("bognor-regis-removals", "Bognor Regis", "West Sussex"),
    ("burgess-hill-removals", "Burgess Hill", "West Sussex"),
    ("chichester-removals", "Chichester", "West Sussex"),
    ("cowfold-removals", "Cowfold", "West Sussex"),
    ("crawley-removals", "Crawley", "West Sussex"),
    ("east-preston-removals", "East Preston", "West Sussex"),
    ("fittleworth-removals", "Fittleworth", "West Sussex"),
    ("goring-by-sea-removals", "Goring-by-Sea", "West Sussex"),
    ("handcross-removals", "Handcross", "West Sussex"),
    ("hassocks-removals", "Hassocks", "West Sussex"),
    ("haywards-heath-removals", "Haywards Heath", "West Sussex"),
    ("henfield-removals", "Henfield", "West Sussex"),
    ("hickstead-removals", "Hickstead", "West Sussex"),
    ("horsham-removals", "Horsham", "West Sussex"),
    ("hurstpierpoint-removals", "Hurstpierpoint", "West Sussex"),
    ("lancing-removals", "Lancing", "West Sussex"),
    ("littlehampton-removals", "Littlehampton", "West Sussex"),
    ("loxwood-removals", "Loxwood", "West Sussex"),
    ("midhurst-removals", "Midhurst", "West Sussex"),
    ("pagham-removals", "Pagham", "West Sussex"),
    ("partridge-green-removals", "Partridge Green", "West Sussex"),
    ("petworth-removals", "Petworth", "West Sussex"),
    ("pulborough-removals", "Pulborough", "West Sussex"),
    ("rustington-removals", "Rustington", "West Sussex"),
    ("selsey-removals", "Selsey", "West Sussex"),
    ("shipley-removals", "Shipley", "West Sussex"),
    ("shoreham-removals", "Shoreham-by-Sea", "West Sussex"),
    ("southwater-removals", "Southwater", "West Sussex"),
    ("southwick-removals", "Southwick", "West Sussex"),
    ("steyning-removals", "Steyning", "West Sussex"),
    ("storrington-removals", "Storrington", "West Sussex"),
    ("thakeham-removals", "Thakeham", "West Sussex"),
    ("upper-beeding-removals", "Upper Beeding", "West Sussex"),
    ("worthing-removals", "Worthing", "West Sussex"),
    # East Sussex
    ("brighton-removals", "Brighton", "East Sussex"),
    ("eastbourne-removals", "Eastbourne", "East Sussex"),
    ("crowborough-removals", "Crowborough", "East Sussex"),
    ("ditchling-removals", "Ditchling", "East Sussex"),
    ("falmer-removals", "Falmer", "East Sussex"),
    ("hailsham-removals", "Hailsham", "East Sussex"),
    ("hastings-removals", "Hastings", "East Sussex"),
    ("heathfield-removals", "Heathfield", "East Sussex"),
    ("hove-removals", "Hove", "East Sussex"),
    ("lewes-removals", "Lewes", "East Sussex"),
    ("newhaven-removals", "Newhaven", "East Sussex"),
    ("north-chailey-removals", "North Chailey", "East Sussex"),
    ("peacehaven-removals", "Peacehaven", "East Sussex"),
    ("polegate-removals", "Polegate", "East Sussex"),
    ("rottingdean-removals", "Rottingdean", "East Sussex"),
    ("saltdean-removals", "Saltdean", "East Sussex"),
    ("seaford-removals", "Seaford", "East Sussex"),
    ("uckfield-removals", "Uckfield", "East Sussex"),
    # Surrey
    ("dorking-removals", "Dorking", "Surrey"),
    ("guildford-removals", "Guildford", "Surrey"),
    ("horley-removals", "Horley", "Surrey"),
    ("redhill-removals", "Redhill", "Surrey"),
    ("reigate-removals", "Reigate", "Surrey"),
    ("removals-cranleigh", "Cranleigh", "Surrey"),
    # Hampshire
    ("petersfield-removals", "Petersfield", "Hampshire"),
    # Kent
    ("tunbridge-wells-removals", "Tunbridge Wells", "Kent"),
]

# County hub pages (slug, county-name used to filter towns)
HUBS = [
    ("sussex-removals", "Sussex", ("West Sussex", "East Sussex")),
    ("west-sussex-removals", "West Sussex", ("West Sussex",)),
    ("east-sussex-removals", "East Sussex", ("East Sussex",)),
    ("surrey-removals", "Surrey", ("Surrey",)),
    ("hampshire-removals", "Hampshire", ("Hampshire",)),
]

def by_county(county):
    return [t for t in TOWNS if t[2] == county]

def nearby(slug, limit=6):
    """Other towns in the same county, for internal cross-linking."""
    me = next((t for t in TOWNS if t[0] == slug), None)
    if not me:
        return []
    same = [t for t in TOWNS if t[2] == me[2] and t[0] != slug]
    # deterministic spread: start near this town's index
    idx = TOWNS.index(me)
    same.sort(key=lambda t: abs(TOWNS.index(t) - idx))
    return same[:limit]
