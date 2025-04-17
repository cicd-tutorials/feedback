*** Settings ***
Library             OperatingSystem
Library             Browser  auto_closing_level=SUITE
Suite Setup         Check URL and open browser
Suite Teardown      Close browser

*** Variables ***
${BROWSER}          chromium
${URL}              %{BASE_URL}

*** Test cases ***
Open feedback form
    New Page  ${URL}?key=thumbs
    Wait For Elements State  text=How are you feeling?  timeout=1 minute

Send positive feedback
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
    Skip if  not $URL  msg=BASE_URL environment variable or URL variable must be defined
    Open browser defined by environment

Get value count
    [Arguments]  ${title}  ${count}
    ${elem}=  Get element by  title  ${title}
    Get element  ${elem} >> text=${count}
