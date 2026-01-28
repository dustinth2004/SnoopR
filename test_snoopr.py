
import unittest
import SnoopR

class TestSnoopR(unittest.TestCase):
    def test_sanitize_string(self):
        self.assertEqual(SnoopR.sanitize_string("Hello World"), "Hello World")
        self.assertEqual(SnoopR.sanitize_string("Hello{World}"), "HelloWorld")
        self.assertEqual(SnoopR.sanitize_string("Hello|World"), "HelloWorld")
        self.assertEqual(SnoopR.sanitize_string("Hello[World]"), "HelloWorld")
        self.assertEqual(SnoopR.sanitize_string("Hello'World"), "HelloWorld")
        self.assertEqual(SnoopR.sanitize_string('Hello"World'), "HelloWorld")
        self.assertEqual(SnoopR.sanitize_string("Hello\\World"), "HelloWorld")
        self.assertEqual(SnoopR.sanitize_string("Hello<World>"), "HelloWorld")
        self.assertEqual(SnoopR.sanitize_string("Hello%World"), "HelloWorld")
        self.assertEqual(SnoopR.sanitize_string(None), "Unknown")
        self.assertEqual(SnoopR.sanitize_string(123), "123")

    def test_is_drone(self):
        # Known SSIDs
        self.assertTrue(SnoopR.is_drone("My DJI-Mavic Drone", "00:00:00:00:00:00"))
        self.assertTrue(SnoopR.is_drone("Just DJI here", "00:00:00:00:00:00"))
        self.assertTrue(SnoopR.is_drone("Autel-Evo II", "00:00:00:00:00:00"))

        # Known MACs
        self.assertTrue(SnoopR.is_drone("Unknown SSID", "60:60:1f:aa:bb:cc"))
        self.assertTrue(SnoopR.is_drone("Unknown SSID", "90:3A:E6:11:22:33")) # Uppercase check

        # Negative cases
        self.assertFalse(SnoopR.is_drone("My Home WiFi", "00:11:22:33:44:55"))
        self.assertFalse(SnoopR.is_drone(None, "00:11:22:33:44:55"))
        self.assertFalse(SnoopR.is_drone("", "00:11:22:33:44:55"))

    def test_haversine(self):
        # Test case: Distance between two known points
        # Point 1: (-80.5, 30.0)
        # Point 2: (-80.6, 30.1)
        # Expected distance ~ 9.13 miles
        dist = SnoopR.haversine(-80.5, 30.0, -80.6, 30.1)
        self.assertAlmostEqual(dist, 9.13, delta=0.1)

        # Zero distance
        self.assertEqual(SnoopR.haversine(0, 0, 0, 0), 0)

if __name__ == '__main__':
    unittest.main()
