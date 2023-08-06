import unittest

from upyls import MultiIniParser


class TestMultiIniParser(unittest.TestCase):
    def test_simple_ini_config_colon_delimiter(self):
        ini_config = """option1: first option
[section1]
option2: second option
[section2]
option3: third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        self.assertEqual("first option", parser[None]["option1"][0])
        self.assertEqual("second option", parser["section1"][0]["option2"][0])
        self.assertEqual("third option", parser["section2"][0]["option3"][0])

    def test_simple_ini_config_equals_delimiter(self):
        ini_config = """option1= first option
[section1]
option2= second option
[section2]
option3= third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        self.assertEqual("first option", parser[None]["option1"][0])
        self.assertEqual("second option", parser["section1"][0]["option2"][0])
        self.assertEqual("third option", parser["section2"][0]["option3"][0])

    def test_multiple_section_name_colon_delimiter(self):
        ini_config = """option1: first option
[section]
option2: second option
[section]
option3: third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        self.assertEqual("first option", parser[None]["option1"][0])
        self.assertEqual("second option", parser["section"][0]["option2"][0])
        self.assertEqual("third option", parser["section"][1]["option3"][0])

    def test_multiple_option_name_colon_delimiter(self):
        ini_config = """option1: first option
[section]
option2: second option
option2: second second option
[section]
option3: third option
option3: second third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        self.assertEqual("first option", parser[None]["option1"][0])
        self.assertEqual("second option", parser["section"][0]["option2"][0])
        self.assertEqual("second second option", parser["section"][0]["option2"][1])
        self.assertEqual("third option", parser["section"][1]["option3"][0])
        self.assertEqual("second third option", parser["section"][1]["option3"][1])

    def test_get(self):
        ini_config = """option1: first option
[section]
option2: second option
option2: second second option
[section]
option3: third option
option3: second third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        self.assertEqual("first option", parser.get(None, "option1")[0].value)
        self.assertEqual("second option", parser.get("section", "option2")[0].value)
        self.assertEqual("second second option", parser.get("section", "option2")[1].value)
        self.assertEqual("third option", parser.get("section", "option3")[0].value)
        self.assertEqual("second third option", parser.get("section", "option3")[1].value)



    def test_get_sections_by_name(self):
        ini_config = """option1: first option
[section]
option2: second option
option2: second second option
[section]
option3: third option
option3: second third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        sections = parser.get_sections_by_name("section")
        self.assertEqual(2, len(sections))
        self.assertEqual(2, len(sections[0].options))
        self.assertEqual(2, len(sections[1].options))
        self.assertEqual("second option", sections[0].options[0].value)
        self.assertEqual("second second option", sections[0].options[1].value)
        self.assertEqual("third option", sections[1].options[0].value)
        self.assertEqual("second third option", sections[1].options[1].value)

    def test_get_options_by_name_options_in_different_sections(self):
        ini_config = """option1: first option
[section]
option2: second option
option2: second second option
[section]
option3: third option
option3: second third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        options2 = parser.get_options_by_name("option2")
        self.assertEqual("second option", options2[0].value)
        self.assertEqual("second second option", options2[1].value)
        options3 = parser.get_options_by_name("option3")
        self.assertEqual("third option", options3[0].value)
        self.assertEqual("second third option", options3[1].value)

    def test_get_options_by_name_options_in_same_sections(self):
        ini_config = """option1: first option
[section]
option2: second option
option3: third option
[section]
option2: second second option
option3: second third option
"""
        parser = MultiIniParser()
        parser.read(ini_config)
        options2 = parser.get_options_by_name("option2")
        self.assertEqual("second option", options2[0].value)
        self.assertEqual("second second option", options2[1].value)
        options3 = parser.get_options_by_name("option3")
        self.assertEqual("third option", options3[0].value)
        self.assertEqual("second third option", options3[1].value)

if __name__ == '__main__':
    unittest.main()
