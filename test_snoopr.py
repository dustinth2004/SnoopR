
import unittest
import SnoopR
from math import isclose

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
        # 1 degree longitude at equator
        d1 = SnoopR.haversine(0, 0, 1, 0)
        self.assertTrue(isclose(d1, 69.04522520889567, rel_tol=1e-9))

        # 1 degree latitude
        d2 = SnoopR.haversine(0, 0, 0, 1)
        self.assertTrue(isclose(d2, 69.04522520889567, rel_tol=1e-9))

        # Arbitrary points: (-80, 30) to (-80.1, 30.1)
        # 0.1 degree change in both.
        # Expected value from pre-optimization check: 9.3876 (calculated below or in previous step? No, previous step didn't print d3)
        # Let's rely on calculation for the test.
        from math import radians, sin, cos, asin, sqrt
        lon1, lat1, lon2, lat2 = map(radians, [-80.0, 30.0, -80.1, 30.1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        expected_miles = 3956 * c

        d3 = SnoopR.haversine(-80.0, 30.0, -80.1, 30.1)
        self.assertTrue(isclose(d3, expected_miles, rel_tol=1e-9))

if __name__ == '__main__':
    unittest.main()
