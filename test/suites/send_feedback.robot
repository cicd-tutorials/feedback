*** Settings ***
Library             OperatingSystem
Library             Browser  auto_closing_level=SUITE
Suite Setup         Check URL and open browser
Suite Teardown      Close browser

*** Variables ***
${BROWSER}          chromium
${URL}              ${EMPTY}

*** Test cases ***
Send positive feedback
    New Page  ${URL}
    Click  text=👍
    Click  text=Submit

Check feedback was recorded
    Get value count  Thumbs up  1

Send another positive feedback and check summary
    Reload
    Click  text=👍
    Click  text=Submit
    Get value count  Thumbs up  2

Send negative feedback and check summary
    Reload
    Click  text=👎
    Click  text=Submit
    Get value count  Thumbs down  1

*** Keywords ***
Open browser defined by environment
    ${browser}=  Get Environment Variable    BROWSER    ${BROWSER}
    New Browser  ${browser}
    New Context  viewport={'width': 1280, 'height': 720}

Check URL and open browser
    Skip if  not $URL  msg=Target URL not specified
    Open browser defined by environment

Get value count
    [Arguments]  ${title}  ${count}
    ${elem}=  Get element by  title  ${title}
    Get element  ${elem} >> text=${count}
