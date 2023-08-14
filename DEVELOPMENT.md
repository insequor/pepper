# Notes on Development

## Application Structure 

Pepper will act as a hub for several applications  that might be designed for different purposes. For example, I'd like to use the command prompt interface for quick access. Web View will be the user interface executing commands. Below sections captures the notes for different applications.

### App
This represents the main pepper application. It is there to act as a central hub allowing other applications use to communicate.

### WebServer
A local webserver. I am not sure if we will need this yet but it looks like a good idea to be able to present information to the user.

### Command Prompt
An interface to interact with the application. The idea is we use a hotkey to show a quick access UI. This way we try to keep the user within the application they are working on and minimize the context switch 

### Web View
This is the application UI to show for the quick access