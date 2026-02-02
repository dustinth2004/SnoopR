
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
        # Distance between two known points
        # New York (40.7128, -74.0060) to London (51.5074, -0.1278)
        # Expected distance approx 3461 miles
        dist = SnoopR.haversine(-74.0060, 40.7128, -0.1278, 51.5074)
        self.assertAlmostEqual(dist, 3461, delta=50)

        # Same point
        self.assertEqual(SnoopR.haversine(0, 0, 0, 0), 0)

if __name__ == '__main__':
    unittest.main()
