
# Server architecture

## General 

Freespeech server is architectured as follows:

```
                             ----> [Comptoir]
                            |
[SocketServer] ----> [Chat]  ----> [Comptoir]
                            |
                             ----> ...
```

The `ServerSocket` is the external part of the server. It handles incoming connections and 
socket messages. The `Chat` object handles all messages relative to the chat functionnality
(new user connection, user disconnection, new message, etc.). Finally, there is one `Comptoir`
object for each "chat room".

When a socket message arrives from the network, it is first handled by the `SocketServer`.
Then, if relative to chat functionnality, it is forwarded to the `Chat`. The `Chat` parses
the socket message data to determine the source and the type of action to perform, and call the corresponding
method of the `Comptoirs`concerned by the source. 

### Example

1. A socket message arrives, it is handled by `ServerSocket`.
2. `ServerSocket` forwards it to `Chat`.
3. `Chat` parses it. Socket message is from user `loop` and contains a chat message for comptoir `abc`.
4. `Chat` forwards the chat message to the comptoir where `loop` is connected.
5. The `Comptoir` object handles the forwarding of the message to all users connected to `abc`.

## SocketServer


## Chat

## Comptoir
