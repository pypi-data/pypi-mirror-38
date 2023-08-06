# RobotEyes
Visual Regression Library for Robot Framework

Uses Imagemagick to compare images and create a diff image. Also contains a report generator to create a custom
visual test report.

- Import the Library into your Robot test. Pass Mode("test" or "baseline") as argument.
- Call open eyes method after opening the browser in your selenium test.
- Use the capture full screen, capture element keywords to capture images.
- Call the compare images keyword at the end of the test to compare all the images captured in the respective test.
- Once done running the tests, execute the report generator script and pass the path to output directory .Eg reportgen results
- A custom report will be generated at the root of your project. 
- It will display the baseline images if run on "baseline" mode. Baseline, Actual and diff in "test" mode.

# Requirement
pip install robotframework-eyes <br/>
pip install pillow <br/>
Imagemagick (for mac: brew install imagemagick, linux: apt-get install imagemagick) <br/>

# Example
*** Settings ***    <br/>
**Library**  Selenium2Library    <br/>
**Library**  RobotEyes  test (or baseline, if running for the first time)  0.01(Global test tolerance, optional)    <br/>


*** Test Cases ***    
**Sample visual regression test case**   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;open browser  https://www.google.com/  chrome     <br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;maximize browser window    <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;open eyes    <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;wait until element is visible  id=lst-ib    <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;@{blur}  id=body  css=#SIvCob    <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;capture full screen  0.05(tolerance to override global value, optional)  blur=${blur}(regions to blur from image)   radius=50(thickness of the blur)  <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;capture element  id=hplogo    <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;compare images    <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;close browser

To generate the report:
**reportgen /path/to/output directory**

# Keyword Documentation
**open eyes** - Arguments: lib Eg AppiumLibrary (optional) - (Gets current selenium/appium instance) <br/>
**capture full screen** - Arguments: tolerance, blur(array of locators to blur, optional), radius(thickness of blur, optional) - (Captures an entire page)<br/>
**capture element** - Arguments: locator, blur(array of locators to blur, optional), radius(thickness of blur, optional)(Captures a region or an individual element in a webpage)<br/>
**capture mobile element** - Arguments: locator - (Captures a region or an individual element in a mobile screen)<br/>
**scroll to element** - Arguments: locator - (Scrolls to an element in a webpage)<br/>
**compare images** - Arguments: None - (Compares baseline and actual images of a testcase)<br/>
