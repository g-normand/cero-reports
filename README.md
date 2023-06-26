# Sixth report of the CERO
A map of rare birds seen in Ecuador (according to the sixth report of the CERO)

Inspired by <a href="https://zoziologie.raphaelnussbaumer.com/global-rare-ebird/">![image](https://user-images.githubusercontent.com/7571260/190668681-2bd06339-2568-4da2-9931-bccc5e95c360.png)</a>

# Installation

```
git clone git@github.com:g-normand/global-rare-ebird.git cero-report
cd cero-report
git checkout _cero

npm install
npm run processObs
npm run dev

FOR PROD:
npm run build
scp -r dist/* guiguide@ssh-guiguide.alwaysdata.net:/home/guiguide/www/cero_report/
```
