
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
        # Test distance between two points
        # Point A: 0, 0
        # Point B: 1, 0 (1 degree latitude difference)
        # Expected: ~69.05 miles (using radius 3956)
        dist = SnoopR.haversine(0, 0, 0, 1)
        self.assertAlmostEqual(dist, 69.0467, places=1)

        # Same point
        dist_zero = SnoopR.haversine(10, 20, 10, 20)
        self.assertEqual(dist_zero, 0.0)

        # Long distance: NY (-74.006, 40.7128) to LA (-118.2437, 34.0522)
        # Approx 2446 miles
        dist_long = SnoopR.haversine(-74.006, 40.7128, -118.2437, 34.0522)
        self.assertTrue(2440 < dist_long < 2460)

if __name__ == '__main__':
    unittest.main()
