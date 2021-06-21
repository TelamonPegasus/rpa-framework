*** Settings ***
Library           RPA.JavaAccessBridge
Library           Process
Suite Setup       Start Demo Application
Task Setup        Task setup actions
Suite Teardown    Exit Demo Application
Force Tags        windows    skip

*** Variables ***
${RESOURCES}      ${CURDIR}${/}..${/}resources
${TEST_APP}       ${RESOURCES}${/}test-app${/}BasicSwing.jar

*** Keywords ***
Start Demo Application
    Start Process    java -jar ${TEST_APP}    shell=${TRUE}    cwd=${CURDIR}

*** Keywords ***
Exit Demo Application
    Select Window    Chat Frame
    Select Menu    FILE    Exit
    Select Window    Exit
    Click Push Button    Exit ok

*** Keywords ***
Clear chat frame
    Click Element    role:push button and name:Clear

*** Keywords ***
Task setup actions
    Select Window    Chat Frame
    Clear chat frame

*** Tasks ***
Click element
    Click Element    role:push button and name:Send

Click push button
    Click Push Button    Send
    Click Push Button    Clear

Print Element Tree
    ${tree}=    Print Element Tree

Typing text
    Type Text    role:text    textarea text
    Type Text    role:text    input field text    index=1    clear=${TRUE}
    ${area_text}=    Get Element Text    role:text    0
    ${input_text}=    Get Element Text    role:text    1
    Should Contain    ${area_text}    textarea text
    Should Be Equal As Strings    input field text    ${input_text}

Get elements
    ${elements}=    Get Elements    role:text
    ${len}=    Get Length    ${elements}
    Should Be Equal As Integers    ${len}    2
    Log Many    ${elements}[0]
    Log Many    ${elements}[1]
    Highlight Element    ${elements}[0]
    Highlight Element    ${elements}[1]
