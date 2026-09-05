import unittest

from melakat_desktop.parameters import CORE_SCHEMA


class ParameterSchemaTests(unittest.TestCase):
    def test_defaults_are_valid(self) -> None:
        values = CORE_SCHEMA.validate(CORE_SCHEMA.defaults())
        self.assertEqual(values["population.initial_size"], 12)

    def test_schema_can_grow_without_ui_changes(self) -> None:
        self.assertGreaterEqual(len(CORE_SCHEMA.specs), 20)

    def test_invalid_value_is_rejected(self) -> None:
        values = CORE_SCHEMA.defaults()
        values["mutation.substitution_rate"] = 2.0
        with self.assertRaises(ValueError):
            CORE_SCHEMA.validate(values)


if __name__ == "__main__":
    unittest.main()
