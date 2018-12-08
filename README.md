# AutoGarden Server Application
This repo holds the code for the heroku server to send commands through a `POST` request and send that data to device with Socket.io

Example request to `/api/send/$device` :

```
{
  command: $command,
  data: $data
}
```

For device project repo go to: https://github.com/ericklikan/autogardener-device

For more information go to: https://autogarden-f6476.firebaseapp.com/
