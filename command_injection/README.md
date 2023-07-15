# Command Injection 

### Command Injection cause by using system function in web application. A System function, like os.system() in python, take shell command in operating system. In case of dynamic input system, the user's input controlling shell is very dangerous if there isn't checking system.

> In fact, developer should not use system function as possible.

<br>

#### General Meta character )
##### `;` : end former command and add new command in it's line
##### `&&` : Logical And. 
##### `||` : Logical Or.

</br>
