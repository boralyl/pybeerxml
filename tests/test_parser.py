# -*- coding: utf-8 -*-
import os
from math import floor
from xml.etree.ElementTree import Element, SubElement

from pybeerxml.parser import Parser, Recipe
from pybeerxml.hop import Hop
from pybeerxml.equipment import Equipment
from pybeerxml.utils import to_lower

from pybeerxml.mash import Mash

RECIPE_PATH = os.path.join(os.path.dirname(__file__), "Simcoe IPA.xml")
RECIPE_PATH_2 = os.path.join(os.path.dirname(__file__), "Oatmeal Stout.xml")
RECIPE_PATH_3 = os.path.join(os.path.dirname(__file__), "CoffeeStout.xml")


def test_parse_recipe_1_from_file():

    recipe_parser = Parser()
    recipes = recipe_parser.parse(RECIPE_PATH)
    assert_simcoe_ipa_recipe(recipes)


def test_parse_recipe_1_from_string():

    xml_data = open(RECIPE_PATH, "r").read()
    recipe_parser = Parser()
    recipes = recipe_parser.parse_from_string(xml_data)
    assert_simcoe_ipa_recipe(recipes)


def assert_simcoe_ipa_recipe(recipes):
    assert len(recipes) > 0, "should have at least one recipe"

    recipe = recipes[0]
    assert isinstance(recipe, Recipe), "should be of type Recipe"

    assert len(recipe.hops) == 3, "should have the correct amount of hops"
    assert len(recipe.yeasts) == 1, "should have the correct amount of yeasts"
    assert (
        len(recipe.fermentables) == 2
    ), "should have the correct amount of fermentables"

    # should have mashing steps
    assert len(recipe.mash.steps) == 4
    assert recipe.mash.steps[0].name == "Dough In"
    assert recipe.mash.steps[0].version == 1
    assert recipe.mash.steps[0].type == "Infusion"
    assert recipe.mash.steps[0].step_temp == 102
    assert recipe.mash.steps[0].step_time == 20

    # should have the original recipe properties
    assert round(recipe.og, 4) == 1.0756
    assert round(recipe.og_plato, 4) == 18.3327
    assert round(recipe.fg, 4) == 1.0106
    assert round(recipe.fg_plato, 4) == 2.7119
    assert floor(recipe.ibu) == 64

    # should fall back to the calculated value for missing properties
    assert round(recipe.abv, 2) == 3.84
    assert round(recipe.color, 2) == 6.27

    # should have the correctly calculated properties
    assert round(recipe.og_calculated, 4) == 1.0338
    assert round(recipe.og_calculated_plato, 4) == 8.4815
    assert round(recipe.fg_calculated, 4) == 1.0047
    assert round(recipe.fg_calculated_plato, 4) == 1.2156
    assert round(recipe.ibu_calculated, 2) == 99.85
    assert round(recipe.abv_calculated, 2) == 3.84
    assert round(recipe.color_calculated, 2) == 6.27

    # should have the correct recipe metadata
    assert recipe.name == "Simcoe IPA"
    assert recipe.brewer == "Tom Herold"
    assert recipe.efficiency == 76.0
    assert recipe.batch_size == 14.9902306488
    assert recipe.boil_time == 30.0

    assert recipe.style.name == "American IPA", "should have the correct style metadata"


def test_parse_recipe_2_from_file():

    recipe_parser = Parser()
    recipes = recipe_parser.parse(RECIPE_PATH_2)
    assert_oatmeal_stout_recipe(recipes)


def test_parse_recipe_2_from_string():

    xml_data = open(RECIPE_PATH_2, "r").read()
    recipe_parser = Parser()
    recipes = recipe_parser.parse_from_string(xml_data)
    assert_oatmeal_stout_recipe(recipes)


def assert_oatmeal_stout_recipe(recipes):

    assert len(recipes) > 0, "should have at least one recipe"

    recipe = recipes[0]
    assert isinstance(recipe, Recipe), "should be of type Recipe"

    assert len(recipe.hops) == 1, "should have the correct amount of hops"
    assert len(recipe.yeasts) == 1, "should have the correct amount of yeasts"
    assert (
        len(recipe.fermentables) == 5
    ), "should have the correct amount of fermentables"

    assert len(recipe.mash.steps) == 2, "should have 2 mashing steps"
    assert recipe.mash.steps[0].name == "Mash step"
    assert recipe.mash.steps[0].step_time == 60
    assert recipe.mash.steps[0].step_temp == 68

    # should fall back to calculated values for missing properties
    assert (
        round(recipe.og, 4) == 1.0556
    ), "should have the correctly calculated og property"
    assert (
        round(recipe.og_plato, 4) == 13.7108
    ), "should have the correctly calculated og_plato property in Plato"
    assert (
        round(recipe.fg, 4) == 1.0139
    ), "should have the correctly calculated fg property"
    assert (
        round(recipe.fg_plato, 4) == 3.5467
    ), "should have the correctly calculated fg_plato property in Plato"
    assert round(recipe.ibu, 2) == 32.22
    assert round(recipe.abv, 2) == 5.47

    # should have mashing base information
    assert isinstance(recipe.mash, Mash)
    assert recipe.mash.name == "Mash for Oatmeal Stout no. 1"
    assert recipe.mash.grain_temp == "unknown"

    # should have mashing steps
    assert len(recipe.mash.steps) == 2
    assert recipe.mash.steps[0].name == "Mash step"
    assert recipe.mash.steps[0].version == 1
    assert recipe.mash.steps[0].type == "Temperature"
    assert recipe.mash.steps[0].step_time == 60
    assert recipe.mash.steps[0].step_temp == 68

    # should have the same calculated properties
    assert round(recipe.og_calculated, 4) == 1.0556
    assert round(recipe.og_calculated_plato, 4) == 13.7108
    assert round(recipe.fg_calculated, 4) == 1.0139
    assert round(recipe.fg_calculated_plato, 4) == 3.5467
    assert round(recipe.ibu_calculated, 2) == 32.22
    assert round(recipe.abv_calculated, 2) == 5.47

    # should have the correct recipe metadata
    assert recipe.name == "Oatmeal Stout no. 1"
    assert recipe.brewer == "Niels Kjøller"
    assert recipe.efficiency == 75.0
    assert recipe.batch_size == 25

    assert (
        recipe.style.name == "Oatmeal Stout"
    ), "should have the correct style metadata"

    assert len(recipe.miscs) == 1, "should have misc ingredients"
    assert recipe.miscs[0].name == "Protafloc"
    assert recipe.miscs[0].use == "Boil"
    assert recipe.miscs[0].use_for is None
    assert recipe.miscs[0].amount == 0.0016
    assert recipe.miscs[0].amount_is_weight  # True
    assert recipe.miscs[0].time == 15
    assert recipe.miscs[0].notes == "Half a tablet @ 15 minutes"


def test_parse_recipe_3_from_file():

    recipe_parser = Parser()
    recipes = recipe_parser.parse(RECIPE_PATH_3)
    assert_coffee_stout_recipe(recipes)


def test_parse_recipe_3_from_string():

    xml_data = open(RECIPE_PATH_3, "r").read()
    recipe_parser = Parser()
    recipes = recipe_parser.parse_from_string(xml_data)
    assert_coffee_stout_recipe(recipes)


# pylint: disable=too-many-statements
def assert_coffee_stout_recipe(recipes):

    assert len(recipes) > 0, "should have at least one recipe"

    recipe = recipes[0]
    assert isinstance(recipe, Recipe), "should be of type Recipe"

    assert len(recipe.hops) == 2, "should have the correct amount of hops"
    assert len(recipe.yeasts) == 1, "should have the correct amount of yeasts"
    assert (
        len(recipe.fermentables) == 4
    ), "should have the correct amount of fermentables"

    assert len(recipe.mash.steps) == 2, "should have two mashing steps"
    assert recipe.mash.steps[0].name == "Conversion"
    assert recipe.mash.steps[0].step_time == 60
    assert recipe.mash.steps[0].step_temp == 66.66666667

    # should have mashing base information
    assert isinstance(recipe.mash, Mash)
    assert recipe.mash.name == "Single Step"
    assert recipe.mash.grain_temp == 20.0
    assert recipe.mash.sparge_temp == 74.0
    assert recipe.mash.ph == 7
    assert recipe.mash.tun_temp == 21.0
    assert recipe.mash.tun_weight == 4.082
    assert recipe.mash.tun_specific_heat == 0.3
    assert recipe.mash.equip_adjust

    # should have mashing steps
    assert len(recipe.mash.steps) == 2
    assert recipe.mash.steps[0].name == "Conversion"
    assert recipe.mash.steps[0].step_time == 60
    assert recipe.mash.steps[0].step_temp == 66.66666667

    # should have the original recipe properties
    assert round(recipe.og, 4) == 1.0489
    assert round(recipe.og_plato, 4) == 12.1176
    assert round(recipe.fg, 4) == 1.0151
    assert round(recipe.fg_plato, 4) == 3.8613
    assert round(recipe.ibu, 2) == 35
    assert round(recipe.abv, 2) == 5.76
    assert round(recipe.color, 2) == 37

    # should have the correctly calculated properties
    assert round(recipe.og_calculated, 4) == 1.0594
    assert round(recipe.og_calculated_plato, 4) == 14.6092
    assert round(recipe.fg_calculated, 4) == 1.0184
    assert round(recipe.fg_calculated_plato, 4) == 4.684
    assert round(recipe.ibu_calculated, 2) == 25.97
    assert round(recipe.abv_calculated, 2) == 5.35
    assert round(recipe.color_calculated, 2) == 35.01

    # general recipe metadata
    assert recipe.name == "Coffee Stout"
    assert recipe.brewer == "https://github.com/jwjulien"
    assert recipe.efficiency == 70.0
    assert recipe.batch_size == 20.82
    assert recipe.version == 1
    assert recipe.type == "All Grain"
    assert recipe.asst_brewer == "Brewtarget: free beer software"
    assert recipe.boil_size == 25.552
    assert recipe.notes == "Recipe Notes"
    assert recipe.taste_notes == "Taste Notes"
    assert recipe.taste_rating == 42
    assert recipe.fermentation_stages == 1
    assert recipe.date == "3 Dec 04"
    assert recipe.carbonation == 2.1
    assert not recipe.forced_carbonation
    assert recipe.priming_sugar_name == "Honey"
    assert recipe.carbonation_temp == 20.0
    assert recipe.priming_sugar_equiv == 1.1
    assert recipe.keg_priming_factor == 1.2
    assert recipe.est_og == 1.049
    assert recipe.est_fg == 1.015
    assert recipe.est_color == 3.1
    assert recipe.ibu_method == "Tinseth"
    assert recipe.est_abv == 6.23
    assert recipe.actual_efficiency == 65.1
    assert recipe.calories == "180 Cal/pint"
    assert recipe.carbonation_used == "50g corn sugar"

    assert recipe.style.name == "Dry Stout", "should have the correct style metadata"

    assert len(recipe.miscs) == 1, "should have one misc ingredient"
    assert recipe.miscs[0].name == "Coffee, Dark Roast"
    assert recipe.miscs[0].use == "Boil"
    assert recipe.miscs[0].use_for == "Adding coffee notes."
    assert recipe.miscs[0].amount == 0.11339809
    assert recipe.miscs[0].amount_is_weight  # True
    assert recipe.miscs[0].time == 0
    assert (
        recipe.miscs[0].notes
        == "Use a coarse grind, add at flameout, steep 20 minutes."
    )

    # should have equipments
    assert isinstance(recipe.equipment, Equipment)
    assert recipe.equipment.name == "5.5 gal - All Grain - 10 gal Igloo Cooler"
    assert recipe.equipment.version == 1
    assert recipe.equipment.boil_size == 25.552
    assert recipe.equipment.batch_size == 20.82
    assert recipe.equipment.tun_volume == 37.854
    assert recipe.equipment.tun_weight == 4.082
    assert recipe.equipment.tun_specific_heat == 0.3
    assert recipe.equipment.top_up_water == 0.1
    assert recipe.equipment.trub_chiller_loss == 1.893
    assert recipe.equipment.evap_rate == 13.63592699
    assert recipe.equipment.boil_time == 60.0
    assert recipe.equipment.calc_boil_volume  # True
    assert recipe.equipment.lauter_deadspace == 0.2
    assert recipe.equipment.top_up_kettle == 0.4
    assert recipe.equipment.hop_utilization == 100.0
    assert recipe.equipment.notes == "Equipment notes"

    assert recipe.yeasts[0].name == "Wyeast - London ESB Ale"
    assert recipe.yeasts[0].version == 1
    assert recipe.yeasts[0].type == "Ale"
    assert recipe.yeasts[0].form == "Liquid"
    assert recipe.yeasts[0].amount == 0.125
    assert not recipe.yeasts[0].amount_is_weight
    assert recipe.yeasts[0].laboratory == "Wyeast Labs"
    assert recipe.yeasts[0].product_id == 1968
    assert recipe.yeasts[0].min_temperature == 18
    assert recipe.yeasts[0].max_temperature == 22
    assert recipe.yeasts[0].flocculation == "Very High"
    assert recipe.yeasts[0].attenuation == 69.0
    assert recipe.yeasts[0].notes.startswith("This extremely flocculent yeast produces")
    assert recipe.yeasts[0].best_for.startswith("Ordinary/Special Bitters, ESB")
    assert recipe.yeasts[0].times_cultured == 1
    assert recipe.yeasts[0].max_reuse == 0
    assert not recipe.yeasts[0].add_to_secondary


def test_node_to_object():
    "test XML node parsing to Python object"

    node = Element("hop")
    SubElement(node, "name").text = "Simcoe"
    SubElement(node, "alpha").text = 13
    SubElement(node, "amount").text = 0.5
    SubElement(node, "use").text = "boil"
    SubElement(node, "time").text = 30

    test_hop = Hop()

    recipe_parser = Parser()
    recipe_parser.nodes_to_object(node, test_hop)

    assert test_hop.name == "Simcoe"
    assert test_hop.alpha == 13
    assert test_hop.amount == 0.5
    assert test_hop.use == "boil"
    assert test_hop.time == 30


def test_to_lower():

    assert to_lower("MASH") == "mash"
    assert to_lower("") == ""
    assert to_lower(10) == ""
    assert to_lower(None) == ""
