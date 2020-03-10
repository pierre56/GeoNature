import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

// import { AppModule } from '@geonature/app.module';
import { AppModule } from './app/app.module';
import { AppConfig } from './conf/app.config';
import { environment } from './environments/environment';

if (environment) {
  enableProdMode();
}

platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .catch(err => console.log(err));
