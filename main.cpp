

#include "TestHarness.h"
#include "TestResultStdErr.h"


int main()
{   
    TestResultStdErr result;
    //TestRegistry::runAllTests(result);
	//return (result.getFailureCount());
	//TestRegistry::runTestsbyFullName(result,"MyFixture","Test1");

	///TestRegistry::runTestsbySuite(result,"MyFixture");
	///TestRegistry::runTestsbySuite(result,"Double");
	///TestRegistry::runTestsbySuite(result,"CHECK");
	//TestRegistry::runTestsbyFullName(result,"CHECK","MyTest1");
	///TestRegistry::runTestsbySuite(result,"CHECK_CLOSE");
	//TestRegistry::runTestsbyFullName(result,"MyFixture","Test1");
	 ///TestRegistry::runTestsbySuite(result,"CHECK_STRINGS_EQUAL");

	 TestRegistry::runTestsbySuite(result,"check_eq");
	 TestRegistry::runTestsbySuite(result,"AAA");
	result.getTotalTestCases();
}

