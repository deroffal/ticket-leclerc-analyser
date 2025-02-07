# ticket-leclerc-analyser

## Présentation

## Connexion
J'utilise les apis du site https://www.e.leclerc/.
Elles nécessitent d'avoir un compte.

Une fois connecté, récupérer la valeur du cookie `id_token` :

```javascript
// copy "allow pasting" to dev console to be able to copy this code
// allow pasting
document.cookie.split('; ').find(row => row.startsWith('id_token='))?.split('=')[1];
```
