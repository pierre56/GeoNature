import { Component, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { AuthService } from '@geonature/components/auth/auth.service';
import { ConfigService } from '@geonature/utils/configModule/core';

@Component({
  selector: 'pnx-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  constructor(
    private _authService: AuthService,
    private translate: TranslateService,
    private _configService: ConfigService
  ) {
    translate.addLangs(['en', 'fr', 'cn']);
    const DEFAULT_LANGUAGE = this._configService.getSettings('DEFAULT_LANGUAGE');
    translate.setDefaultLang(DEFAULT_LANGUAGE);
    translate.use(DEFAULT_LANGUAGE);
  }

  ngOnInit() {}
}
