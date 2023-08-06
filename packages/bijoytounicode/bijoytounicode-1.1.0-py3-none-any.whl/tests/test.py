import unittest
from bijoytounicode import bijoy2unicode


class TestConversion(unittest.TestCase):

    def test_basic_conversion(self):
        TEST_TEXT = "‡Kv‡bv †Kv‡bv w`b, AvKvk‡Rvov †gN K‡i, Kv‡R gb e‡m bv| †W‡¯‹i mvg‡bi Rvbvjvi c`©v Zz‡j w`B| w¯Œ‡b ZvKvB, †`wL bv, `‚ieZ©x AvKvk I Bgvi‡Z wKQz †LvuR _v‡K| Ggb me w`‡bi bvg †KvgjMvÜvi|"
        CONVERTED_TEST_TEXT = 'কোনো কোনো দিন, আকাশজোড়া মেঘ করে, কাজে মন বসে না। ডেস্কের সামনের জানালার পর্দা তুলে দিই। স্ক্রিনে তাকাই, দেখি না, দূরবর্তী আকাশ ও ইমারতে কিছু খোঁজ থাকে। এমন সব দিনের নাম কোমলগান্ধার।'
        CONVERTED = bijoy2unicode(TEST_TEXT)
        self.assertEqual(CONVERTED, CONVERTED_TEST_TEXT)


if __name__ == '__main__':
    unittest.main()
