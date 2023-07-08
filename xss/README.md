# Diff of XSS and CSRF

> ### Target of XSS is "Client" While that of CSRF is "Server".

<br>

## XSS)

#### XSS use point that the "USER trusts website".

#### So, XSS take fake website or backdoor for client so that the user get deceived.

#### The start point of attack : When a person, not admin, can insert malware script in the website. While web application not accurately check the value user inputed.

#### The result : Hacker can hijack cookie, session... 

##### ex) community board.

## CSRF)

#### CSRF use point that the "website trusts USER's web browser."

#### So, CSRF forge the request to get some USER's permission.

<br>
