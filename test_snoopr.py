
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
        # Test Case 1: Same point
        self.assertAlmostEqual(SnoopR.haversine(0, 0, 0, 0), 0.0)
        self.assertAlmostEqual(SnoopR.haversine(-80.0, 30.0, -80.0, 30.0), 0.0)

        # Test Case 2: 1 degree latitude difference
        # Approx 69 miles (69.055 miles)
        dist_lat = SnoopR.haversine(0, 0, 0, 1)
        self.assertAlmostEqual(dist_lat, 69.09, delta=0.5)

        # Test Case 3: 1 degree longitude difference at equator
        dist_lon = SnoopR.haversine(0, 0, 1, 0)
        self.assertAlmostEqual(dist_lon, 69.09, delta=0.5)

        # Test Case 4: Known distance
        # NY (-74.0060, 40.7128) to LA (-118.2437, 34.0522)
        # Approx 2446 miles
        dist_ny_la = SnoopR.haversine(-74.0060, 40.7128, -118.2437, 34.0522)
        self.assertAlmostEqual(dist_ny_la, 2450, delta=20) # Approx check

if __name__ == '__main__':
    unittest.main()
