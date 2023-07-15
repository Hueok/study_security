# Command Injection 

#### Command Injection cause by using system function in web application. A System function, like os.system() in python, take shell command in operating system. In case of dynamic input system, the user's input controlling shell is very dangerous if there isn't checking system.  
> In fact, developer should not use system function as possible.

## General Meta character )
##### `;` : end former command and add new command in it's line  
##### `&&` : Logical And. 
##### `||` : Logical Or.  

## Problems I had.  
```py
host = request.form.get('host')
cmd = f'ping -c 3 "{host}"'
try:
    output = subprocess.check_output(['/bin/sh', '-c', cmd], timeout=5)
    return render_template('ping_result.html', data=output.decode('utf-8'))
except subprocess.TimeoutExpired:
    return render_template('ping_result.html', data='Timeout !')
except subprocess.CalledProcessError:
    return render_template('ping_result.html', data=f'an error occurred while executing the command. -> {cmd}')
```
In this code, I didn't know about double quotation meta character in linux shell.  
So I take input of `request.form.get('host')` as `1.1.1.1"; "ls -a` first, but I got `CalledProcessError`.  
In my case, in the command `"ls -a"`, `-a` is not treated as option argument by shell. this is a feature of double quotation. So I can't use command with argument.  
__SOLVE__ : first use main command keyword out of `"`, and take an option or other argument in `"`. ex ) `ls "-a"`. So the solution of this question is `1.1.1.1"; cat "flag.py`
