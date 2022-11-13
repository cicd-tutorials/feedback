*** Settings ***
Library             OperatingSystem
Library             SeleniumLibrary
Suite Setup         Check URL and open browser
Suite Teardown      Close browser

*** Variables ***
${BROWSER}          headlesschrome
${BROWSER_OPTIONS}  ${EMPTY}
${URL}              ${EMPTY}
${WAIT_PAGE_LOAD}   10 seconds

*** Test cases ***
Send positive feedback
    Go to  ${URL}
    Sleep  ${WAIT_PAGE_LOAD}
    Click button  //*[text()="👍"]

Check feedback was recorded
    Wait until element contains  id:results-count-positive  1  5 seconds

Send another positive feedback and check summary
    Reload page
    Click button  //*[text()="👍"]
    Wait until element contains  id:results-count-positive  2  5 seconds

Send neative feedback and check summary
    Reload page
    Click button  //*[text()="👎"]
    Wait until element contains  id:results-count-negative  1  5 seconds

*** Keywords ***
Open browser defined by environment
    ${browser_options}=  Get Environment Variable    BROWSER_OPTIONS    ${BROWSER_OPTIONS}
    ${browser}=  Get Environment Variable    BROWSER    ${BROWSER}
    Open browser    browser=${browser}    options=${browser_options}
    Set Screenshot Directory  ${OUTPUT DIR}${/}${browser}_screenshots

Check URL and open browser
    Skip if  not $URL  msg=Target URL not specified
    Open browser defined by environment
