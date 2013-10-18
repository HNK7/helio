from django.db.models import Q
from tourney.models import *
from tourney.views import *

registered_player = [
"Amanda Butler",
"Amber Huddleston",
"Anela Tucay-Beaman",
"Angela Brigugulio",
"Anna Secka",
"Anthony Mock",
"Anthony Najera",
"Arthur Perez",
"Barlow Jayson",
"Bill James",
"Bob Bretz",
"Bob Brockman",
"Brad Eckenrode",
"Brad Haley",
"Brett Valentine",
"Brett Wakino",
"Brian Castilho",
"Brian Dunagan",
"Brian Jackson",
"Bruce Lawson",
"Bruce Riley",
"Bryson Gibson",
"Bubba Huddy",
"Carl Polefko",
"Carol Bretz",
"Cassie Salinas",
"Cathy Breckenfelder",
"Cathy Erwin",
"Charles Pankow",
"Chris Pestana",
"Clarence Pope",
"Cody Stocke",
"Colin Rath",
"Courtney Kocher",
"Craig Hittinger",
"Craig Ishibashi",
"Dana Gardner",
"Dana Williams",
"Daniel Daley",
"Daniel Daugherty",
"Daniel Denkovich",
"Daniel Dunagan",
"Daniel Vinesky",
"Dario Meza",
"Darla Glass-Hill",
"Dave Hild",
"David Caputo",
"David Wilderman",
"Davina Mancao",
"Dee Adams",
"Delta Newton",
"Denise Davis",
"Dick Cortez",
"Donna Daley",
"Donna James",
"Doug Siperly",
"Ed Shoepe",
"Eddie Espinoza",
"Eddie Nakamoto",
"Elliott Garma",
"Elton Munoz",
"Eric Coomes",
"Eric Gibson",
"Eric Gillespie",
"Eric Housden",
"Eric O'Con",
"Erin Maloney",
"Ernie Sudberry",
"Estevon Flores",
"Ethan Malicki",
"Eva Gil",
"Francine Ginder",
"Frank DeMarco",
"Frank Perez",
"Frank Sadlo",
"Gary Erwin",
"Gary Laino",
"Gilberto Mojica",
"Gina Robertson",
"Gloria Gutierrez",
"Gordon Dixon",
"Gordon Germain",
"Greg Lumsdaine",
"Gretel Flores",
"Grzesik Trish",
"Guillermo Mejia Jr.",
"Hank Hogan",
"Harms Erin",
"Harry DeLandro",
"Heath Hudson",
"Ikaika Betonio",
"Jacob Hicks",
"Jaeger Paul",
"James Goodwin",
"James Hopkins",
"Jamie Luke",
"Jay O'Con",
"Jeanne Messer",
"Jeff Cox",
"Jeff Johnson",
"Jeff Meduna",
"Jennifer Garma",
"Jeremiah Barba",
"Jermaine Jones",
"Jerry Kormick",
"Jesse Mendoza",
"Jim Luft",
"Jody Mayer",
"Joe Hedrick",
"John Cherry",
"John Kuczynski",
"John Ortega",
"John Sutherland",
"Juan Carlos	Martinez",
"Julio Espinoza Jr.",
"Julio Espinoza Sr.",
"Justin Boebel",
"Justin Kulsa",
"Katie Hild",
"Keith Sielaff",
"Kelli Wise",
"Kenneth Mercier",
"Kenny Wright",
"Kevin Tokuhara",
"Kevin Vandenberg",
"Kix Alcala",
"Kuhio Kapolulu",
"Lisa Mullins",
"Lisa Yee",
"Lupe Flores Jr",
"Lynda Juhr",
"Maria Diaz",
"Mario Lugo",
"Mark Fair",
"Mark Selgrath",
"Mary Hopkins",
"Matt Lucas",
"Matthew Mohawk",
"Maurice Fitzpatrick",
"Melanie Mofsie",
"Melinda Gomez",
"Melissa Pryor",
"Melissa Tittle",
"Melvin Mofsie",
"Micah Ono",
"Michael Roman",
"Michael Salinas",
"Michael Salinas Jr",
"Michael Wingfield",
"Michelle Vandenberg",
"Mike Durans",
"Mike Haney",
"Mike Joseph",
"Mike Kaminski",
"Mike Miranda",
"Mike Nicholls",
"Mike Sanko",
"Mitch Hedrick",
"Moses Gonzales",
"Nick McMullen",
"Nick Rivera",
"Nick Siperly",
"Niels Juhr",
"Nikki Hedrick",
"Pat Jones",
"Patrick Howard",
"Paul Preston",
"Paul Woodhouse",
"Paula Murphy",
"Pete Linaris",
"Rachel Cloud",
"Randy Pinacate",
"Randy Rusch",
"Rashad Sandridge",
"Ray Arreola",
"Ray Gerbert",
"Richard Kim",
"Richard Wescott",
"Rick Breckenfelder",
"Rick Kerska",
"Rits Michiue",
"Robert Berry",
"Robert Sowinski",
"Robert Stone",
"Rock Owens",
"Rodney Pryor",
"Rodney Watai",
"Ron Colvard",
"Ron Eckerson",
"Ron Matsushita",
"Ryan Moore",
"Ryan Sebastian",
"Sean Downs",
"Sean Flynn",
"Sean Lochridge",
"Shad Newton",
"Shannon Rae Kehoe",
"Sheila Dill",
"Stephan Doncevic",
"Sterling Oili",
"Suzanne Lawson",
"Tammy Espinoza",
"Tash Oda",
"Teresa Arreola",
"Thad Uraine",
"Theodore Mahiai",
"Theresa Karam",
"Timothy Goodwin",
"Toby Romero",
"Todd Allebach",
"Tom Williamson",
"Tommy Hicks",
"Tracey Hines",
"Vaughn Larry",
"Vincent Fong",
"Wendi Dodson",]


# for p in pre_imported:
# 	fname = "%s %s" %(p.first_name, p.last_name)
# 	if not fname in registered_player:
# 		print fname

class Vegas:

	def copy_live_to_entry(self, entries):
		"""
		copy live casual stats to entry stats
		"""
		for e in entries:
			# if e.mpr_rank == 0 or e.ppd_rank == 0:
				c_stat = e.player.casual_stat()
				print e.player, '\t\tcasual: ', c_stat['MPR'], c_stat['PPD'], '\treplaces entry: ', e.mpr_event, e.ppd_event
				e.mpr_event = c_stat['MPR'] if c_stat['MPR'] > 0 else e.mpr_event
				e.ppd_event = c_stat['PPD'] if c_stat['PPD'] > 0 else e.ppd_event

	def copy_entry_to_live(self, entreis):
		"""
		make entry stats to live
		"""

		for e in entries:
			update_stat(e.mpr_event, e.ppd_event, e.player.card.rfid)
			print 'e.player stat updted: %s %s' % e.mpr_event, e.ppd_event

# for p in pre_imported:
# 	fname = '%s %s' % (p.first_name, p.last_name)
# 	p_list.append(fname)
# e_list = [str(e.player.full_name) for e in vegas.entry_set.all()]

# print 'justin - PreRegVegas:', list(set(registered_player) - set(p_list))
# print 'Entry - PreRegVegas:', list(set(e_list) - set(p_list))
# print 'justin - Entry:', list(set(registered_player) - set(e_list))


# walkins = [e.player for e in w_entries]
# for w in walkins:
# 	try:
# 		PreRegVegas.objects.get(first_name=w.first_name, last_name=w.last_name)
# 		print w
# 	except:
# 		pass

