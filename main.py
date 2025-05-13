import time
import unittest

from BasePageTest import BasePageTest
from MainPageTest import MainPageTest
from PartnerPageTest import PartnerPageTest
from RegisterBusinessPageTest import RegisterBusinessPageTest
from RegisterRepetitorPageTest import RegisterRepetitorPageTest
from SearchPageTest import SearchPageTest

# List of test classes to run
test_classes = [
    BasePageTest,
    MainPageTest,
    PartnerPageTest,
    RegisterBusinessPageTest,
    RegisterRepetitorPageTest,
    SearchPageTest,
]

if __name__ == "__main__":
    fail_count = 0
    total_tests = len(test_classes)

    print("\n🧪 Starting Selenium Test Suite\n")
    print("=" * 60)

    for idx, test_class in enumerate(test_classes, start=1):
        print(f"\n🔹 [{idx}/{total_tests}] Running tests in: `{test_class.__name__}`\n")
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        result = unittest.TextTestRunner(verbosity=2).run(suite)

        time.sleep(0.1)

        if not result.wasSuccessful():
            print(f"\n❌ Tests FAILED in '{test_class.__name__}'")
            fail_count += 1
        else:
            print(f"\n✅ All tests PASSED in '{test_class.__name__}'")

        print("\n" + "-" * 60)

    # Summary
    print("\n📊 Test Run Summary")
    print("=" * 60)
    print(f"🔸 Total test classes run: {total_tests}")
    print(f"✅ Passed: {total_tests - fail_count}")
    print(f"❌ Failed: {fail_count}")
    print("=" * 60)

    if fail_count > 0:
        print("\n🚨 Some tests failed. Check output above for details.")
    else:
        print("\n🎉 All tests passed successfully!")
