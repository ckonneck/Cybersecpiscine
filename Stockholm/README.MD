Greetings Traveller.

This program shows off different implementations of encryptionprocesses.
This program however only encrypts files in a folder called "infection" <-(case sensitive) which needs to be located in the HOME Directory of your Computer. 
so for example: /home/yourusername/infection
To use this Program, you will go to the folder of Stockholm and open a terminal.
You will then type in the command line:
make
after all the requirements have been installed and the virtual environment has been started, you will be able to use either make ssl if you wish to use my ssl implementation 
or make pynacl if you wish to try my pynacl implementation.

You can of course reverse the encryption with either make pynacl_rev or make ssl_rev.

Alternatively, you can check the -help for either program
or type make help, the instructions are the same for both programs.

to use those options together with the make command, you would need to type something like make ssl ARGS="-r -s -v or -h"
type make help to see the options you have.

The encryptionkeys will be created in the Stockholm folder if you use any encryptioncommand. 
Keep in mind, that without these keys, you won't be able to undo the encryption, and your files will be rendered useless.
The keys will have to be located at the base of the Stockholm folder, or the reversing command won't work.

