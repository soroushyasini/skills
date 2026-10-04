from pathlib import Path
import tempfile
import unittest

from scripts.validate_skills import validate


class ValidateSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skills-validator-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.folder = self.root / "skills" / "example-skill"
        self.folder.mkdir(parents=True)
        self.entry = self.folder / "SKILL.md"
        self.entry.write_text(
            "---\nname: example-skill\ndescription: Create an example artifact.\n---\n",
            encoding="utf-8",
        )

    def append(self, text):
        with self.entry.open("a", encoding="utf-8") as stream:
            stream.write(text)

    def test_portable_package_with_reference(self):
        reference = self.folder / "references" / "example.md"
        reference.parent.mkdir()
        reference.write_text("# Example\n", encoding="utf-8")
        self.append("[Reference](references/example.md#example)\n")
        self.assertEqual(validate(self.root), [])

    def test_missing_reference_fails(self):
        self.append("[Reference](references/missing.md)\n")
        self.assertTrue(any("missing or external local target" in error for error in validate(self.root)))

    def test_package_without_entrypoint_fails(self):
        (self.root / "skills" / "unfinished-skill").mkdir()
        self.assertTrue(any("missing SKILL.md" in error for error in validate(self.root)))

    def test_name_mismatch_fails(self):
        self.entry.write_text("---\nname: different-name\ndescription: Example.\n---\n", encoding="utf-8")
        self.assertTrue(any("match the folder name" in error for error in validate(self.root)))

    def test_invalid_yaml_fails(self):
        self.entry.write_text("---\nname: [\n---\n", encoding="utf-8")
        self.assertTrue(any("invalid YAML" in error for error in validate(self.root)))

    def test_empty_description_fails(self):
        self.entry.write_text("---\nname: example-skill\ndescription: ''\n---\n", encoding="utf-8")
        self.assertTrue(any("description" in error for error in validate(self.root)))

    def test_fenced_examples_and_external_links_are_ignored(self):
        self.append("```markdown\n[Sample](missing.md)\n```\n[Source](https://example.com)\n")
        self.assertEqual(validate(self.root), [])

    def test_outside_repository_link_fails(self):
        self.append("[External file](../../../outside.md)\n")
        self.assertTrue(any("missing or external local target" in error for error in validate(self.root)))

    def test_legacy_top_level_metadata_fails(self):
        self.entry.write_text(
            "---\nname: example-skill\ndescription: Example.\nversion: 1.0.0\n---\n",
            encoding="utf-8",
        )
        self.assertTrue(any("place version under metadata" in error for error in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
